"""
실제 이미지 기반 학습 시스템
Cafe24 FTP에서 다운로드한 실제 상품 이미지를 분석하여 초사실주의 프롬프트 생성
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import logging
from datetime import datetime
from sklearn.cluster import KMeans
from collections import defaultdict
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ImageFeatures:
    """이미지 특징 데이터클래스"""
    file_path: str
    product_name: str
    category: str
    
    # 기술적 특성
    resolution: Tuple[int, int]
    aspect_ratio: float
    file_size: int
    
    # 시각적 특성
    brightness: float
    contrast: float
    saturation: float
    sharpness: float
    
    # 색상 특성
    dominant_colors: List[Tuple[int, int, int]]
    color_palette: str
    
    # 구성 특성
    edge_density: float
    texture_complexity: float
    focus_area: str
    
    # 조명 특성
    lighting_type: str
    shadow_intensity: float
    highlight_intensity: float
    
    # 카메라 설정 추정
    estimated_focal_length: str
    estimated_aperture: str
    depth_of_field: str

class RealImageLearner:
    """실제 이미지 학습 시스템"""
    
    def __init__(self):
        self.base_path = Path("C:/Users/8899y/CUA-MASTER/modules")
        self.cafe24_images = self.base_path / "cafe24/ftp_mirror/download/web/product"
        self.learning_db_path = self.base_path / "ai-image-studio/learning/image_features.json"
        self.prompt_templates_path = self.base_path / "ai-image-studio/learning/prompt_templates.json"
        
        self.features_db = []
        self.prompt_templates = {}
        
        self.setup_directories()
        self.load_database()
    
    def setup_directories(self):
        """디렉토리 설정"""
        os.makedirs(self.base_path / "ai-image-studio/learning", exist_ok=True)
        os.makedirs(self.base_path / "ai-image-studio/learning/analysis", exist_ok=True)
        os.makedirs(self.base_path / "ai-image-studio/learning/patterns", exist_ok=True)
    
    def load_database(self):
        """학습 데이터베이스 로드"""
        if os.path.exists(self.learning_db_path):
            with open(self.learning_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.features_db = data.get('features', [])
                logger.info(f"기존 데이터베이스 로드: {len(self.features_db)}개 이미지")
        
        if os.path.exists(self.prompt_templates_path):
            with open(self.prompt_templates_path, 'r', encoding='utf-8') as f:
                self.prompt_templates = json.load(f)
    
    def save_database(self):
        """학습 데이터베이스 저장"""
        with open(self.learning_db_path, 'w', encoding='utf-8') as f:
            json.dump({
                'features': self.features_db,
                'updated': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        with open(self.prompt_templates_path, 'w', encoding='utf-8') as f:
            json.dump(self.prompt_templates, f, indent=2, ensure_ascii=False)
    
    def extract_image_features(self, image_path: str) -> Optional[ImageFeatures]:
        """이미지에서 특징 추출"""
        try:
            # 이미지 로드
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # 파일 정보
            file_path = Path(image_path)
            category = file_path.parent.name
            product_name = file_path.stem.replace('-', ' ').replace('_', ' ')
            
            # 기본 특성
            height, width = img.shape[:2]
            file_size = os.path.getsize(image_path)
            
            # 색상 공간 변환
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            
            # 밝기 분석
            brightness = np.mean(lab[:,:,0])
            
            # 대비 분석
            contrast = np.std(gray)
            
            # 채도 분석
            saturation = np.mean(hsv[:,:,1])
            
            # 선명도 분석 (Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            
            # 주요 색상 추출 (K-means)
            dominant_colors = self.extract_dominant_colors(img, n_colors=5)
            
            # 색상 팔레트 분류
            color_palette = self.classify_color_palette(dominant_colors)
            
            # 엣지 밀도
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (height * width)
            
            # 텍스처 복잡도
            texture_complexity = self.calculate_texture_complexity(gray)
            
            # 초점 영역 추정
            focus_area = self.estimate_focus_area(img)
            
            # 조명 분석
            lighting_type = self.analyze_lighting(lab)
            shadow_intensity = self.calculate_shadow_intensity(lab)
            highlight_intensity = self.calculate_highlight_intensity(lab)
            
            # 카메라 설정 추정
            estimated_focal_length = self.estimate_focal_length(img)
            estimated_aperture = self.estimate_aperture(img)
            depth_of_field = self.estimate_depth_of_field(img)
            
            return ImageFeatures(
                file_path=str(file_path),
                product_name=product_name,
                category=category,
                resolution=(width, height),
                aspect_ratio=width/height,
                file_size=file_size,
                brightness=float(brightness),
                contrast=float(contrast),
                saturation=float(saturation),
                sharpness=float(sharpness),
                dominant_colors=dominant_colors,
                color_palette=color_palette,
                edge_density=float(edge_density),
                texture_complexity=float(texture_complexity),
                focus_area=focus_area,
                lighting_type=lighting_type,
                shadow_intensity=float(shadow_intensity),
                highlight_intensity=float(highlight_intensity),
                estimated_focal_length=estimated_focal_length,
                estimated_aperture=estimated_aperture,
                depth_of_field=depth_of_field
            )
            
        except Exception as e:
            logger.error(f"특징 추출 실패 {image_path}: {e}")
            return None
    
    def extract_dominant_colors(self, img: np.ndarray, n_colors: int = 5) -> List[Tuple[int, int, int]]:
        """주요 색상 추출"""
        # 이미지 리사이즈 (성능 향상)
        small = cv2.resize(img, (100, 100))
        data = small.reshape((-1, 3))
        
        # K-means 클러스터링
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(data)
        
        # RGB 색상으로 변환
        colors = kmeans.cluster_centers_.astype(int)
        return [tuple(color) for color in colors]
    
    def classify_color_palette(self, colors: List[Tuple[int, int, int]]) -> str:
        """색상 팔레트 분류"""
        # 평균 색상 계산
        avg_color = np.mean(colors, axis=0)
        b, g, r = avg_color
        
        # HSV로 변환
        hsv = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = hsv
        
        # 팔레트 분류
        if s < 30:
            return "monochrome"
        elif v < 50:
            return "dark"
        elif v > 200:
            return "bright"
        elif 0 <= h < 30 or 150 <= h <= 180:
            return "warm"
        elif 60 <= h < 120:
            return "cool"
        else:
            return "neutral"
    
    def calculate_texture_complexity(self, gray: np.ndarray) -> float:
        """텍스처 복잡도 계산"""
        # GLCM (Gray Level Co-occurrence Matrix) 대신 간단한 방법 사용
        # 로컬 표준편차의 평균
        kernel_size = 5
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
        
        mean = cv2.filter2D(gray.astype(float), -1, kernel)
        sqr_mean = cv2.filter2D(gray.astype(float) ** 2, -1, kernel)
        variance = sqr_mean - mean ** 2
        
        return float(np.mean(np.sqrt(np.maximum(variance, 0))))
    
    def estimate_focus_area(self, img: np.ndarray) -> str:
        """초점 영역 추정"""
        height, width = img.shape[:2]
        
        # 중앙 영역 선명도
        center_y, center_x = height // 2, width // 2
        margin = min(height, width) // 4
        
        center_region = img[center_y-margin:center_y+margin, 
                           center_x-margin:center_x+margin]
        
        gray_center = cv2.cvtColor(center_region, cv2.COLOR_BGR2GRAY)
        center_sharpness = cv2.Laplacian(gray_center, cv2.CV_64F).var()
        
        # 전체 선명도
        gray_full = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        full_sharpness = cv2.Laplacian(gray_full, cv2.CV_64F).var()
        
        if center_sharpness > full_sharpness * 1.5:
            return "center"
        elif center_sharpness < full_sharpness * 0.7:
            return "edges"
        else:
            return "uniform"
    
    def analyze_lighting(self, lab: np.ndarray) -> str:
        """조명 유형 분석"""
        l_channel = lab[:,:,0]
        
        # 히스토그램 분석
        hist = cv2.calcHist([l_channel], [0], None, [256], [0, 256])
        hist = hist.flatten() / hist.sum()
        
        # 분포 특성 계산
        mean_val = np.mean(l_channel)
        std_val = np.std(l_channel)
        
        # 조명 유형 분류
        if std_val < 20:
            return "flat"
        elif mean_val > 180:
            return "high-key"
        elif mean_val < 80:
            return "low-key"
        elif std_val > 40:
            return "dramatic"
        else:
            return "natural"
    
    def calculate_shadow_intensity(self, lab: np.ndarray) -> float:
        """그림자 강도 계산"""
        l_channel = lab[:,:,0]
        # 하위 20% 픽셀의 평균값
        threshold = np.percentile(l_channel, 20)
        shadows = l_channel[l_channel < threshold]
        return float(np.mean(shadows)) if len(shadows) > 0 else 0.0
    
    def calculate_highlight_intensity(self, lab: np.ndarray) -> float:
        """하이라이트 강도 계산"""
        l_channel = lab[:,:,0]
        # 상위 20% 픽셀의 평균값
        threshold = np.percentile(l_channel, 80)
        highlights = l_channel[l_channel > threshold]
        return float(np.mean(highlights)) if len(highlights) > 0 else 255.0
    
    def estimate_focal_length(self, img: np.ndarray) -> str:
        """초점 거리 추정"""
        height, width = img.shape[:2]
        aspect = width / height
        
        # 간단한 휴리스틱 기반 추정
        if aspect > 1.5:
            return "wide-angle (24-35mm)"
        elif aspect < 0.8:
            return "telephoto (85-200mm)"
        else:
            return "standard (50-85mm)"
    
    def estimate_aperture(self, img: np.ndarray) -> str:
        """조리개 추정 (배경 흐림 기반)"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 중앙과 가장자리 선명도 비교
        h, w = gray.shape
        center = gray[h//3:2*h//3, w//3:2*w//3]
        edges = np.concatenate([
            gray[:h//3, :].flatten(),
            gray[2*h//3:, :].flatten(),
            gray[:, :w//3].flatten(),
            gray[:, 2*w//3:].flatten()
        ])
        
        center_sharp = cv2.Laplacian(center, cv2.CV_64F).var()
        edge_sharp = cv2.Laplacian(edges.reshape(-1, 1), cv2.CV_64F).var()
        
        ratio = center_sharp / (edge_sharp + 1e-6)
        
        if ratio > 3:
            return "f/1.4-f/2.8 (shallow)"
        elif ratio > 1.5:
            return "f/4-f/5.6 (medium)"
        else:
            return "f/8-f/11 (deep)"
    
    def estimate_depth_of_field(self, img: np.ndarray) -> str:
        """피사계 심도 추정"""
        aperture = self.estimate_aperture(img)
        
        if "shallow" in aperture:
            return "shallow depth of field with bokeh"
        elif "medium" in aperture:
            return "moderate depth of field"
        else:
            return "deep depth of field, everything in focus"
    
    def learn_from_directory(self, directory: str, max_images: int = 100) -> Dict:
        """디렉토리의 이미지들로부터 학습"""
        results = {
            'processed': 0,
            'learned': 0,
            'failed': 0,
            'patterns': defaultdict(list)
        }
        
        # 이미지 파일 찾기
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(Path(directory).rglob(f"*{ext}"))
        
        # 최대 개수만큼 처리
        for img_path in image_files[:max_images]:
            results['processed'] += 1
            
            # 특징 추출
            features = self.extract_image_features(str(img_path))
            
            if features:
                # 데이터베이스에 추가
                self.features_db.append(asdict(features))
                results['learned'] += 1
                
                # 패턴 학습
                results['patterns'][features.category].append({
                    'lighting': features.lighting_type,
                    'palette': features.color_palette,
                    'focal': features.estimated_focal_length,
                    'aperture': features.estimated_aperture
                })
                
                logger.info(f"학습 완료: {features.product_name} ({features.category})")
            else:
                results['failed'] += 1
        
        # 데이터베이스 저장
        self.save_database()
        
        # 패턴 분석 및 프롬프트 템플릿 생성
        self.analyze_patterns_and_create_templates(results['patterns'])
        
        return results
    
    def analyze_patterns_and_create_templates(self, patterns: Dict):
        """패턴 분석 및 프롬프트 템플릿 생성"""
        for category, pattern_list in patterns.items():
            if not pattern_list:
                continue
            
            # 가장 빈번한 설정 찾기
            lighting_counts = defaultdict(int)
            palette_counts = defaultdict(int)
            focal_counts = defaultdict(int)
            aperture_counts = defaultdict(int)
            
            for p in pattern_list:
                lighting_counts[p['lighting']] += 1
                palette_counts[p['palette']] += 1
                focal_counts[p['focal']] += 1
                aperture_counts[p['aperture']] += 1
            
            # 최빈값 찾기
            common_lighting = max(lighting_counts, key=lighting_counts.get)
            common_palette = max(palette_counts, key=palette_counts.get)
            common_focal = max(focal_counts, key=focal_counts.get)
            common_aperture = max(aperture_counts, key=aperture_counts.get)
            
            # 카테고리별 템플릿 생성
            self.prompt_templates[category] = {
                'lighting': f"{common_lighting} lighting",
                'camera': f"shot with {common_focal} lens at {common_aperture}",
                'style': f"{common_palette} color palette",
                'technical': "ultra-high resolution, photorealistic, professional photography"
            }
            
            logger.info(f"카테고리 '{category}' 템플릿 생성 완료")
    
    def generate_learned_prompt(self, subject: str, category: Optional[str] = None) -> str:
        """학습된 데이터 기반 프롬프트 생성"""
        prompt_parts = [f"A photorealistic image of {subject}"]
        
        # 카테고리별 템플릿 적용
        if category and category in self.prompt_templates:
            template = self.prompt_templates[category]
            prompt_parts.extend([
                template['lighting'],
                template['camera'],
                template['style'],
                template['technical']
            ])
        else:
            # 기본 템플릿
            prompt_parts.extend([
                "natural studio lighting",
                "shot with 85mm lens at f/2.8",
                "neutral color palette",
                "ultra-high resolution, photorealistic"
            ])
        
        # 추가 사실성 키워드
        prompt_parts.extend([
            "hyperrealistic",
            "indistinguishable from real photograph",
            "commercial product photography",
            "award-winning quality",
            "8K resolution",
            "ultra-detailed texture",
            "perfect focus"
        ])
        
        return ", ".join(prompt_parts)
    
    def find_similar_images(self, target_features: ImageFeatures, top_k: int = 5) -> List[Dict]:
        """유사한 이미지 찾기"""
        similarities = []
        
        for stored in self.features_db:
            # 유사도 계산 (간단한 유클리드 거리)
            score = 0
            score += abs(stored['brightness'] - target_features.brightness)
            score += abs(stored['contrast'] - target_features.contrast)
            score += abs(stored['saturation'] - target_features.saturation)
            score += abs(stored['sharpness'] - target_features.sharpness)
            
            similarities.append({
                'image': stored['file_path'],
                'product': stored['product_name'],
                'category': stored['category'],
                'score': score
            })
        
        # 점수 기준 정렬 (낮을수록 유사)
        similarities.sort(key=lambda x: x['score'])
        
        return similarities[:top_k]

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("실제 이미지 기반 학습 시스템")
    print("=" * 60)
    
    learner = RealImageLearner()
    
    # Cafe24 이미지 학습
    cafe24_dirs = [
        "C:/Users/8899y/CUA-MASTER/modules/cafe24/ftp_mirror/download/web/product/life",
        "C:/Users/8899y/CUA-MASTER/modules/cafe24/ftp_mirror/download/web/product/ccw",
        "C:/Users/8899y/CUA-MASTER/modules/cafe24/ftp_mirror/download/web/product/taekong"
    ]
    
    for dir_path in cafe24_dirs:
        if os.path.exists(dir_path):
            print(f"\n학습 중: {dir_path}")
            results = learner.learn_from_directory(dir_path, max_images=20)
            print(f"결과: 처리 {results['processed']}, 학습 {results['learned']}, 실패 {results['failed']}")
    
    # 학습된 템플릿 표시
    print("\n" + "=" * 60)
    print("학습된 프롬프트 템플릿")
    print("=" * 60)
    
    for category, template in learner.prompt_templates.items():
        print(f"\n[{category}]")
        for key, value in template.items():
            print(f"  {key}: {value}")
    
    # 테스트 프롬프트 생성
    print("\n" + "=" * 60)
    print("테스트 프롬프트 생성")
    print("=" * 60)
    
    test_subjects = [
        ("Korean BBQ galbi", "life"),
        ("Fresh kimchi", "ccw"),
        ("Seafood pancake", "taekong")
    ]
    
    for subject, category in test_subjects:
        prompt = learner.generate_learned_prompt(subject, category)
        print(f"\n제품: {subject}")
        print(f"프롬프트: {prompt[:200]}...")

if __name__ == "__main__":
    main()