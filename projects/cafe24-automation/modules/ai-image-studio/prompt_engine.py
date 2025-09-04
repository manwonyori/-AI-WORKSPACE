"""
AI Image Studio - Prompt Engine
Phase 3 Implementation: Advanced prompt generation and optimization system
"""

import json
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib

class PromptEngine:
    """Advanced prompt engineering system for AI image generation"""
    
    def __init__(self, templates_path: str = None):
        self.base_path = Path(__file__).parent
        self.templates_path = templates_path or self.base_path / "prompts" / "prompt_templates.json"
        self.templates = self._load_templates()
        self.generation_history = []
        self.quality_metrics = {}
        
    def _load_templates(self) -> Dict:
        """Load prompt templates from JSON file"""
        try:
            with open(self.templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Templates file not found: {self.templates_path}")
            return {}
    
    def generate_prompt(self, 
                       product_data: Dict, 
                       category: str = "food", 
                       style: str = "product_showcase",
                       platform: str = "midjourney") -> Dict:
        """
        Generate optimized prompt for AI image generation
        
        Args:
            product_data: Dictionary containing product information
            category: Template category (food, ecommerce, etc.)
            style: Style template to use
            platform: Target AI platform (midjourney, dalle, stable_diffusion)
            
        Returns:
            Dictionary containing generated prompt and metadata
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get base template
        base_template = self.templates["categories"][category]["base_templates"].get(style, "")
        if not base_template:
            raise ValueError(f"Template not found: {category}/{style}")
        
        # Fill template with product data
        filled_prompt = self._fill_template(base_template, product_data, category)
        
        # Add quality parameters
        quality_prompt = self._add_quality_parameters(filled_prompt)
        
        # Add platform-specific formatting
        final_prompt = self._format_for_platform(quality_prompt, platform, product_data)
        
        # Generate negative prompt
        negative_prompt = self._generate_negative_prompt(category)
        
        prompt_data = {
            "id": hashlib.md5(f"{final_prompt}{timestamp}".encode()).hexdigest()[:8],
            "timestamp": timestamp,
            "product_data": product_data,
            "category": category,
            "style": style,
            "platform": platform,
            "prompt": final_prompt,
            "negative_prompt": negative_prompt,
            "quality_score": None,  # To be filled after generation
            "metadata": {
                "template_used": f"{category}/{style}",
                "prompt_length": len(final_prompt),
                "estimated_generation_time": self._estimate_generation_time(platform)
            }
        }
        
        self.generation_history.append(prompt_data)
        return prompt_data
    
    def _fill_template(self, template: str, product_data: Dict, category: str) -> str:
        """Fill template placeholders with product data"""
        # Basic product information
        filled = template.format(
            product_name=product_data.get('name', 'product'),
            style_description=product_data.get('style', 'modern'),
            background_setting=product_data.get('background', 'clean white background'),
            lighting_type=product_data.get('lighting', 'studio'),
            camera_angle=product_data.get('angle', '45-degree'),
            context_setting=product_data.get('context', 'kitchen environment'),
            mood_description=product_data.get('mood', 'warm and inviting'),
            demographic_target=product_data.get('target', 'family'),
            texture_details=product_data.get('texture', 'fresh and detailed'),
            color_palette=product_data.get('colors', 'natural vibrant colors'),
            artistic_style=product_data.get('art_style', 'professional photography'),
            usage_context=product_data.get('usage', 'everyday use'),
            target_audience=product_data.get('audience', 'general consumers'),
            product_feature=product_data.get('feature', 'main product'),
            material_texture=product_data.get('material', 'high quality'),
            size_specification=product_data.get('size', 'medium shot')
        )
        
        return filled
    
    def _add_quality_parameters(self, prompt: str) -> str:
        """Add quality enhancement parameters to prompt"""
        quality_params = self.templates["quality_parameters"]
        
        # Randomly select quality enhancers
        resolution = random.choice(quality_params["resolution"])
        style_quality = random.choice(quality_params["style_quality"])
        composition = random.choice(quality_params["composition"])
        
        enhanced_prompt = f"{prompt}, {resolution}, {style_quality}, {composition}"
        return enhanced_prompt
    
    def _format_for_platform(self, prompt: str, platform: str, product_data: Dict) -> str:
        """Format prompt for specific AI platform"""
        platform_config = self.templates["platform_specific"].get(platform, {})
        
        if platform == "midjourney":
            prefix = platform_config.get("prefix", "")
            aspect_ratio = product_data.get("aspect_ratio", "1:1")
            parameters = platform_config["parameters"].format(
                aspect_ratio=aspect_ratio,
                style_value=product_data.get("style_value", "raw")
            )
            return f"{prefix}{prompt}{parameters}"
            
        elif platform == "dalle":
            # DALL-E uses simpler formatting
            return prompt
            
        elif platform == "stable_diffusion":
            # Add SD-specific parameters
            return f"{prompt}, masterpiece, best quality, highly detailed"
        
        return prompt
    
    def _generate_negative_prompt(self, category: str) -> str:
        """Generate negative prompt to avoid unwanted elements"""
        negatives = []
        
        # Common negative prompts
        negatives.append(self.templates["negative_prompts"]["common"])
        
        # Category-specific negatives
        if category in self.templates["negative_prompts"]:
            category_key = f"{category}_specific"
            if category_key in self.templates["negative_prompts"]:
                negatives.append(self.templates["negative_prompts"][category_key])
        
        return ", ".join(negatives)
    
    def _estimate_generation_time(self, platform: str) -> int:
        """Estimate generation time in seconds based on platform"""
        time_estimates = {
            "midjourney": 60,
            "dalle": 30,
            "stable_diffusion": 45
        }
        return time_estimates.get(platform, 45)
    
    def batch_generate_prompts(self, products_list: List[Dict], 
                              category: str = "food",
                              styles: List[str] = None,
                              platform: str = "midjourney") -> List[Dict]:
        """Generate prompts for multiple products"""
        if styles is None:
            styles = ["product_showcase", "lifestyle", "ingredient_focus"]
        
        batch_prompts = []
        
        for product in products_list:
            for style in styles:
                try:
                    prompt_data = self.generate_prompt(
                        product_data=product,
                        category=category,
                        style=style,
                        platform=platform
                    )
                    batch_prompts.append(prompt_data)
                except Exception as e:
                    print(f"Error generating prompt for {product.get('name', 'unknown')}: {e}")
                    continue
        
        return batch_prompts
    
    def evaluate_prompt_quality(self, prompt_data: Dict, 
                              generation_success: bool = True,
                              user_rating: int = None,
                              generation_time: float = None) -> float:
        """
        Evaluate prompt quality based on various metrics
        
        Args:
            prompt_data: Generated prompt data
            generation_success: Whether generation was successful
            user_rating: User rating (1-5 scale)
            generation_time: Actual generation time
            
        Returns:
            Quality score (0-100)
        """
        score = 0
        
        # Base score for successful generation
        if generation_success:
            score += 40
        
        # Prompt length optimization (not too short, not too long)
        prompt_length = len(prompt_data["prompt"])
        if 50 <= prompt_length <= 200:
            score += 20
        elif 200 < prompt_length <= 300:
            score += 15
        elif prompt_length > 300:
            score += 5
        
        # User rating contribution
        if user_rating:
            score += user_rating * 8  # Max 40 points from user rating
        
        # Time efficiency
        if generation_time:
            estimated_time = prompt_data["metadata"]["estimated_generation_time"]
            if generation_time <= estimated_time * 0.8:
                score += 10  # Faster than expected
            elif generation_time <= estimated_time * 1.2:
                score += 5   # Within expected range
        
        # Store quality score
        prompt_data["quality_score"] = min(score, 100)
        self.quality_metrics[prompt_data["id"]] = score
        
        return score
    
    def get_best_performing_templates(self, category: str = None, 
                                   min_score: float = 70,
                                   limit: int = 10) -> List[Dict]:
        """Get best performing prompt templates based on quality scores"""
        scored_prompts = [p for p in self.generation_history if p.get("quality_score")]
        
        if category:
            scored_prompts = [p for p in scored_prompts if p["category"] == category]
        
        # Filter by minimum score
        good_prompts = [p for p in scored_prompts if p["quality_score"] >= min_score]
        
        # Sort by quality score
        good_prompts.sort(key=lambda x: x["quality_score"], reverse=True)
        
        return good_prompts[:limit]
    
    def optimize_prompt(self, base_prompt_data: Dict, 
                       optimization_goals: List[str] = None) -> Dict:
        """
        Optimize existing prompt based on performance data and goals
        
        Args:
            base_prompt_data: Existing prompt data to optimize
            optimization_goals: List of goals like ['faster', 'higher_quality', 'more_creative']
            
        Returns:
            Optimized prompt data
        """
        if not optimization_goals:
            optimization_goals = ['higher_quality']
        
        optimized_data = base_prompt_data.copy()
        original_prompt = base_prompt_data["prompt"]
        
        # Apply optimizations based on goals
        if 'higher_quality' in optimization_goals:
            # Add more quality descriptors
            quality_enhancers = [
                "ultra-realistic", "masterpiece", "award-winning photography",
                "professional lighting", "perfect composition"
            ]
            enhancer = random.choice(quality_enhancers)
            optimized_data["prompt"] = f"{original_prompt}, {enhancer}"
        
        if 'faster' in optimization_goals:
            # Simplify prompt for faster generation
            simplified = re.sub(r',\s*ultra detailed.*?,', ',', original_prompt)
            optimized_data["prompt"] = simplified
        
        if 'more_creative' in optimization_goals:
            # Add creative elements
            creative_elements = [
                "artistic interpretation", "unique perspective", 
                "creative composition", "innovative styling"
            ]
            element = random.choice(creative_elements)
            optimized_data["prompt"] = f"{original_prompt}, {element}"
        
        # Update metadata
        optimized_data["id"] = f"{optimized_data['id']}_opt"
        optimized_data["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")
        optimized_data["metadata"]["optimization_goals"] = optimization_goals
        optimized_data["metadata"]["optimized_from"] = base_prompt_data["id"]
        
        return optimized_data
    
    def export_prompt_library(self, output_path: str = None) -> str:
        """Export generated prompts as a reusable library"""
        if not output_path:
            output_path = self.base_path / "prompts" / f"prompt_library_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Filter high-quality prompts
        library_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_prompts": len(self.generation_history),
                "average_quality": sum(p.get("quality_score", 0) for p in self.generation_history) / len(self.generation_history) if self.generation_history else 0
            },
            "high_quality_prompts": self.get_best_performing_templates(min_score=80),
            "templates_used": list(set(p["metadata"]["template_used"] for p in self.generation_history)),
            "platform_distribution": self._get_platform_distribution()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(library_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def _get_platform_distribution(self) -> Dict[str, int]:
        """Get distribution of prompts across platforms"""
        distribution = {}
        for prompt in self.generation_history:
            platform = prompt["platform"]
            distribution[platform] = distribution.get(platform, 0) + 1
        return distribution

# A/B Testing Framework
class PromptABTester:
    """A/B testing framework for prompt optimization"""
    
    def __init__(self):
        self.test_groups = {}
        self.results = {}
    
    def create_test(self, test_name: str, 
                   prompt_a: Dict, 
                   prompt_b: Dict,
                   success_metric: str = "user_rating") -> str:
        """Create A/B test for two prompts"""
        test_id = hashlib.md5(f"{test_name}_{datetime.now()}".encode()).hexdigest()[:8]
        
        self.test_groups[test_id] = {
            "name": test_name,
            "prompt_a": prompt_a,
            "prompt_b": prompt_b,
            "success_metric": success_metric,
            "results_a": [],
            "results_b": [],
            "created": datetime.now().isoformat()
        }
        
        return test_id
    
    def record_result(self, test_id: str, prompt_variant: str, 
                     success_value: float, additional_metrics: Dict = None):
        """Record result for A/B test"""
        if test_id not in self.test_groups:
            raise ValueError(f"Test {test_id} not found")
        
        result_data = {
            "success_value": success_value,
            "timestamp": datetime.now().isoformat(),
            "additional_metrics": additional_metrics or {}
        }
        
        if prompt_variant == "a":
            self.test_groups[test_id]["results_a"].append(result_data)
        elif prompt_variant == "b":
            self.test_groups[test_id]["results_b"].append(result_data)
        else:
            raise ValueError("Prompt variant must be 'a' or 'b'")
    
    def analyze_test(self, test_id: str) -> Dict:
        """Analyze A/B test results"""
        test = self.test_groups.get(test_id)
        if not test:
            raise ValueError(f"Test {test_id} not found")
        
        results_a = test["results_a"]
        results_b = test["results_b"]
        
        if not results_a or not results_b:
            return {"status": "insufficient_data", "message": "Need results for both variants"}
        
        # Calculate averages
        avg_a = sum(r["success_value"] for r in results_a) / len(results_a)
        avg_b = sum(r["success_value"] for r in results_b) / len(results_b)
        
        # Determine winner
        winner = "a" if avg_a > avg_b else "b"
        improvement = abs(avg_a - avg_b) / min(avg_a, avg_b) * 100
        
        analysis = {
            "test_name": test["name"],
            "samples_a": len(results_a),
            "samples_b": len(results_b),
            "average_a": avg_a,
            "average_b": avg_b,
            "winner": winner,
            "improvement_percentage": improvement,
            "confidence": self._calculate_confidence(results_a, results_b),
            "recommendation": self._get_recommendation(winner, improvement, results_a, results_b)
        }
        
        self.results[test_id] = analysis
        return analysis
    
    def _calculate_confidence(self, results_a: List, results_b: List) -> str:
        """Calculate statistical confidence level"""
        # Simplified confidence calculation
        sample_size = min(len(results_a), len(results_b))
        
        if sample_size >= 30:
            return "high"
        elif sample_size >= 10:
            return "medium"
        else:
            return "low"
    
    def _get_recommendation(self, winner: str, improvement: float, 
                          results_a: List, results_b: List) -> str:
        """Get actionable recommendation"""
        sample_size = min(len(results_a), len(results_b))
        
        if improvement > 10 and sample_size >= 10:
            return f"Strong recommendation: Use prompt {winner.upper()}"
        elif improvement > 5 and sample_size >= 20:
            return f"Moderate recommendation: Use prompt {winner.upper()}"
        else:
            return "Continue testing - results inconclusive"


if __name__ == "__main__":
    # Example usage and testing
    engine = PromptEngine()
    
    # Test product data
    test_product = {
        "name": "고추장 오돌뼈",
        "style": "traditional Korean",
        "background": "wooden table",
        "lighting": "natural",
        "angle": "45-degree",
        "context": "Korean dining room",
        "mood": "warm and traditional",
        "target": "Korean food lovers",
        "colors": "rich red and natural tones",
        "aspect_ratio": "4:3"
    }
    
    # Generate prompt
    prompt_data = engine.generate_prompt(test_product, "food", "product_showcase", "midjourney")
    print("Generated Prompt:")
    print(prompt_data["prompt"])
    print("\nNegative Prompt:")
    print(prompt_data["negative_prompt"])
    
    # Simulate quality evaluation
    quality_score = engine.evaluate_prompt_quality(
        prompt_data, 
        generation_success=True, 
        user_rating=4, 
        generation_time=45
    )
    print(f"\nQuality Score: {quality_score}")
    
    # Export library
    library_path = engine.export_prompt_library()
    print(f"\nPrompt library exported to: {library_path}")