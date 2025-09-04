// 포토샵 자동화 JSX 스크립트
// Adobe Photoshop 2024 호환

// 1. 새 문서 생성
function createNewDocument(width, height, resolution) {
    var doc = app.documents.add(
        UnitValue(width, "px"),
        UnitValue(height, "px"), 
        resolution,
        "자동생성문서",
        NewDocumentMode.RGB,
        DocumentFill.WHITE
    );
    return doc;
}

// 2. 텍스트 레이어 추가
function addTextLayer(document, text, x, y, fontSize) {
    var textLayer = document.artLayers.add();
    textLayer.kind = LayerKind.TEXT;
    textLayer.name = "자동텍스트";
    
    var textItem = textLayer.textItem;
    textItem.contents = text;
    textItem.position = [UnitValue(x, "px"), UnitValue(y, "px")];
    textItem.size = UnitValue(fontSize, "px");
    textItem.color = new SolidColor();
    textItem.color.rgb.red = 0;
    textItem.color.rgb.green = 0;
    textItem.color.rgb.blue = 0;
    
    return textLayer;
}

// 3. 이미지 파일 열기
function openImageFile(filePath) {
    var file = new File(filePath);
    if (file.exists) {
        var doc = app.open(file);
        return doc;
    } else {
        alert("파일을 찾을 수 없습니다: " + filePath);
        return null;
    }
}

// 4. 이미지 리사이즈
function resizeImage(document, newWidth, newHeight) {
    document.resizeImage(
        UnitValue(newWidth, "px"),
        UnitValue(newHeight, "px"),
        null,
        ResampleMethod.BICUBIC
    );
}

// 5. 파일 저장 (JPEG)
function saveAsJPEG(document, filePath, quality) {
    var saveFile = new File(filePath);
    var jpegOptions = new JPEGSaveOptions();
    jpegOptions.quality = quality; // 1-12 (12가 최고 품질)
    jpegOptions.embedColorProfile = true;
    jpegOptions.formatOptions = FormatOptions.STANDARDBASELINE;
    jpegOptions.matte = MatteType.NONE;
    
    document.saveAs(saveFile, jpegOptions, true);
}

// 6. 파일 저장 (PNG)
function saveAsPNG(document, filePath) {
    var saveFile = new File(filePath);
    var pngOptions = new PNGSaveOptions();
    pngOptions.compression = 6;
    pngOptions.interlaced = false;
    
    document.saveAs(saveFile, pngOptions, true);
}

// 7. 워터마크 추가
function addWatermark(document, watermarkText, opacity) {
    var watermarkLayer = addTextLayer(document, watermarkText, 50, 50, 24);
    watermarkLayer.opacity = opacity; // 0-100
    watermarkLayer.blendMode = BlendMode.OVERLAY;
}

// 8. 일괄 처리 메인 함수
function batchProcess() {
    try {
        // 새 문서 생성 (1920x1080)
        var doc = createNewDocument(1920, 1080, 72);
        
        // 텍스트 추가
        addTextLayer(doc, "Claude 자동화 테스트", 100, 100, 48);
        
        // 워터마크 추가
        addWatermark(doc, "© 2025 CUA System", 30);
        
        // 저장 경로 설정
        var savePath = "C:/Users/8899y/CUA-MASTER/output/auto_generated.jpg";
        
        // JPEG로 저장
        saveAsJPEG(doc, savePath, 10);
        
        alert("자동화 작업 완료!\n저장 위치: " + savePath);
        
        // 문서 닫기
        doc.close(SaveOptions.DONOTSAVECHANGES);
        
    } catch (error) {
        alert("오류 발생: " + error.message);
    }
}

// 스크립트 실행
batchProcess();
