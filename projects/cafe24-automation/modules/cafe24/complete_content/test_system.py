"""시스템 테스트 스크립트"""

import sys
from pathlib import Path

# 경로 설정
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content')

def test_imports():
    """모든 import 테스트"""
    print("\n[Import Test]")
    print("-" * 40)
    
    try:
        from cafe24_bridge_integration import Cafe24BridgeIntegration
        print("  [OK] Cafe24BridgeIntegration")
    except Exception as e:
        print(f"  [ERROR] Cafe24BridgeIntegration: {e}")
    
    try:
        from ultimate_image_workflow import UltimateImageWorkflow
        print("  [OK] UltimateImageWorkflow")
    except Exception as e:
        print(f"  [ERROR] UltimateImageWorkflow: {e}")
    
    try:
        from complete_detail_page_system import CompleteDetailPageSystem
        print("  [OK] CompleteDetailPageSystem")
    except Exception as e:
        print(f"  [ERROR] CompleteDetailPageSystem: {e}")
    
    try:
        from claude_bridge_template_system import ClaudeBridgeTemplateSystem
        print("  [OK] ClaudeBridgeTemplateSystem")
    except Exception as e:
        print(f"  [ERROR] ClaudeBridgeTemplateSystem: {e}")
    
    try:
        from ftp_image_upload_system import FTPImageUploadSystem
        print("  [OK] FTPImageUploadSystem")
    except Exception as e:
        print(f"  [ERROR] FTPImageUploadSystem: {e}")
    
    try:
        from html_design_optimizer import HtmlDesignOptimizer
        print("  [OK] HtmlDesignOptimizer")
    except Exception as e:
        print(f"  [ERROR] HtmlDesignOptimizer: {e}")
    
    try:
        from html_image_integration import HtmlImageIntegration
        print("  [OK] HtmlImageIntegration")
    except Exception as e:
        print(f"  [ERROR] HtmlImageIntegration: {e}")
    
    try:
        from image_size_optimizer import ImageSizeOptimizer
        print("  [OK] ImageSizeOptimizer")
    except Exception as e:
        print(f"  [ERROR] ImageSizeOptimizer: {e}")

def test_files():
    """파일 존재 확인"""
    print("\n[File Check]")
    print("-" * 40)
    
    base_path = Path(r"C:\Users\8899y\CUA-MASTER\modules\cafe24\complete_content")
    
    # TXT 파일 확인
    txt_path = base_path / "html" / "temp_txt"
    if txt_path.exists():
        txt_files = list(txt_path.glob("*.txt"))
        print(f"  TXT Files: {len(txt_files)} files found")
    else:
        print(f"  TXT Path not found: {txt_path}")
    
    # 대표이미지 폴더 확인
    rep_path = base_path / "representative_images"
    if rep_path.exists():
        rep_files = list(rep_path.glob("*.jpg"))
        print(f"  Representative Images: {len(rep_files)} files")
    else:
        print(f"  Representative folder will be created at: {rep_path}")
    
    # Output 폴더 확인
    output_path = base_path / "output"
    if output_path.exists():
        output_files = list(output_path.rglob("*.*"))
        print(f"  Output Files: {len(output_files)} files")
    else:
        print(f"  Output folder will be created at: {output_path}")

def main():
    print("\n" + "="*50)
    print("CAFE24 COMPLETE CONTENT - SYSTEM TEST")
    print("="*50)
    
    # Import 테스트
    test_imports()
    
    # 파일 테스트
    test_files()
    
    print("\n" + "="*50)
    print("[Test Complete]")
    print("="*50)

if __name__ == "__main__":
    main()