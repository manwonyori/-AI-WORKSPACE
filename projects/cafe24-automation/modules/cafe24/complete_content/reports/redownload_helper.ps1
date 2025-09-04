# Cafe24 재다운로드 도우미
# 생성일: 2025-09-01 18:28:13

$products = @(
    @{No="143"; Name="[최씨남매]돼지김치찜 650g"},
    @{No="146"; Name="[BS]연평도 간장게장2.5kg"},
    @{No="147"; Name="[피자코리아] 무료배송 포카치아 피자 4종  비프불고기 애플고르곤졸라 콰트로치즈 김치불고기 20개 구성 세트 [ 총 1,450g ]"},
    @{No="46"; Name="[반찬단지]실속메추리알장조림 1kg"},
    @{No="51"; Name="[반찬단지]고추무침 1kg"},
    @{No="73"; Name="[반찬단지]입맛 돋우는 젓갈 3종 세트[낙지젓pe200+오징어젓pe200+씨앗젓갈200g]"},
    @{No="76"; Name="[반찬단지]간장깻잎 1kg"}
)

Write-Host "======================================"
Write-Host "   Cafe24 재다운로드 도우미"
Write-Host "======================================"
Write-Host ""
Write-Host "재다운로드할 상품 목록:"
Write-Host ""

foreach ($product in $products) {
    Write-Host ("상품번호: " + $product.No + " - " + $product.Name)
}

Write-Host ""
Write-Host "위 상품들을 Cafe24 관리자에서 다운로드하세요."
Write-Host ""
Write-Host "다운로드 방법:"
Write-Host "1. 상품번호로 검색"
Write-Host "2. 상품 수정 페이지 진입"
Write-Host "3. 상세설명 HTML 복사"
Write-Host "4. html/temp_txt/상품번호.txt로 저장"
Write-Host ""

$openBrowser = Read-Host "Cafe24 관리자를 열까요? (Y/N)"
if ($openBrowser -eq 'Y') {
    Start-Process "https://manwonyori.cafe24.com/admin/product/product_search.html"
}

Write-Host ""
Write-Host "완료되면 Enter를 누르세요..."
Read-Host
