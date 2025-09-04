// 이미지 일괄 처리 스크립트
// 특정 폴더의 모든 이미지를 자동으로 리사이즈하고 워터마크 추가

function batchImageProcess() {
    // 입력 폴더 선택
    var inputFolder = Folder.selectDialog("처리할 이미지가 있는 폴더를 선택하세요");
    if (!inputFolder) return;
    
    // 출력 폴더 선택
    var outputFolder = Folder.selectDialog("결과를 저장할 폴더를 선택하세요");
    if (!outputFolder) return;
    
    // 이미지 파일 필터
    var imageFiles = [];
    var files = inputFolder.getFiles();
    
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (file instanceof File) {
            var fileName = file.name.toLowerCase();
            if (fileName.match(/\.(jpg|jpeg|png|tif|tiff|bmp)$/)) {
                imageFiles.push(file);
            }
        }
    }
    
    if (imageFiles.length === 0) {
        alert("처리할 이미지 파일이 없습니다.");
        return;
    }
    
    // 처리 설정
    var settings = {
        newWidth: 1920,
        newHeight: 1080,
        quality: 10,
        watermarkText: "© CUA System",
        watermarkOpacity: 25
    };
    
    // 진행률 표시를 위한 변수
    var processed = 0;
    var total = imageFiles.length;
    
    try {
        for (var i = 0; i < imageFiles.length; i++) {
            var inputFile = imageFiles[i];
            
            // 파일 열기
            var doc = app.open(inputFile);
            
            // 리사이즈 (비율 유지)
            var originalWidth = doc.width.as("px");
            var originalHeight = doc.height.as("px");
            var ratio = Math.min(settings.newWidth / originalWidth, settings.newHeight / originalHeight);
            
            doc.resizeImage(
                UnitValue(originalWidth * ratio, "px"),
                UnitValue(originalHeight * ratio, "px"),
                null,
                ResampleMethod.BICUBIC
            );
            
            // 캔버스 크기 조정 (중앙 정렬)
            doc.resizeCanvas(
                UnitValue(settings.newWidth, "px"),
                UnitValue(settings.newHeight, "px"),
                AnchorPosition.MIDDLECENTER
            );
            
            // 워터마크 추가
            if (settings.watermarkText) {
                var watermarkLayer = doc.artLayers.add();
                watermarkLayer.kind = LayerKind.TEXT;
                watermarkLayer.name = "워터마크";
                
                var textItem = watermarkLayer.textItem;
                textItem.contents = settings.watermarkText;
                textItem.position = [UnitValue(50, "px"), UnitValue(settings.newHeight - 50, "px")];
                textItem.size = UnitValue(24, "px");
                textItem.color = new SolidColor();
                textItem.color.rgb.red = 255;
                textItem.color.rgb.green = 255;
                textItem.color.rgb.blue = 255;
                
                watermarkLayer.opacity = settings.watermarkOpacity;
                watermarkLayer.blendMode = BlendMode.OVERLAY;
            }
            
            // 저장할 파일명 생성
            var baseName = inputFile.name.replace(/\.[^\.]+$/, "");
            var outputFile = new File(outputFolder + "/" + baseName + "_processed.jpg");
            
            // JPEG로 저장
            var jpegOptions = new JPEGSaveOptions();
            jpegOptions.quality = settings.quality;
            jpegOptions.embedColorProfile = true;
            jpegOptions.formatOptions = FormatOptions.STANDARDBASELINE;
            
            doc.saveAs(outputFile, jpegOptions, true);
            
            // 문서 닫기
            doc.close(SaveOptions.DONOTSAVECHANGES);
            
            processed++;
            
            // 진행률 업데이트 (매 10개마다)
            if (processed % 10 === 0 || processed === total) {
                app.refresh();
            }
        }
        
        alert("배치 처리 완료!\n처리된 파일: " + processed + "개\n저장 위치: " + outputFolder.fsName);
        
    } catch (error) {
        alert("배치 처리 중 오류 발생:\n" + error.message + "\n\n처리 완료: " + processed + "/" + total);
    }
}

// 스크립트 실행
batchImageProcess();
