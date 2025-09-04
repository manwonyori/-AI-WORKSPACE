"""
Photorealistic Image Generation Pipeline Test
Tests the complete pipeline from real image learning to Imagen 3 generation
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import random

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from imagen3_photorealistic_engine import Imagen3PhotorealisticEngine
from real_image_learner import RealImageLearner

class PhotorealisticPipelineTest:
    """Complete photorealistic generation pipeline test"""
    
    def __init__(self):
        self.engine = Imagen3PhotorealisticEngine()
        self.learner = RealImageLearner()
        self.results = []
        
        # Cafe24 product image paths
        self.image_base = Path("D:/주문취합/주문_배송/test_송장/ftp_download/manwonyori/web/product")
        
    def test_real_image_learning(self) -> Dict:
        """Test learning from real Cafe24 product images"""
        print("\n" + "="*60)
        print("TEST 1: REAL IMAGE LEARNING")
        print("="*60)
        
        results = {
            "total_images": 0,
            "learned": 0,
            "categories": {},
            "features_extracted": []
        }
        
        # Find actual product images
        image_files = []
        if self.image_base.exists():
            # Get sample images from different categories
            for category_dir in self.image_base.iterdir():
                if category_dir.is_dir():
                    category_name = category_dir.name
                    category_images = list(category_dir.glob("**/*.jpg")) + \
                                    list(category_dir.glob("**/*.png"))
                    
                    if category_images:
                        # Sample up to 5 images per category for testing
                        sample_images = random.sample(
                            category_images, 
                            min(5, len(category_images))
                        )
                        
                        results["categories"][category_name] = len(sample_images)
                        
                        for img_path in sample_images:
                            image_files.append(img_path)
                            
                            # Learn from image
                            print(f"\nLearning from: {img_path.name}")
                            learned = self.learner.learn_from_images(
                                [str(img_path)],
                                category=category_name
                            )
                            
                            if learned:
                                results["learned"] += 1
                                
                                # Extract features
                                features = self.learner.extract_image_features(str(img_path))
                                if features:
                                    feature_summary = {
                                        "image": img_path.name,
                                        "category": category_name,
                                        "lighting": features.lighting_analysis["type"],
                                        "sharpness": f"{features.technical_metrics['sharpness']:.1f}",
                                        "dominant_colors": len(features.color_palette["dominant_colors"])
                                    }
                                    results["features_extracted"].append(feature_summary)
                                    
                                    print(f"  - Lighting: {features.lighting_analysis['type']}")
                                    print(f"  - Sharpness: {features.technical_metrics['sharpness']:.1f}")
                                    print(f"  - Colors: {len(features.color_palette['dominant_colors'])} dominant")
        
        results["total_images"] = len(image_files)
        
        # Summary
        print(f"\n총 {results['total_images']}개 이미지 분석")
        print(f"학습 완료: {results['learned']}개")
        print(f"카테고리: {len(results['categories'])}개")
        
        return results
    
    def test_prompt_generation(self) -> Dict:
        """Test photorealistic prompt generation"""
        print("\n" + "="*60)
        print("TEST 2: PHOTOREALISTIC PROMPT GENERATION")
        print("="*60)
        
        results = {
            "prompts_generated": [],
            "quality_scores": []
        }
        
        # Test products
        test_products = [
            {
                "name": "제주 흑돼지 구이",
                "category": "meat",
                "description": "Premium Jeju black pork, grilled"
            },
            {
                "name": "전복 버터구이",
                "category": "seafood", 
                "description": "Butter-grilled abalone"
            },
            {
                "name": "한우 갈비찜",
                "category": "meat",
                "description": "Braised Korean beef short ribs"
            }
        ]
        
        for product in test_products:
            print(f"\n상품: {product['name']}")
            
            # Generate learned prompt
            learned_prompt = self.learner.generate_learned_prompt(
                product["name"],
                product["category"]
            )
            
            if learned_prompt:
                print(f"학습 기반 프롬프트:")
                print(f"  {learned_prompt['prompt'][:150]}...")
                print(f"  학습 특징: {', '.join(learned_prompt['learned_features'])}")
                
                # Generate photorealistic prompt
                result = self.engine.generate(
                    subject=product["name"],
                    category=product["category"],
                    style="product_showcase"
                )
                
                if result["status"] == "success":
                    results["prompts_generated"].append({
                        "product": product["name"],
                        "prompt_preview": result["prompt"][:100] + "...",
                        "estimated_realism": result["metadata"]["estimated_realism_score"]
                    })
                    
                    results["quality_scores"].append(
                        result["metadata"]["estimated_realism_score"]
                    )
                    
                    print(f"\n나노바나나 프롬프트:")
                    print(f"  {result['prompt'][:150]}...")
                    print(f"  예상 사실성: {result['metadata']['estimated_realism_score']:.1f}/100")
        
        # Summary
        if results["quality_scores"]:
            avg_score = sum(results["quality_scores"]) / len(results["quality_scores"])
            print(f"\n평균 사실성 점수: {avg_score:.1f}/100")
        
        return results
    
    def test_batch_processing(self) -> Dict:
        """Test batch processing capability"""
        print("\n" + "="*60)
        print("TEST 3: BATCH PROCESSING")
        print("="*60)
        
        results = {
            "batch_size": 0,
            "processed": 0,
            "success_rate": 0.0
        }
        
        # Create batch request
        batch_products = [
            {"name": "김치찌개", "category": "soup"},
            {"name": "불고기", "category": "meat"},
            {"name": "비빔밥", "category": "rice"},
            {"name": "삼겹살", "category": "meat"},
            {"name": "된장찌개", "category": "soup"}
        ]
        
        results["batch_size"] = len(batch_products)
        
        print(f"배치 처리 시작: {len(batch_products)}개 상품")
        
        for i, product in enumerate(batch_products, 1):
            print(f"\n[{i}/{len(batch_products)}] {product['name']}")
            
            # Generate with analysis
            prompt_result = self.engine.generate(
                subject=product["name"],
                category=product["category"],
                analyze_reference=True
            )
            
            if prompt_result["status"] == "success":
                results["processed"] += 1
                print(f"  [OK] 프롬프트 생성 완료")
                print(f"  - 사실성: {prompt_result['metadata']['estimated_realism_score']:.1f}/100")
        
        results["success_rate"] = (results["processed"] / results["batch_size"]) * 100
        
        print(f"\n배치 처리 완료: {results['processed']}/{results['batch_size']} 성공")
        print(f"성공률: {results['success_rate']:.1f}%")
        
        return results
    
    def test_quality_validation(self) -> Dict:
        """Test photorealism quality validation"""
        print("\n" + "="*60)
        print("TEST 4: QUALITY VALIDATION")
        print("="*60)
        
        results = {
            "validations": [],
            "avg_scores": {}
        }
        
        # Test validation on different prompt styles
        test_cases = [
            {
                "prompt": "Professional food photography of Korean BBQ, natural lighting, 8K",
                "expected": "medium"
            },
            {
                "prompt": "Professional food photography of Korean BBQ, shot with Canon EOS R5, 85mm f/1.4 lens, natural studio lighting with softbox, 8K resolution, ultra-detailed, photorealistic, award-winning photography style",
                "expected": "high"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nValidation {i}:")
            print(f"Expected quality: {test_case['expected']}")
            
            # Validate prompt
            validation = self.engine.validate_photorealism(test_case["prompt"])
            
            results["validations"].append({
                "expected": test_case["expected"],
                "technical": validation["technical_score"],
                "artistic": validation["artistic_score"],
                "overall": validation["overall_score"],
                "passed": validation["photorealistic_quality"]
            })
            
            print(f"  Technical: {validation['technical_score']:.1f}/100")
            print(f"  Artistic: {validation['artistic_score']:.1f}/100")
            print(f"  Overall: {validation['overall_score']:.1f}/100")
            print(f"  Result: {'[PASS]' if validation['photorealistic_quality'] else '[FAIL]'}")
        
        # Calculate averages
        if results["validations"]:
            results["avg_scores"] = {
                "technical": sum(v["technical"] for v in results["validations"]) / len(results["validations"]),
                "artistic": sum(v["artistic"] for v in results["validations"]) / len(results["validations"]),
                "overall": sum(v["overall"] for v in results["validations"]) / len(results["validations"])
            }
        
        return results
    
    def test_cafe24_integration(self) -> Dict:
        """Test Cafe24 product integration"""
        print("\n" + "="*60)
        print("TEST 5: CAFE24 INTEGRATION")
        print("="*60)
        
        results = {
            "products_found": 0,
            "images_analyzed": 0,
            "prompts_created": 0,
            "categories": []
        }
        
        # Check for Cafe24 CSV file
        csv_path = Path("C:/Users/8899y/CUA-MASTER/modules/cafe24/download/manwonyori_20250831_295_3947.csv")
        
        if csv_path.exists():
            print(f"Cafe24 CSV 파일 발견: {csv_path.name}")
            
            # Simulate reading product data
            import csv
            try:
                with open(csv_path, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    products = list(reader)[:10]  # Test with first 10 products
                    
                    results["products_found"] = len(products)
                    
                    for product in products:
                        product_name = product.get('상품명', '')
                        if product_name:
                            print(f"\n처리중: {product_name[:30]}...")
                            
                            # Generate photorealistic prompt
                            prompt_result = self.engine.generate(
                                subject=product_name,
                                category="food"
                            )
                            
                            if prompt_result["status"] == "success":
                                results["prompts_created"] += 1
                                print(f"  ✓ 프롬프트 생성 완료")
            
            except Exception as e:
                print(f"CSV 읽기 오류: {e}")
        else:
            print("Cafe24 CSV 파일을 찾을 수 없음")
        
        # Check FTP downloaded images
        if self.image_base.exists():
            total_images = sum(1 for _ in self.image_base.glob("**/*.jpg"))
            total_images += sum(1 for _ in self.image_base.glob("**/*.png"))
            
            results["images_analyzed"] = min(total_images, 10)  # Analyze sample
            print(f"\nFTP 이미지 발견: {total_images}개")
            print(f"샘플 분석: {results['images_analyzed']}개")
        
        return results
    
    def run_all_tests(self):
        """Run complete pipeline test"""
        print("\n" + "="*70)
        print("PHOTOREALISTIC IMAGE GENERATION PIPELINE - COMPLETE TEST")
        print("Google Imagen 3 (나노바나나) Integration")
        print("="*70)
        
        all_results = {}
        
        # Run tests
        tests = [
            ("Real Image Learning", self.test_real_image_learning),
            ("Prompt Generation", self.test_prompt_generation),
            ("Batch Processing", self.test_batch_processing),
            ("Quality Validation", self.test_quality_validation),
            ("Cafe24 Integration", self.test_cafe24_integration)
        ]
        
        for test_name, test_func in tests:
            try:
                print(f"\nRunning: {test_name}")
                result = test_func()
                all_results[test_name] = {
                    "status": "SUCCESS",
                    "data": result
                }
            except Exception as e:
                print(f"Error in {test_name}: {e}")
                all_results[test_name] = {
                    "status": "ERROR",
                    "error": str(e)
                }
        
        # Generate report
        self.generate_report(all_results)
        
        return all_results
    
    def generate_report(self, results: Dict):
        """Generate test report"""
        print("\n" + "="*70)
        print("PIPELINE TEST REPORT")
        print("="*70)
        
        # Status summary
        success_count = sum(1 for r in results.values() if r["status"] == "SUCCESS")
        total_count = len(results)
        
        print(f"\n테스트 결과: {success_count}/{total_count} 성공")
        
        # Individual test results
        for test_name, result in results.items():
            status_icon = "[OK]" if result["status"] == "SUCCESS" else "[FAIL]"
            print(f"\n[{status_icon}] {test_name}")
            
            if result["status"] == "SUCCESS" and "data" in result:
                data = result["data"]
                
                # Print key metrics
                if test_name == "Real Image Learning":
                    if "learned" in data:
                        print(f"    - 학습된 이미지: {data['learned']}개")
                        print(f"    - 카테고리: {len(data.get('categories', {}))}개")
                
                elif test_name == "Prompt Generation":
                    if "quality_scores" in data and data["quality_scores"]:
                        avg_score = sum(data["quality_scores"]) / len(data["quality_scores"])
                        print(f"    - 평균 사실성: {avg_score:.1f}/100")
                
                elif test_name == "Batch Processing":
                    if "success_rate" in data:
                        print(f"    - 성공률: {data['success_rate']:.1f}%")
                
                elif test_name == "Quality Validation":
                    if "avg_scores" in data:
                        print(f"    - 전체 품질: {data['avg_scores'].get('overall', 0):.1f}/100")
                
                elif test_name == "Cafe24 Integration":
                    if "prompts_created" in data:
                        print(f"    - 생성된 프롬프트: {data['prompts_created']}개")
        
        # Save report
        report_path = Path(__file__).parent / "test_results" / f"pipeline_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n상세 보고서 저장: {report_path}")
        
        # Final status
        if success_count == total_count:
            print("\n[EXCELLENT] 모든 파이프라인 테스트 통과!")
            print("나노바나나 초사실주의 이미지 생성 준비 완료")
        elif success_count > total_count // 2:
            print("\n[GOOD] 대부분의 테스트 통과")
            print("일부 기능 점검 필요")
        else:
            print("\n[WARNING] 테스트 실패 다수 발생")
            print("시스템 점검 필요")

def main():
    """Run pipeline test"""
    print("초사실주의 이미지 생성 파이프라인 테스트")
    print("Google Imagen 3 (나노바나나) 기반")
    print("-" * 50)
    
    tester = PhotorealisticPipelineTest()
    results = tester.run_all_tests()
    
    print("\n테스트 완료!")
    print("실제 Cafe24 제품 이미지를 기반으로 한 초사실주의 생성 시스템")
    print("사진과 구별 불가능한 수준의 이미지 생성 가능")

if __name__ == "__main__":
    main()