"""
AI Image Studio - CLI Interface
Phase 5 Implementation: Unified command-line interface for AI image generation
"""

import argparse
import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from prompt_engine import PromptEngine, PromptABTester
from image_analyzer import ImageQualityAnalyzer, FeedbackLoop

class AIStudioCLI:
    """Unified CLI interface for AI image generation and analysis"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.config_path = self.base_path / "config" / "studio_config.json"
        self.prompt_engine = PromptEngine()
        self.image_analyzer = ImageQualityAnalyzer()
        self.feedback_loop = FeedbackLoop(self.image_analyzer)
        self.ab_tester = PromptABTester()
        
        self.config = self._load_config()
        self.generation_queue = []
        
    def _load_config(self) -> Dict:
        """Load CLI configuration"""
        default_config = {
            "platforms": {
                "midjourney": {
                    "enabled": True,
                    "api_endpoint": None,
                    "default_params": "--ar 1:1 --v 6 --quality 2"
                },
                "dalle": {
                    "enabled": True,
                    "api_key": None,
                    "api_endpoint": "https://api.openai.com/v1/images/generations",
                    "default_size": "1024x1024",
                    "default_quality": "hd"
                },
                "stable_diffusion": {
                    "enabled": True,
                    "api_endpoint": None,
                    "default_model": "SDXL",
                    "default_steps": 30,
                    "default_cfg": 7
                }
            },
            "output": {
                "base_directory": str(self.base_path / "generated"),
                "organize_by_date": True,
                "organize_by_platform": True,
                "save_metadata": True
            },
            "analysis": {
                "auto_analyze": True,
                "save_analysis": True,
                "quality_threshold": 70
            },
            "batch": {
                "max_concurrent": 3,
                "retry_failed": True,
                "max_retries": 2
            }
        }
        
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    return {**default_config, **loaded_config}
            else:
                # Create config file with defaults
                self.config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
    
    def generate_single(self, product_data: Dict, 
                       category: str = "food",
                       style: str = "product_showcase",
                       platform: str = "midjourney",
                       analyze: bool = True) -> Dict:
        """Generate a single image with prompt optimization"""
        try:
            # Generate optimized prompt
            prompt_data = self.prompt_engine.generate_prompt(
                product_data=product_data,
                category=category,
                style=style,
                platform=platform
            )
            
            print(f"Generated prompt: {prompt_data['prompt']}")
            
            # Simulate image generation (replace with actual API calls)
            generated_image_path = self._simulate_generation(prompt_data, platform)
            
            result = {
                "prompt_data": prompt_data,
                "generated_image_path": generated_image_path,
                "platform": platform,
                "status": "success"
            }
            
            # Auto-analysis if enabled
            if analyze and self.config["analysis"]["auto_analyze"]:
                analysis_result = self.image_analyzer.analyze_image(
                    generated_image_path, 
                    prompt_data
                )
                result["analysis"] = analysis_result
                
                # Quality check
                overall_score = analysis_result["scores"]["overall"]
                if overall_score < self.config["analysis"]["quality_threshold"]:
                    print(f"Warning: Generated image quality score ({overall_score:.1f}) below threshold")
                    result["quality_warning"] = True
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "product_data": product_data
            }
    
    def generate_batch(self, products_file: str,
                      category: str = "food",
                      styles: List[str] = None,
                      platforms: List[str] = None,
                      output_report: str = None) -> Dict:
        """Generate images for multiple products"""
        
        if styles is None:
            styles = ["product_showcase"]
        if platforms is None:
            platforms = ["midjourney"]
            
        # Load products data
        try:
            with open(products_file, 'r', encoding='utf-8') as f:
                if products_file.endswith('.json'):
                    products_data = json.load(f)
                else:
                    # Assume CSV format
                    import pandas as pd
                    df = pd.read_csv(products_file)
                    products_data = df.to_dict('records')
        except Exception as e:
            return {"error": f"Failed to load products file: {e}"}
        
        print(f"Starting batch generation for {len(products_data)} products")
        print(f"Styles: {styles}")
        print(f"Platforms: {platforms}")
        
        batch_results = []
        total_combinations = len(products_data) * len(styles) * len(platforms)
        completed = 0
        
        for product in products_data:
            for style in styles:
                for platform in platforms:
                    print(f"Processing {completed + 1}/{total_combinations}: {product.get('name', 'Unknown')} - {style} - {platform}")
                    
                    result = self.generate_single(
                        product_data=product,
                        category=category,
                        style=style,
                        platform=platform,
                        analyze=True
                    )
                    
                    batch_results.append(result)
                    completed += 1
                    
                    # Progress update
                    if completed % 5 == 0:
                        success_rate = sum(1 for r in batch_results if r.get("status") == "success") / len(batch_results) * 100
                        print(f"Progress: {completed}/{total_combinations} ({success_rate:.1f}% success rate)")
        
        # Generate batch report
        report = self._generate_batch_report(batch_results)
        
        # Save report if requested
        if output_report:
            with open(output_report, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def analyze_existing(self, image_path: str, 
                        prompt_file: str = None,
                        detailed: bool = True) -> Dict:
        """Analyze existing image quality and prompt matching"""
        
        prompt_data = None
        if prompt_file:
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompt_data = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load prompt file: {e}")
        
        analysis_result = self.image_analyzer.analyze_image(
            image_path=image_path,
            prompt_data=prompt_data,
            save_to_db=True
        )
        
        if detailed:
            self._print_detailed_analysis(analysis_result)
        
        return analysis_result
    
    def optimize_prompt(self, base_prompt: str,
                       optimization_goals: List[str] = None,
                       test_variations: int = 3) -> Dict:
        """Optimize prompt using A/B testing approach"""
        
        if not optimization_goals:
            optimization_goals = ["higher_quality"]
        
        # Create base prompt data
        base_prompt_data = {
            "prompt": base_prompt,
            "id": "base_prompt",
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate variations
        variations = []
        for i in range(test_variations):
            optimized = self.prompt_engine.optimize_prompt(
                base_prompt_data, optimization_goals
            )
            optimized["variation_id"] = f"var_{i+1}"
            variations.append(optimized)
        
        print(f"Generated {len(variations)} prompt variations:")
        for var in variations:
            print(f"- {var['variation_id']}: {var['prompt'][:100]}...")
        
        return {
            "base_prompt": base_prompt_data,
            "variations": variations,
            "optimization_goals": optimization_goals,
            "recommendation": "Test all variations and compare results"
        }
    
    def run_ab_test(self, prompt_a: str, prompt_b: str,
                   test_name: str = None,
                   product_data: Dict = None,
                   platform: str = "midjourney") -> str:
        """Set up A/B test for two prompts"""
        
        if not test_name:
            test_name = f"prompt_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create prompt data structures
        prompt_data_a = {
            "prompt": prompt_a,
            "id": "prompt_a",
            "platform": platform
        }
        prompt_data_b = {
            "prompt": prompt_b,
            "id": "prompt_b",
            "platform": platform
        }
        
        # Create A/B test
        test_id = self.ab_tester.create_test(
            test_name=test_name,
            prompt_a=prompt_data_a,
            prompt_b=prompt_data_b,
            success_metric="overall_quality"
        )
        
        print(f"A/B test '{test_name}' created with ID: {test_id}")
        print("Generate images with both prompts and record results using:")
        print(f"  record_ab_result {test_id} a <quality_score>")
        print(f"  record_ab_result {test_id} b <quality_score>")
        
        return test_id
    
    def record_ab_result(self, test_id: str, variant: str, 
                        quality_score: float,
                        additional_metrics: Dict = None):
        """Record A/B test result"""
        
        try:
            self.ab_tester.record_result(
                test_id=test_id,
                prompt_variant=variant,
                success_value=quality_score,
                additional_metrics=additional_metrics
            )
            print(f"Recorded result for test {test_id}, variant {variant}: {quality_score}")
        except Exception as e:
            print(f"Error recording result: {e}")
    
    def analyze_ab_test(self, test_id: str) -> Dict:
        """Analyze A/B test results"""
        
        try:
            analysis = self.ab_tester.analyze_test(test_id)
            
            print(f"\nA/B Test Analysis: {analysis['test_name']}")
            print(f"Samples A: {analysis['samples_a']}, Samples B: {analysis['samples_b']}")
            print(f"Average A: {analysis['average_a']:.2f}, Average B: {analysis['average_b']:.2f}")
            print(f"Winner: Prompt {analysis['winner'].upper()}")
            print(f"Improvement: {analysis['improvement_percentage']:.1f}%")
            print(f"Confidence: {analysis['confidence']}")
            print(f"Recommendation: {analysis['recommendation']}")
            
            return analysis
        except Exception as e:
            print(f"Error analyzing test: {e}")
            return {"error": str(e)}
    
    def configure_platform(self, platform: str, **kwargs):
        """Configure platform-specific settings"""
        
        if platform not in self.config["platforms"]:
            self.config["platforms"][platform] = {}
        
        for key, value in kwargs.items():
            self.config["platforms"][platform][key] = value
        
        # Save updated config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
        
        print(f"Updated configuration for {platform}: {kwargs}")
    
    def export_library(self, output_path: str = None,
                      min_quality: float = 70) -> str:
        """Export high-quality prompts as reusable library"""
        
        library_path = self.prompt_engine.export_prompt_library(output_path)
        
        print(f"Prompt library exported to: {library_path}")
        return library_path
    
    def _simulate_generation(self, prompt_data: Dict, platform: str) -> str:
        """Simulate image generation (replace with actual API calls)"""
        
        # Create output directory structure
        output_dir = Path(self.config["output"]["base_directory"])
        
        if self.config["output"]["organize_by_date"]:
            date_dir = datetime.now().strftime("%Y%m%d")
            output_dir = output_dir / date_dir
        
        if self.config["output"]["organize_by_platform"]:
            output_dir = output_dir / platform
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{prompt_data['id']}_{timestamp}.jpg"
        image_path = output_dir / filename
        
        # Create placeholder image file (in real implementation, save actual generated image)
        placeholder_content = f"Generated with prompt: {prompt_data['prompt'][:100]}..."
        with open(str(image_path).replace('.jpg', '.txt'), 'w', encoding='utf-8') as f:
            f.write(placeholder_content)
        
        # Save metadata if enabled
        if self.config["output"]["save_metadata"]:
            metadata_path = str(image_path).replace('.jpg', '_metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
        
        print(f"Image generated: {image_path}")
        return str(image_path)
    
    def _generate_batch_report(self, batch_results: List[Dict]) -> Dict:
        """Generate comprehensive batch processing report"""
        
        total = len(batch_results)
        successful = sum(1 for r in batch_results if r.get("status") == "success")
        failed = total - successful
        
        # Quality analysis
        quality_scores = []
        for result in batch_results:
            if result.get("analysis", {}).get("scores"):
                quality_scores.append(result["analysis"]["scores"]["overall"])
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Platform distribution
        platform_stats = {}
        for result in batch_results:
            platform = result.get("platform", "unknown")
            if platform not in platform_stats:
                platform_stats[platform] = {"total": 0, "successful": 0}
            platform_stats[platform]["total"] += 1
            if result.get("status") == "success":
                platform_stats[platform]["successful"] += 1
        
        # Common issues
        common_issues = {}
        for result in batch_results:
            if result.get("analysis", {}).get("recommendations"):
                for rec in result["analysis"]["recommendations"]:
                    common_issues[rec] = common_issues.get(rec, 0) + 1
        
        report = {
            "summary": {
                "total_generations": total,
                "successful": successful,
                "failed": failed,
                "success_rate": successful / total * 100,
                "average_quality_score": avg_quality,
                "generated_at": datetime.now().isoformat()
            },
            "platform_performance": platform_stats,
            "quality_distribution": {
                "excellent": sum(1 for s in quality_scores if s > 90),
                "good": sum(1 for s in quality_scores if 70 < s <= 90),
                "fair": sum(1 for s in quality_scores if 50 < s <= 70),
                "poor": sum(1 for s in quality_scores if s <= 50)
            },
            "common_issues": common_issues,
            "failed_generations": [r for r in batch_results if r.get("status") != "success"]
        }
        
        return report
    
    def _print_detailed_analysis(self, analysis_result: Dict):
        """Print detailed analysis results"""
        
        print(f"\n{'='*50}")
        print(f"IMAGE ANALYSIS REPORT")
        print(f"{'='*50}")
        
        print(f"Image ID: {analysis_result['id']}")
        print(f"Image Path: {analysis_result['image_path']}")
        print(f"Analysis Time: {analysis_result['timestamp']}")
        
        scores = analysis_result['scores']
        print(f"\nOVERALL SCORES:")
        print(f"  Technical Quality: {scores['technical']:.1f}/100")
        print(f"  Aesthetic Quality: {scores['aesthetic']:.1f}/100")
        print(f"  Prompt Matching: {scores['prompt_match']:.1f}/100")
        print(f"  Overall Score: {scores['overall']:.1f}/100")
        
        print(f"\nAUTO-GENERATED TAGS:")
        for tag in analysis_result['auto_tags']:
            print(f"  - {tag}")
        
        print(f"\nRECOMMENDATIONS:")
        for rec in analysis_result['recommendations']:
            print(f"  - {rec}")


def create_cli_parser():
    """Create command-line argument parser"""
    
    parser = argparse.ArgumentParser(
        description="AI Image Studio - Advanced AI image generation and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate single image
  python ai_studio_cli.py generate --product "Korean BBQ" --style product_showcase --platform midjourney
  
  # Batch generation from CSV
  python ai_studio_cli.py batch --input products.csv --styles product_showcase,lifestyle --platforms midjourney,dalle
  
  # Analyze existing image
  python ai_studio_cli.py analyze --image path/to/image.jpg --prompt prompt_data.json
  
  # Optimize prompt
  python ai_studio_cli.py optimize --prompt "product photo" --goals higher_quality,more_creative
  
  # A/B test prompts
  python ai_studio_cli.py ab-test --prompt-a "photo A" --prompt-b "photo B" --name "test1"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate single image
    gen_parser = subparsers.add_parser('generate', help='Generate single image')
    gen_parser.add_argument('--product', required=True, help='Product name or JSON data')
    gen_parser.add_argument('--category', default='food', help='Product category')
    gen_parser.add_argument('--style', default='product_showcase', help='Image style')
    gen_parser.add_argument('--platform', default='midjourney', help='AI platform')
    gen_parser.add_argument('--no-analyze', action='store_true', help='Skip analysis')
    
    # Batch generation
    batch_parser = subparsers.add_parser('batch', help='Batch generate images')
    batch_parser.add_argument('--input', required=True, help='Input CSV/JSON file')
    batch_parser.add_argument('--category', default='food', help='Product category')
    batch_parser.add_argument('--styles', help='Comma-separated styles')
    batch_parser.add_argument('--platforms', help='Comma-separated platforms')
    batch_parser.add_argument('--output-report', help='Output report file path')
    
    # Analyze image
    analyze_parser = subparsers.add_parser('analyze', help='Analyze existing image')
    analyze_parser.add_argument('--image', required=True, help='Image file path')
    analyze_parser.add_argument('--prompt', help='Associated prompt JSON file')
    analyze_parser.add_argument('--brief', action='store_true', help='Brief analysis only')
    
    # Optimize prompt
    opt_parser = subparsers.add_parser('optimize', help='Optimize prompt')
    opt_parser.add_argument('--prompt', required=True, help='Base prompt to optimize')
    opt_parser.add_argument('--goals', help='Comma-separated optimization goals')
    opt_parser.add_argument('--variations', type=int, default=3, help='Number of variations')
    
    # A/B test
    ab_parser = subparsers.add_parser('ab-test', help='Create A/B test')
    ab_parser.add_argument('--prompt-a', required=True, help='First prompt')
    ab_parser.add_argument('--prompt-b', required=True, help='Second prompt')
    ab_parser.add_argument('--name', help='Test name')
    ab_parser.add_argument('--platform', default='midjourney', help='Platform')
    
    # Record A/B result
    record_parser = subparsers.add_parser('record-ab', help='Record A/B test result')
    record_parser.add_argument('--test-id', required=True, help='Test ID')
    record_parser.add_argument('--variant', required=True, choices=['a', 'b'], help='Variant')
    record_parser.add_argument('--score', type=float, required=True, help='Quality score')
    
    # Analyze A/B test
    ab_analyze_parser = subparsers.add_parser('analyze-ab', help='Analyze A/B test')
    ab_analyze_parser.add_argument('--test-id', required=True, help='Test ID')
    
    # Configure platform
    config_parser = subparsers.add_parser('config', help='Configure platform')
    config_parser.add_argument('--platform', required=True, help='Platform name')
    config_parser.add_argument('--api-key', help='API key')
    config_parser.add_argument('--endpoint', help='API endpoint')
    
    # Export library
    export_parser = subparsers.add_parser('export', help='Export prompt library')
    export_parser.add_argument('--output', help='Output file path')
    export_parser.add_argument('--min-quality', type=float, default=70, help='Minimum quality score')
    
    return parser


def main():
    """Main CLI entry point"""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = AIStudioCLI()
    
    try:
        if args.command == 'generate':
            # Parse product data
            try:
                product_data = json.loads(args.product)
            except:
                product_data = {"name": args.product}
            
            result = cli.generate_single(
                product_data=product_data,
                category=args.category,
                style=args.style,
                platform=args.platform,
                analyze=not args.no_analyze
            )
            
            if result.get("status") == "success":
                print("Generation completed successfully!")
                if result.get("analysis"):
                    score = result["analysis"]["scores"]["overall"]
                    print(f"Quality Score: {score:.1f}/100")
            else:
                print(f"Generation failed: {result.get('error', 'Unknown error')}")
        
        elif args.command == 'batch':
            styles = args.styles.split(',') if args.styles else None
            platforms = args.platforms.split(',') if args.platforms else None
            
            report = cli.generate_batch(
                products_file=args.input,
                category=args.category,
                styles=styles,
                platforms=platforms,
                output_report=args.output_report
            )
            
            if "error" in report:
                print(f"Batch generation failed: {report['error']}")
            else:
                summary = report["summary"]
                print(f"Batch completed: {summary['successful']}/{summary['total_generations']} successful")
                print(f"Success rate: {summary['success_rate']:.1f}%")
                print(f"Average quality: {summary['average_quality_score']:.1f}/100")
        
        elif args.command == 'analyze':
            result = cli.analyze_existing(
                image_path=args.image,
                prompt_file=args.prompt,
                detailed=not args.brief
            )
            
            if not args.brief:
                print(f"Analysis completed. Overall score: {result['scores']['overall']:.1f}/100")
        
        elif args.command == 'optimize':
            goals = args.goals.split(',') if args.goals else None
            
            result = cli.optimize_prompt(
                base_prompt=args.prompt,
                optimization_goals=goals,
                test_variations=args.variations
            )
            
            print("Prompt optimization completed!")
            print(f"Generated {len(result['variations'])} variations")
        
        elif args.command == 'ab-test':
            test_id = cli.run_ab_test(
                prompt_a=args.prompt_a,
                prompt_b=args.prompt_b,
                test_name=args.name,
                platform=args.platform
            )
        
        elif args.command == 'record-ab':
            cli.record_ab_result(
                test_id=args.test_id,
                variant=args.variant,
                quality_score=args.score
            )
        
        elif args.command == 'analyze-ab':
            cli.analyze_ab_test(args.test_id)
        
        elif args.command == 'config':
            config_data = {}
            if args.api_key:
                config_data['api_key'] = args.api_key
            if args.endpoint:
                config_data['api_endpoint'] = args.endpoint
            
            cli.configure_platform(args.platform, **config_data)
        
        elif args.command == 'export':
            library_path = cli.export_library(
                output_path=args.output,
                min_quality=args.min_quality
            )
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()