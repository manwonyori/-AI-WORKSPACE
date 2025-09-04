"""
품질 검수 시스템
- 중복 내용 검출 및 제거
- 알레르기 정보 중복 제거
- 전체적인 콘텐츠 품질 검증
"""

import os
import re
from pathlib import Path
from collections import Counter
import json

class QualityChecker:
    def __init__(self):
        """품질 검수기 초기화"""
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
        self.output_path = self.base_path / "output" / "content_only"
        
        # 중복 검출 패턴
        self.duplicate_patterns = [
            r'<!-- 영양성분 및 알레르기 정보.*?(?=<!-- [^영양]|</div>\s*</body>)',
            r'<h2 class="section-title">영양성분.*?</div>',
            r'알레르기.*?요소.*?함유',
            r'보관.*?주의사항'
        ]
        
    def find_duplicate_sections(self, content):
        """중복 섹션 찾기"""
        duplicates = []
        
        # 영양성분 섹션 중복 체크
        nutrition_sections = re.findall(r'<!-- 영양성분 및 알레르기 정보.*?(?=<!--|\n\s*</div>)', content, re.DOTALL)
        if len(nutrition_sections) > 1:
            duplicates.append({
                'type': '영양성분 섹션 중복',
                'count': len(nutrition_sections),
                'locations': [content.find(section) for section in nutrition_sections]
            })
        
        # 알레르기 정보 중복 체크
        allergy_sections = re.findall(r'알레르기.*?정보.*?</div>', content, re.DOTALL | re.IGNORECASE)
        if len(allergy_sections) > 1:
            duplicates.append({
                'type': '알레르기 정보 중복',
                'count': len(allergy_sections),
                'sections': allergy_sections
            })
        
        return duplicates
    
    def extract_allergens(self, content):
        """알레르기 요소 추출 및 중복 체크"""
        allergens = []
        
        # 알레르기 스팬 태그에서 추출
        span_allergens = re.findall(r'<span[^>]*>[^<]*?(밀|대두|돼지고기|새우|계란|우유|견과류|참깨)[^<]*?</span>', content, re.IGNORECASE)
        allergens.extend(span_allergens)
        
        # 텍스트에서 알레르기 요소 추출
        text_allergens = re.findall(r'(밀|대두|돼지고기|새우|계란|우유|견과류|참깨)', content)
        allergens.extend(text_allergens)
        
        # 중복 제거 및 카운트
        allergen_count = Counter(allergens)
        duplicated_allergens = {allergen: count for allergen, count in allergen_count.items() if count > 3}  # 3번 이상 나오면 중복으로 판단
        
        return list(set(allergens)), duplicated_allergens
    
    def clean_duplicate_allergens(self, content):
        """중복된 알레르기 정보 정리"""
        # 알레르기 스팬 태그들 찾기
        allergen_spans = re.findall(r'<span[^>]*background[^>]*>[^<]*?(밀|대두|돼지고기|새우|계란|우유|견과류|참깨)[^<]*?</span>', content, re.IGNORECASE)
        
        if len(allergen_spans) > 0:
            # 중복 제거된 알레르기 리스트 생성
            unique_allergens = []
            seen_allergens = set()
            
            for span in allergen_spans:
                allergen_match = re.search(r'(밀|대두|돼지고기|새우|계란|우유|견과류|참깨)', span)
                if allergen_match:
                    allergen = allergen_match.group(1)
                    if allergen not in seen_allergens:
                        unique_allergens.append(allergen)
                        seen_allergens.add(allergen)
            
            # 새로운 알레르기 스팬 HTML 생성
            new_allergen_html = ""
            for allergen in unique_allergens:
                new_allergen_html += f'\n                <span style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 8px 16px; border-radius: 25px; font-size: 14px; font-weight: 600; box-shadow: 0 2px 4px rgba(220,53,69,0.3);">{allergen}</span>'
            
            # 기존 알레르기 스팬들을 새것으로 교체
            pattern = r'(<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 15px;">).*?(</div>)'
            replacement = r'\1' + new_allergen_html + r'\n            \2'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        return content
    
    def remove_duplicate_sections(self, content):
        """중복 섹션 제거"""
        # 영양성분 섹션이 여러 개 있다면 첫 번째만 남기고 제거
        nutrition_pattern = r'<!-- 영양성분 및 알레르기 정보.*?(?=<!-- [^영양]|</div>\s*</body>|\n\s*<!-- 판매자)'
        nutrition_matches = list(re.finditer(nutrition_pattern, content, re.DOTALL))
        
        if len(nutrition_matches) > 1:
            # 첫 번째를 제외한 나머지 제거
            for match in reversed(nutrition_matches[1:]):  # 뒤에서부터 제거
                content = content[:match.start()] + content[match.end():]
            
            print(f"    [정리] {len(nutrition_matches)-1}개 중복 영양성분 섹션 제거")
        
        return content
    
    def check_content_quality(self, content):
        """콘텐츠 전반적인 품질 체크"""
        quality_issues = []
        
        # 1. 빈 태그 체크
        empty_tags = re.findall(r'<(\w+)[^>]*>\s*</\1>', content)
        if empty_tags:
            quality_issues.append(f"빈 태그 발견: {set(empty_tags)}")
        
        # 2. 깨진 이미지 링크 체크
        img_links = re.findall(r'<img[^>]*src=["\']([^"\']*)["\']', content)
        broken_links = [link for link in img_links if 'placeholder' in link]
        if broken_links:
            quality_issues.append(f"플레이스홀더 이미지: {len(broken_links)}개")
        
        # 3. 텍스트 길이 체크
        text_content = re.sub(r'<[^>]+>', '', content)
        if len(text_content.strip()) < 1000:
            quality_issues.append("콘텐츠 길이가 너무 짧음")
        
        # 4. 필수 섹션 체크
        required_sections = ['상품설명', '상세정보', '영양성분', '판매자 정보']
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            quality_issues.append(f"누락된 섹션: {missing_sections}")
        
        return quality_issues
    
    def generate_quality_report(self, product_number, duplicates, allergens, duplicate_allergens, quality_issues, file_size):
        """품질 리포트 생성"""
        report = {
            'product_number': product_number,
            'timestamp': str(Path().resolve()),
            'file_size_kb': round(file_size / 1024, 2),
            'duplicate_sections': duplicates,
            'allergens': {
                'total_unique': len(allergens),
                'list': allergens,
                'duplicated': duplicate_allergens
            },
            'quality_issues': quality_issues,
            'score': self._calculate_quality_score(duplicates, quality_issues, duplicate_allergens),
            'status': 'PASS' if len(duplicates) == 0 and len(quality_issues) == 0 else 'NEEDS_REVIEW'
        }
        
        return report
    
    def _calculate_quality_score(self, duplicates, quality_issues, duplicate_allergens):
        """품질 점수 계산 (100점 만점)"""
        score = 100
        
        # 중복 섹션 감점
        score -= len(duplicates) * 15
        
        # 품질 이슈 감점
        score -= len(quality_issues) * 10
        
        # 중복 알레르기 감점
        score -= len(duplicate_allergens) * 5
        
        return max(0, score)
    
    def check_and_fix_file(self, file_path):
        """단일 파일 검수 및 수정"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            print(f"\n[검수중] {file_path.name}")
            
            # 1. 중복 섹션 찾기
            duplicates = self.find_duplicate_sections(original_content)
            if duplicates:
                print(f"    [발견] 중복 섹션: {len(duplicates)}개")
                for dup in duplicates:
                    print(f"      - {dup['type']}: {dup['count']}회")
            
            # 2. 알레르기 정보 분석
            allergens, duplicate_allergens = self.extract_allergens(original_content)
            if duplicate_allergens:
                print(f"    [발견] 중복 알레르기: {duplicate_allergens}")
            
            # 3. 품질 이슈 체크
            quality_issues = self.check_content_quality(original_content)
            if quality_issues:
                print(f"    [발견] 품질 이슈: {len(quality_issues)}개")
                for issue in quality_issues:
                    print(f"      - {issue}")
            
            # 4. 수정 작업
            fixed_content = original_content
            
            # 중복 섹션 제거
            if duplicates:
                fixed_content = self.remove_duplicate_sections(fixed_content)
            
            # 중복 알레르기 정보 정리
            if duplicate_allergens:
                fixed_content = self.clean_duplicate_allergens(fixed_content)
            
            # 5. 수정된 내용을 새 파일로 저장
            if fixed_content != original_content:
                reviewed_file = file_path.with_name(file_path.stem + "_reviewed.html")
                with open(reviewed_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"    [수정완료] {reviewed_file}")
            else:
                print(f"    [완료] 수정 필요 없음")
            
            # 6. 품질 리포트 생성
            file_size = len(fixed_content.encode('utf-8'))
            report = self.generate_quality_report(
                file_path.stem, duplicates, allergens, duplicate_allergens, quality_issues, file_size
            )
            
            print(f"    [품질점수] {report['score']}/100 - {report['status']}")
            
            return report
            
        except Exception as e:
            print(f"    [ERROR] 검수 실패: {e}")
            return None
    
    def review_all_files(self, pattern="*_final_complete.html"):
        """모든 파일 검수"""
        print("=" * 60)
        print("콘텐츠 품질 검수 시작")
        print("=" * 60)
        
        files = list(self.output_path.glob(pattern))
        if not files:
            print("검수할 파일이 없습니다.")
            return
        
        all_reports = []
        
        for file_path in files:
            report = self.check_and_fix_file(file_path)
            if report:
                all_reports.append(report)
        
        # 전체 리포트 저장
        summary_report = {
            'total_files': len(all_reports),
            'passed_files': len([r for r in all_reports if r['status'] == 'PASS']),
            'average_score': sum(r['score'] for r in all_reports) / len(all_reports) if all_reports else 0,
            'reports': all_reports
        }
        
        report_file = self.output_path / f"quality_report_{pattern.replace('*', 'all').replace('.html', '')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(summary_report, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("검수 완료 요약")
        print("=" * 60)
        print(f"총 파일 수: {summary_report['total_files']}")
        print(f"통과 파일 수: {summary_report['passed_files']}")
        print(f"평균 품질 점수: {summary_report['average_score']:.1f}/100")
        print(f"상세 리포트: {report_file}")
        
        return summary_report

if __name__ == "__main__":
    checker = QualityChecker()
    checker.review_all_files()