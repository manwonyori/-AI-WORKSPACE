@echo off
chcp 65001 >nul
echo.
echo =====================================
echo   사업자등록증 이미지 업로드
echo =====================================
echo.
echo 이미지를 다음 폴더에 저장해주세요:
echo.
echo 📁 C:\Users\8899y\mart-project\data\images\pending
echo.
echo 폴더 열기...
explorer "C:\Users\8899y\mart-project\data\images\pending"
echo.
echo 이미지를 저장한 후 Enter를 눌러주세요...
pause >nul
echo.
echo 처리를 시작합니다...
python process_business_license.py
pause