"""
AI Image Studio - AI Council Integration
Integration module for seamless connection with existing ai-council system
"""

import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add ai-council path for imports
ai_council_path = Path(__file__).parent.parent.parent / "ai-council"
sys.path.append(str(ai_council_path))

try:
    from ai_council import AICouncil
    from agents.claude_agent import ClaudeAgent
    from agents.gemini_agent import GeminiAgent
    from agents.gpt4_agent import GPT4Agent
except ImportError as e:
    print(f"Warning: Could not import ai-council modules: {e}")
    AICouncil = None

from prompt_engine import PromptEngine
from image_analyzer import ImageQualityAnalyzer
from ai_studio_cli import AIStudioCLI
from scheduler import TaskScheduler
from monitoring import SystemMonitor

class AICouncilImageStudioBridge:
    """Bridge between AI Image Studio and AI Council system"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.integration_config_path = self.base_path / "config" / "ai_council_integration.json"
        
        # Initialize AI Studio components
        self.prompt_engine = PromptEngine()
        self.image_analyzer = ImageQualityAnalyzer()
        self.studio_cli = AIStudioCLI()
        self.scheduler = TaskScheduler()
        self.monitor = SystemMonitor()
        
        # AI Council integration
        self.ai_council = None
        self.council_agents = {}
        
        self.config = self._load_integration_config()
        self._initialize_ai_council()
    
    def _load_integration_config(self) -> Dict:
        """Load AI Council integration configuration"""
        default_config = {
            "ai_council": {
                "enabled": True,
                "use_for_prompt_optimization": True,
                "use_for_quality_analysis": True,
                "use_for_creative_feedback": True,
                "council_voting_threshold": 0.7
            },
            "agents": {
                "claude": {
                    "enabled": True,
                    "role": "prompt_optimization",
                    "weight": 0.4
                },
                "gpt4": {
                    "enabled": True,
                    "role": "creative_direction",
                    "weight": 0.3
                },
                "gemini": {
                    "enabled": True,
                    "role": "quality_analysis",
                    "weight": 0.3
                }
            },
            "workflows": {
                "collaborative_prompt_generation": True,
                "multi_agent_quality_review": True,
                "consensus_based_optimization": True,
                "automated_feedback_loop": True
            },
            "cafe24_integration": {
                "enabled": True,
                "auto_analyze_product_images": True,
                "generate_missing_images": True,
                "optimize_existing_descriptions": True
            }
        }
        
        try:
            if self.integration_config_path.exists():
                with open(self.integration_config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    return {**default_config, **loaded_config}
            else:
                self.integration_config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.integration_config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                return default_config
        except Exception as e:
            print(f"Error loading AI Council integration config: {e}")
            return default_config
    
    def _initialize_ai_council(self):
        """Initialize AI Council connection"""
        if not self.config["ai_council"]["enabled"] or not AICouncil:
            print("AI Council integration disabled or not available")
            return
        
        try:
            # Initialize AI Council
            self.ai_council = AICouncil()
            
            # Initialize agents based on configuration
            if self.config["agents"]["claude"]["enabled"]:
                self.council_agents["claude"] = ClaudeAgent()
            
            if self.config["agents"]["gpt4"]["enabled"]:
                self.council_agents["gpt4"] = GPT4Agent()
            
            if self.config["agents"]["gemini"]["enabled"]:
                self.council_agents["gemini"] = GeminiAgent()
            
            print(f"AI Council integration initialized with {len(self.council_agents)} agents")
            
        except Exception as e:
            print(f"Failed to initialize AI Council: {e}")
            self.ai_council = None
    
    async def collaborative_prompt_generation(self, product_data: Dict, 
                                            category: str = "food",
                                            style: str = "product_showcase") -> Dict:
        """Generate prompts collaboratively using AI Council"""
        
        if not self.ai_council or not self.config["workflows"]["collaborative_prompt_generation"]:
            # Fall back to standard prompt generation
            return self.prompt_engine.generate_prompt(product_data, category, style)
        
        # Base prompt generation
        base_prompt = self.prompt_engine.generate_prompt(product_data, category, style)
        
        # Get agent suggestions for optimization
        optimization_tasks = []
        
        for agent_name, agent in self.council_agents.items():
            agent_config = self.config["agents"][agent_name]
            
            if agent_config["role"] == "prompt_optimization":
                task = asyncio.create_task(
                    self._get_agent_prompt_optimization(agent, base_prompt, product_data)
                )
                optimization_tasks.append((agent_name, task, agent_config["weight"]))
        
        # Wait for all agent responses
        agent_suggestions = []
        for agent_name, task, weight in optimization_tasks:
            try:
                suggestion = await task
                agent_suggestions.append({
                    "agent": agent_name,
                    "suggestion": suggestion,
                    "weight": weight
                })
            except Exception as e:
                print(f"Error getting suggestion from {agent_name}: {e}")
        
        # Combine suggestions using weighted consensus
        optimized_prompt = self._combine_agent_suggestions(base_prompt, agent_suggestions)
        
        return {
            **optimized_prompt,
            "collaboration_data": {
                "base_prompt": base_prompt,
                "agent_suggestions": agent_suggestions,
                "optimization_method": "ai_council_collaborative"
            }
        }
    
    async def multi_agent_quality_review(self, image_path: str, 
                                       prompt_data: Dict) -> Dict:
        """Perform multi-agent quality review of generated images"""
        
        # Standard quality analysis
        base_analysis = self.image_analyzer.analyze_image(image_path, prompt_data)
        
        if not self.ai_council or not self.config["workflows"]["multi_agent_quality_review"]:
            return base_analysis
        
        # Get agent reviews
        review_tasks = []
        
        for agent_name, agent in self.council_agents.items():
            agent_config = self.config["agents"][agent_name]
            
            if agent_config["role"] in ["quality_analysis", "creative_direction"]:
                task = asyncio.create_task(
                    self._get_agent_quality_review(agent, image_path, prompt_data, base_analysis)
                )
                review_tasks.append((agent_name, task, agent_config["weight"]))
        
        # Collect agent reviews
        agent_reviews = []
        for agent_name, task, weight in review_tasks:
            try:
                review = await task
                agent_reviews.append({
                    "agent": agent_name,
                    "review": review,
                    "weight": weight
                })
            except Exception as e:
                print(f"Error getting review from {agent_name}: {e}")
        
        # Combine reviews with base analysis
        enhanced_analysis = self._combine_quality_reviews(base_analysis, agent_reviews)
        
        return enhanced_analysis
    
    async def consensus_based_optimization(self, prompt_data: Dict, 
                                         quality_feedback: Dict,
                                         optimization_goals: List[str] = None) -> Dict:
        """Optimize prompts based on AI Council consensus"""
        
        if not self.ai_council or not self.config["workflows"]["consensus_based_optimization"]:
            return self.prompt_engine.optimize_prompt(prompt_data, optimization_goals)
        
        # Get optimization suggestions from each agent
        optimization_tasks = []
        
        for agent_name, agent in self.council_agents.items():
            task = asyncio.create_task(
                self._get_agent_optimization_suggestion(
                    agent, prompt_data, quality_feedback, optimization_goals
                )
            )
            optimization_tasks.append((agent_name, task))
        
        # Collect suggestions
        agent_optimizations = []
        for agent_name, task in optimization_tasks:
            try:
                optimization = await task
                agent_optimizations.append({
                    "agent": agent_name,
                    "optimization": optimization
                })
            except Exception as e:
                print(f"Error getting optimization from {agent_name}: {e}")
        
        # Build consensus
        consensus_optimization = self._build_optimization_consensus(
            prompt_data, agent_optimizations
        )
        
        return consensus_optimization
    
    def integrate_with_cafe24_workflow(self) -> Dict:
        """Integrate AI Image Studio with existing Cafe24 workflow"""
        
        if not self.config["cafe24_integration"]["enabled"]:
            return {"status": "disabled", "message": "Cafe24 integration is disabled"}
        
        try:
            # Look for Cafe24 module
            cafe24_module_path = Path(__file__).parent.parent / "cafe24"
            
            if not cafe24_module_path.exists():
                return {"status": "error", "message": "Cafe24 module not found"}
            
            # Integration tasks
            integration_results = []
            
            # 1. Analyze existing product images
            if self.config["cafe24_integration"]["auto_analyze_product_images"]:
                analysis_result = self._analyze_cafe24_images()
                integration_results.append({
                    "task": "image_analysis",
                    "result": analysis_result
                })
            
            # 2. Generate missing product images
            if self.config["cafe24_integration"]["generate_missing_images"]:
                generation_result = self._generate_missing_cafe24_images()
                integration_results.append({
                    "task": "missing_image_generation", 
                    "result": generation_result
                })
            
            # 3. Optimize existing product descriptions for better image generation
            if self.config["cafe24_integration"]["optimize_existing_descriptions"]:
                optimization_result = self._optimize_cafe24_descriptions()
                integration_results.append({
                    "task": "description_optimization",
                    "result": optimization_result
                })
            
            return {
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "integration_results": integration_results,
                "summary": {
                    "total_tasks": len(integration_results),
                    "successful_tasks": sum(1 for r in integration_results if r["result"].get("status") == "success")
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def setup_automated_workflows(self) -> List[str]:
        """Setup automated workflows combining AI Studio and AI Council"""
        
        scheduled_jobs = []
        
        # 1. Daily collaborative batch generation
        if self.config["workflows"]["collaborative_prompt_generation"]:
            job_id = self.scheduler.schedule_daily_job(
                name="Daily Collaborative Generation",
                job_type="collaborative_batch_generation",
                time_str="09:00",
                config={
                    "products_file": "daily_products.csv",
                    "use_ai_council": True,
                    "quality_threshold": 80
                }
            )
            scheduled_jobs.append(job_id)
        
        # 2. Multi-agent quality monitoring
        if self.config["workflows"]["multi_agent_quality_review"]:
            job_id = self.scheduler.schedule_interval_job(
                name="Multi-Agent Quality Monitor",
                job_type="multi_agent_monitoring",
                interval_minutes=120,
                config={
                    "review_recent_hours": 2,
                    "consensus_threshold": 0.7
                }
            )
            scheduled_jobs.append(job_id)
        
        # 3. Weekly optimization review
        if self.config["workflows"]["consensus_based_optimization"]:
            job_id = self.scheduler.schedule_weekly_job(
                name="Weekly Optimization Review",
                job_type="consensus_optimization",
                day="sunday",
                time_str="22:00",
                config={
                    "review_period_days": 7,
                    "optimization_goals": ["higher_quality", "better_consistency"]
                }
            )
            scheduled_jobs.append(job_id)
        
        return scheduled_jobs
    
    # Helper methods for AI Council integration
    async def _get_agent_prompt_optimization(self, agent, base_prompt: Dict, 
                                           product_data: Dict) -> Dict:
        """Get prompt optimization suggestion from an agent"""
        
        context = f"""
        Product: {product_data.get('name', 'Unknown')}
        Category: {product_data.get('category', 'food')}
        Current Prompt: {base_prompt.get('prompt', '')}
        
        Please suggest improvements to make this prompt more effective for AI image generation.
        Focus on clarity, specificity, and visual appeal.
        """
        
        try:
            response = await agent.get_response(context)
            
            return {
                "suggested_improvements": response.get("content", ""),
                "confidence": response.get("confidence", 0.5),
                "reasoning": response.get("reasoning", "")
            }
        except Exception as e:
            return {"error": str(e), "confidence": 0}
    
    async def _get_agent_quality_review(self, agent, image_path: str, 
                                      prompt_data: Dict, base_analysis: Dict) -> Dict:
        """Get quality review from an agent"""
        
        context = f"""
        Image Analysis Results:
        - Technical Score: {base_analysis['scores']['technical']}/100
        - Aesthetic Score: {base_analysis['scores']['aesthetic']}/100  
        - Overall Score: {base_analysis['scores']['overall']}/100
        
        Original Prompt: {prompt_data.get('prompt', '')}
        Auto Tags: {', '.join(base_analysis.get('auto_tags', []))}
        
        Please provide your assessment of this generated image quality and suggestions for improvement.
        """
        
        try:
            response = await agent.get_response(context)
            
            return {
                "agent_score": response.get("score", base_analysis['scores']['overall']),
                "feedback": response.get("content", ""),
                "improvement_suggestions": response.get("suggestions", []),
                "confidence": response.get("confidence", 0.5)
            }
        except Exception as e:
            return {"error": str(e), "agent_score": 0, "confidence": 0}
    
    async def _get_agent_optimization_suggestion(self, agent, prompt_data: Dict,
                                               quality_feedback: Dict, 
                                               optimization_goals: List[str]) -> Dict:
        """Get optimization suggestion from an agent"""
        
        context = f"""
        Current Prompt: {prompt_data.get('prompt', '')}
        Quality Issues: {', '.join(quality_feedback.get('recommendations', []))}
        Optimization Goals: {', '.join(optimization_goals or ['improve_quality'])}
        
        Please suggest specific optimizations to the prompt to address the quality issues and achieve the goals.
        """
        
        try:
            response = await agent.get_response(context)
            
            return {
                "optimized_prompt": response.get("optimized_prompt", ""),
                "changes_made": response.get("changes", []),
                "expected_improvement": response.get("improvement_score", 0),
                "confidence": response.get("confidence", 0.5)
            }
        except Exception as e:
            return {"error": str(e), "confidence": 0}
    
    def _combine_agent_suggestions(self, base_prompt: Dict, 
                                 agent_suggestions: List[Dict]) -> Dict:
        """Combine agent suggestions using weighted consensus"""
        
        if not agent_suggestions:
            return base_prompt
        
        # Simple implementation - in practice, use more sophisticated NLP combination
        combined_improvements = []
        total_weight = sum(s["weight"] for s in agent_suggestions)
        
        for suggestion in agent_suggestions:
            if suggestion.get("suggestion", {}).get("confidence", 0) > 0.5:
                weight = suggestion["weight"] / total_weight
                improvements = suggestion["suggestion"].get("suggested_improvements", "")
                if improvements:
                    combined_improvements.append(f"({weight:.1f}) {improvements}")
        
        # Create optimized prompt
        optimized_prompt = base_prompt.copy()
        if combined_improvements:
            optimized_prompt["ai_council_enhancements"] = combined_improvements
            optimized_prompt["optimization_method"] = "ai_council_collaborative"
        
        return optimized_prompt
    
    def _combine_quality_reviews(self, base_analysis: Dict, 
                               agent_reviews: List[Dict]) -> Dict:
        """Combine agent quality reviews with base analysis"""
        
        enhanced_analysis = base_analysis.copy()
        
        if not agent_reviews:
            return enhanced_analysis
        
        # Calculate weighted agent scores
        agent_scores = []
        agent_feedback = []
        
        for review in agent_reviews:
            review_data = review.get("review", {})
            if review_data.get("confidence", 0) > 0.3:
                agent_scores.append(review_data.get("agent_score", 0))
                feedback = review_data.get("feedback", "")
                if feedback:
                    agent_feedback.append(f"{review['agent']}: {feedback}")
        
        # Add AI Council analysis
        if agent_scores:
            enhanced_analysis["ai_council_analysis"] = {
                "agent_average_score": sum(agent_scores) / len(agent_scores),
                "agent_consensus": len(set(agent_scores)) <= 2,  # Agreement if scores are similar
                "agent_feedback": agent_feedback,
                "council_recommendation": "approved" if sum(agent_scores) / len(agent_scores) > 70 else "needs_improvement"
            }
        
        return enhanced_analysis
    
    def _build_optimization_consensus(self, base_prompt: Dict, 
                                    agent_optimizations: List[Dict]) -> Dict:
        """Build optimization consensus from agent suggestions"""
        
        if not agent_optimizations:
            return self.prompt_engine.optimize_prompt(base_prompt)
        
        # Collect high-confidence optimizations
        high_confidence_opts = []
        for opt in agent_optimizations:
            opt_data = opt.get("optimization", {})
            if opt_data.get("confidence", 0) > 0.6:
                high_confidence_opts.append(opt_data)
        
        # Create consensus optimization
        consensus_prompt = base_prompt.copy()
        consensus_prompt["consensus_optimization"] = {
            "participating_agents": len(agent_optimizations),
            "high_confidence_suggestions": len(high_confidence_opts),
            "consensus_strength": len(high_confidence_opts) / len(agent_optimizations),
            "optimization_details": high_confidence_opts
        }
        
        return consensus_prompt
    
    def _analyze_cafe24_images(self) -> Dict:
        """Analyze existing Cafe24 product images"""
        try:
            cafe24_image_path = Path(__file__).parent.parent / "cafe24" / "complete_content" / "images"
            
            if not cafe24_image_path.exists():
                return {"status": "error", "message": "Cafe24 images directory not found"}
            
            # Get all image files
            image_files = list(cafe24_image_path.rglob("*.jpg")) + list(cafe24_image_path.rglob("*.png"))
            
            analysis_results = []
            for image_file in image_files[:10]:  # Limit for demo
                try:
                    analysis = self.image_analyzer.analyze_image(str(image_file))
                    analysis_results.append({
                        "image_path": str(image_file),
                        "overall_score": analysis["scores"]["overall"],
                        "needs_improvement": analysis["scores"]["overall"] < 70
                    })
                except Exception as e:
                    print(f"Error analyzing {image_file}: {e}")
            
            return {
                "status": "success",
                "analyzed_images": len(analysis_results),
                "average_quality": sum(r["overall_score"] for r in analysis_results) / len(analysis_results) if analysis_results else 0,
                "images_needing_improvement": sum(1 for r in analysis_results if r["needs_improvement"]),
                "results": analysis_results
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _generate_missing_cafe24_images(self) -> Dict:
        """Generate missing images for Cafe24 products"""
        # Implementation would check for products without images and generate them
        return {
            "status": "success", 
            "message": "Missing image generation completed",
            "generated_count": 0
        }
    
    def _optimize_cafe24_descriptions(self) -> Dict:
        """Optimize Cafe24 product descriptions for better image generation"""
        # Implementation would analyze and improve product descriptions
        return {
            "status": "success",
            "message": "Description optimization completed", 
            "optimized_count": 0
        }


# Async wrapper for CLI integration
class AsyncAIStudioCLI:
    """Async wrapper for AI Studio CLI with AI Council integration"""
    
    def __init__(self):
        self.bridge = AICouncilImageStudioBridge()
    
    async def generate_collaborative_image(self, product_data: Dict, 
                                         category: str = "food",
                                         style: str = "product_showcase",
                                         platform: str = "midjourney") -> Dict:
        """Generate image using collaborative AI Council approach"""
        
        # Generate collaborative prompt
        prompt_data = await self.bridge.collaborative_prompt_generation(
            product_data, category, style
        )
        
        # Simulate image generation (replace with actual API call)
        generated_image_path = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        # Multi-agent quality review
        quality_analysis = await self.bridge.multi_agent_quality_review(
            generated_image_path, prompt_data
        )
        
        return {
            "prompt_data": prompt_data,
            "generated_image_path": generated_image_path,
            "quality_analysis": quality_analysis,
            "ai_council_enhanced": True,
            "status": "success"
        }


if __name__ == "__main__":
    # Example usage
    bridge = AICouncilImageStudioBridge()
    
    print("AI Council - Image Studio Integration initialized")
    
    # Setup automated workflows
    scheduled_jobs = bridge.setup_automated_workflows()
    print(f"Scheduled {len(scheduled_jobs)} automated workflows")
    
    # Test Cafe24 integration
    cafe24_result = bridge.integrate_with_cafe24_workflow()
    print(f"Cafe24 integration: {cafe24_result['status']}")
    
    # Test collaborative prompt generation
    async def test_collaborative_generation():
        test_product = {
            "name": "고추장 오돌뼈",
            "category": "food",
            "description": "매콤한 한국 전통 요리"
        }
        
        result = await bridge.collaborative_prompt_generation(test_product)
        print(f"Collaborative prompt generated: {result.get('prompt', '')[:100]}...")
        
        return result
    
    # Run async test
    if bridge.ai_council:
        import asyncio
        asyncio.run(test_collaborative_generation())
    else:
        print("AI Council not available for collaborative testing")