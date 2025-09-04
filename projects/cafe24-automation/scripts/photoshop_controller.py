"""
포토샵 자동화 Python 컨트롤러
JSX 스크립트와 UI 자동화를 결합한 통합 솔루션
"""

import os
import time
import subprocess
from pathlib import Path

class PhotoshopAutomation:
    def __init__(self):
        self.script_dir = Path("C:/Users/8899y/CUA-MASTER/scripts")
        self.output_dir = Path("C:/Users/8899y/CUA-MASTER/output")
        self.jsx_scripts = {
            'basic': self.script_dir / 'photoshop_automation.jsx',
            'batch': self.script_dir / 'batch_image_process.jsx'
        }
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(exist_ok=True)
    
    def run_jsx_script(self, script_name):
        """JSX 스크립트 실행"""
        if script_name not in self.jsx_scripts:
            raise ValueError(f"스크립트 '{script_name}'를 찾을 수 없습니다.")
        
        script_path = self.jsx_scripts[script_name]
        if not script_path.exists():
            raise FileNotFoundError(f"스크립트 파일이 없습니다: {script_path}")
        
        # 포토샵이 실행중인지 확인
        try:
            # JSX 스크립트 실행 명령어 (Windows)
            cmd = f'start "" "{script_path}"'
            subprocess.run(cmd, shell=True, check=True)
            print(f"스크립트 실행 완료: {script_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"스크립트 실행 실패: {e}")
            return False
    
    def create_custom_jsx(self, template_name, **kwargs):
        """동적 JSX 스크립트 생성"""
        templates = {
            'resize_batch': '''
            // 동적 리사이즈 스크립트
            var inputFolder = new Folder("{input_path}");
            var outputFolder = new Folder("{output_path}");
            var newWidth = {width};
            var newHeight = {height};
            var quality = {quality};
            
            var files = inputFolder.getFiles("*.jpg");
            for (var i = 0; i < files.length; i++) {{
                var doc = app.open(files[i]);
                doc.resizeImage(UnitValue(newWidth, "px"), UnitValue(newHeight, "px"));
                
                var saveFile = new File(outputFolder + "/" + files[i].name);
                var jpegOptions = new JPEGSaveOptions();
                jpegOptions.quality = quality;
                doc.saveAs(saveFile, jpegOptions, true);
                doc.close(SaveOptions.DONOTSAVECHANGES);
            }}
            alert("배치 리사이즈 완료!");
            ''',
            
            'add_logo': '''
            // 로고 추가 스크립트
            var logoPath = "{logo_path}";
            var inputFolder = new Folder("{input_path}");
            var outputFolder = new Folder("{output_path}");
            
            var logoFile = new File(logoPath);
            var files = inputFolder.getFiles("*.jpg");
            
            for (var i = 0; i < files.length; i++) {{
                var doc = app.open(files[i]);
                
                // 로고 파일 열기
                var logoDoc = app.open(logoFile);
                logoDoc.selection.selectAll();
                logoDoc.selection.copy();
                logoDoc.close(SaveOptions.DONOTSAVECHANGES);
                
                // 메인 문서에 붙여넣기
                doc.paste();
                var logoLayer = doc.activeLayer;
                logoLayer.opacity = {opacity};
                logoLayer.move(doc.layers[doc.layers.length - 1], ElementPlacement.PLACEAFTER);
                
                var saveFile = new File(outputFolder + "/" + files[i].name);
                var jpegOptions = new JPEGSaveOptions();
                jpegOptions.quality = 10;
                doc.saveAs(saveFile, jpegOptions, true);
                doc.close(SaveOptions.DONOTSAVECHANGES);
            }}
            alert("로고 추가 완료!");
            '''
        }
        
        if template_name not in templates:
            raise ValueError(f"템플릿 '{template_name}'를 찾을 수 없습니다.")
        
        script_content = templates[template_name].format(**kwargs)
        
        # 동적 스크립트 파일 저장
        dynamic_script_path = self.script_dir / f"dynamic_{template_name}.jsx"
        with open(dynamic_script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return dynamic_script_path
    
    def batch_resize_images(self, input_path, output_path, width=1920, height=1080, quality=10):
        """이미지 일괄 리사이즈"""
        script_path = self.create_custom_jsx('resize_batch',
                                           input_path=input_path.replace('\\', '/'),
                                           output_path=output_path.replace('\\', '/'),
                                           width=width,
                                           height=height,
                                           quality=quality)
        
        # JSX 스크립트 실행
        cmd = f'start "" "{script_path}"'
        subprocess.run(cmd, shell=True)
        print(f"배치 리사이즈 시작 - {input_path} → {output_path}")
    
    def add_watermark_batch(self, input_path, output_path, watermark_text="© CUA System", opacity=30):
        """워터마크 일괄 추가"""
        watermark_jsx = f'''
        var inputFolder = new Folder("{input_path.replace(chr(92), '/')}");
        var outputFolder = new Folder("{output_path.replace(chr(92), '/')}");
        var watermarkText = "{watermark_text}";
        var opacity = {opacity};
        
        var files = inputFolder.getFiles("*.jpg");
        for (var i = 0; i < files.length; i++) {{
            var doc = app.open(files[i]);
            
            var textLayer = doc.artLayers.add();
            textLayer.kind = LayerKind.TEXT;
            textLayer.name = "워터마크";
            
            var textItem = textLayer.textItem;
            textItem.contents = watermarkText;
            textItem.position = [UnitValue(50, "px"), UnitValue(doc.height.as("px") - 50, "px")];
            textItem.size = UnitValue(24, "px");
            textItem.color = new SolidColor();
            textItem.color.rgb.red = 255;
            textItem.color.rgb.green = 255;
            textItem.color.rgb.blue = 255;
            
            textLayer.opacity = opacity;
            textLayer.blendMode = BlendMode.OVERLAY;
            
            var saveFile = new File(outputFolder + "/" + files[i].name);
            var jpegOptions = new JPEGSaveOptions();
            jpegOptions.quality = 10;
            doc.saveAs(saveFile, jpegOptions, true);
            doc.close(SaveOptions.DONOTSAVECHANGES);
        }}
        alert("워터마크 추가 완료!");
        '''
        
        # 스크립트 파일 생성 및 실행
        script_path = self.script_dir / "watermark_batch.jsx"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(watermark_jsx)
        
        cmd = f'start "" "{script_path}"'
        subprocess.run(cmd, shell=True)
        print(f"워터마크 배치 작업 시작")

# 사용 예시
if __name__ == "__main__":
    ps = PhotoshopAutomation()
    
    # 1. 기본 스크립트 실행
    print("1. 기본 자동화 스크립트 실행")
    ps.run_jsx_script('basic')
    
    # 2. 배치 처리 스크립트 실행
    # ps.run_jsx_script('batch')
    
    # 3. 동적 스크립트 생성 및 실행
    # input_folder = "C:/Users/8899y/CUA-MASTER/data/images"
    # output_folder = "C:/Users/8899y/CUA-MASTER/output/resized"
    # ps.batch_resize_images(input_folder, output_folder, 800, 600)
    
    print("포토샵 자동화 작업 완료")
