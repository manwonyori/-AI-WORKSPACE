"""
통합 발주 시스템 테스트
CCW와 만원요리 발주서 모두 처리
"""

from src.adaptive_order_system import AdaptiveOrderSystem
from pathlib import Path
import json

def main():
    print("=" * 60)
    print(" 통합 발주 시스템 테스트")
    print("=" * 60)
    
    # 시스템 초기화
    system = AdaptiveOrderSystem()
    
    # 테스트 파일
    test_files = [
        {
            "path": "tests/ccw 발주.xlsx",
            "name": "CCW B2B 발주서",
            "expected_format": "ccw_b2b"
        }
    ]
    
    results = []
    
    for test_file in test_files:
        file_path = Path(test_file["path"])
        
        if file_path.exists():
            print(f"\n[{test_file['name']} 처리]")
            print("-" * 40)
            
            # 발주서 처리
            order = system.process_order_file(str(file_path))
            
            if order:
                # 결과 저장
                saved_file = system.save_unified_order(order)
                
                # 요약
                result = {
                    "name": test_file["name"],
                    "status": "성공",
                    "format": order.format_type,
                    "total_items": len(order.items),
                    "total_quantity": sum(item.quantity for item in order.items),
                    "total_amount": sum(item.total_price for item in order.items),
                    "saved_file": str(saved_file)
                }
                
                print(f"\n결과 요약:")
                print(f"  상태: {result['status']}")
                print(f"  형식: {result['format']}")
                print(f"  품목수: {result['total_items']}")
                print(f"  총수량: {result['total_quantity']:.0f}")
                print(f"  총금액: {result['total_amount']:,.0f}원")
                
                # 상위 5개 품목
                print(f"\n주요 품목 (상위 5개):")
                for i, item in enumerate(order.items[:5], 1):
                    print(f"  {i}. {item.product_name}")
                    print(f"     수량: {item.quantity:.0f}, 단가: {item.unit_price:,.0f}원")
                
                results.append(result)
            else:
                results.append({
                    "name": test_file["name"],
                    "status": "실패",
                    "error": "파싱 오류"
                })
        else:
            print(f"\n파일을 찾을 수 없음: {file_path}")
            results.append({
                "name": test_file["name"],
                "status": "실패",
                "error": "파일 없음"
            })
    
    # 최종 결과 출력
    print("\n" + "=" * 60)
    print(" 테스트 결과 요약")
    print("=" * 60)
    
    for result in results:
        print(f"\n{result['name']}:")
        print(f"  상태: {result['status']}")
        if result['status'] == "성공":
            print(f"  품목: {result['total_items']}개")
            print(f"  금액: {result.get('total_amount', 0):,.0f}원")
    
    # 결과 저장
    output_file = Path("data/test_results/test_summary.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n테스트 결과 저장: {output_file}")

if __name__ == "__main__":
    main()