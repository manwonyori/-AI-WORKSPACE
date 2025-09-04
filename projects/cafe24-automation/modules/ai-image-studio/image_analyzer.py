"""
AI Image Studio - Image Analyzer
Phase 4 Implementation: Multimodal analysis system for image quality assessment
"""

import cv2
import numpy as np
from PIL import Image, ImageStat, ImageEnhance
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import base64
import io
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

class ImageQualityAnalyzer:
    """Advanced image quality analysis system"""
    
    def __init__(self, db_path: str = None):
        self.base_path = Path(__file__).parent
        self.db_path = db_path or self.base_path / "analysis" / "image_analysis.db"
        self.analysis_results = []
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize SQLite database for storing analysis results"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_analysis (
                id TEXT PRIMARY KEY,
                image_path TEXT,
                timestamp TEXT,
                technical_score REAL,
                aesthetic_score REAL,
                prompt_match_score REAL,
                overall_score REAL,
                analysis_data TEXT,
                tags TEXT,
                recommendations TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompt_image_pairs (
                id TEXT PRIMARY KEY,
                prompt_id TEXT,
                image_id TEXT,
                match_score REAL,
                feedback_score REAL,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_image(self, image_path: str, 
                     prompt_data: Dict = None,
                     save_to_db: bool = True) -> Dict:
        """
        Comprehensive image quality analysis
        
        Args:
            image_path: Path to image file
            prompt_data: Associated prompt data for matching analysis
            save_to_db: Whether to save results to database
            
        Returns:
            Detailed analysis results
        """
        image_id = hashlib.md5(f"{image_path}_{datetime.now()}".encode()).hexdigest()[:8]
        
        # Load image
        try:
            pil_image = Image.open(image_path)
            cv_image = cv2.imread(image_path)
        except Exception as e:
            return {"error": f"Failed to load image: {e}"}
        
        # Technical analysis
        technical_results = self._analyze_technical_quality(pil_image, cv_image)
        
        # Aesthetic analysis
        aesthetic_results = self._analyze_aesthetic_quality(pil_image, cv_image)
        
        # Prompt matching (if prompt provided)
        prompt_match_results = {}
        if prompt_data:
            prompt_match_results = self._analyze_prompt_matching(
                pil_image, prompt_data
            )
        
        # Auto-tagging
        tags = self._generate_image_tags(pil_image, cv_image)
        
        # Overall scoring
        overall_score = self._calculate_overall_score(
            technical_results, aesthetic_results, prompt_match_results
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            technical_results, aesthetic_results, prompt_match_results
        )
        
        analysis_result = {
            "id": image_id,
            "image_path": image_path,
            "timestamp": datetime.now().isoformat(),
            "technical_analysis": technical_results,
            "aesthetic_analysis": aesthetic_results,
            "prompt_matching": prompt_match_results,
            "auto_tags": tags,
            "scores": {
                "technical": technical_results.get("overall_score", 0),
                "aesthetic": aesthetic_results.get("overall_score", 0),
                "prompt_match": prompt_match_results.get("match_score", 0),
                "overall": overall_score
            },
            "recommendations": recommendations,
            "metadata": {
                "image_size": pil_image.size,
                "image_mode": pil_image.mode,
                "file_size": Path(image_path).stat().st_size if Path(image_path).exists() else 0
            }
        }
        
        if save_to_db:
            self._save_analysis_to_db(analysis_result)
        
        self.analysis_results.append(analysis_result)
        return analysis_result
    
    def _analyze_technical_quality(self, pil_image: Image.Image, cv_image) -> Dict:
        """Analyze technical image quality metrics"""
        results = {}
        
        # Resolution analysis
        width, height = pil_image.size
        total_pixels = width * height
        results["resolution"] = {
            "width": width,
            "height": height,
            "total_pixels": total_pixels,
            "aspect_ratio": width / height,
            "quality_category": self._categorize_resolution(total_pixels)
        }
        
        # Sharpness analysis using Laplacian variance
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        results["sharpness"] = {
            "laplacian_variance": float(laplacian_var),
            "score": min(laplacian_var / 1000 * 100, 100),  # Normalize to 0-100
            "quality": "excellent" if laplacian_var > 1000 else 
                      "good" if laplacian_var > 500 else 
                      "fair" if laplacian_var > 100 else "poor"
        }
        
        # Noise analysis
        noise_score = self._calculate_noise_level(gray)
        results["noise"] = {
            "noise_level": noise_score,
            "score": 100 - noise_score,  # Higher noise = lower score
            "quality": "excellent" if noise_score < 10 else
                      "good" if noise_score < 20 else
                      "fair" if noise_score < 30 else "poor"
        }
        
        # Brightness analysis
        brightness_stats = ImageStat.Stat(pil_image.convert('L'))
        mean_brightness = brightness_stats.mean[0]
        results["brightness"] = {
            "mean_brightness": mean_brightness,
            "score": 100 - abs(mean_brightness - 128) / 128 * 100,  # Optimal around 128
            "quality": "optimal" if 100 <= mean_brightness <= 156 else
                      "acceptable" if 50 <= mean_brightness <= 200 else "poor"
        }
        
        # Contrast analysis
        contrast_enhancer = ImageEnhance.Contrast(pil_image)
        # Calculate contrast using standard deviation
        contrast_score = float(np.std(np.array(pil_image.convert('L'))))
        results["contrast"] = {
            "contrast_score": contrast_score,
            "score": min(contrast_score / 50 * 100, 100),  # Normalize
            "quality": "excellent" if contrast_score > 40 else
                      "good" if contrast_score > 25 else
                      "fair" if contrast_score > 15 else "poor"
        }
        
        # Overall technical score
        technical_scores = [
            results["sharpness"]["score"],
            results["noise"]["score"],
            results["brightness"]["score"],
            results["contrast"]["score"]
        ]
        results["overall_score"] = sum(technical_scores) / len(technical_scores)
        
        return results
    
    def _analyze_aesthetic_quality(self, pil_image: Image.Image, cv_image) -> Dict:
        """Analyze aesthetic quality using computer vision techniques"""
        results = {}
        
        # Color harmony analysis
        color_analysis = self._analyze_color_harmony(pil_image)
        results["color_harmony"] = color_analysis
        
        # Composition analysis
        composition_analysis = self._analyze_composition(cv_image)
        results["composition"] = composition_analysis
        
        # Visual balance
        balance_score = self._calculate_visual_balance(cv_image)
        results["visual_balance"] = {
            "balance_score": balance_score,
            "quality": "excellent" if balance_score > 0.8 else
                      "good" if balance_score > 0.6 else
                      "fair" if balance_score > 0.4 else "poor"
        }
        
        # Interest points detection
        interest_analysis = self._detect_interest_points(cv_image)
        results["interest_points"] = interest_analysis
        
        # Overall aesthetic score
        aesthetic_scores = [
            color_analysis.get("harmony_score", 50),
            composition_analysis.get("rule_of_thirds_score", 50),
            balance_score * 100,
            interest_analysis.get("score", 50)
        ]
        results["overall_score"] = sum(aesthetic_scores) / len(aesthetic_scores)
        
        return results
    
    def _analyze_prompt_matching(self, pil_image: Image.Image, prompt_data: Dict) -> Dict:
        """Analyze how well the image matches the original prompt"""
        results = {}
        
        # Extract visual features for comparison
        visual_features = self._extract_visual_features(pil_image)
        
        # Parse prompt for expected elements
        prompt_elements = self._parse_prompt_elements(prompt_data["prompt"])
        
        # Calculate matching scores
        color_match = self._match_color_expectations(visual_features, prompt_elements)
        composition_match = self._match_composition_expectations(visual_features, prompt_elements)
        style_match = self._match_style_expectations(visual_features, prompt_elements)
        
        results = {
            "color_match": color_match,
            "composition_match": composition_match,
            "style_match": style_match,
            "match_score": (color_match + composition_match + style_match) / 3,
            "expected_elements": prompt_elements,
            "detected_features": visual_features
        }
        
        return results
    
    def _generate_image_tags(self, pil_image: Image.Image, cv_image) -> List[str]:
        """Generate automatic tags for the image"""
        tags = []
        
        # Basic image properties
        width, height = pil_image.size
        if width > height:
            tags.append("landscape")
        elif height > width:
            tags.append("portrait")
        else:
            tags.append("square")
        
        # Color analysis
        dominant_colors = self._get_dominant_colors(pil_image)
        for color in dominant_colors[:3]:  # Top 3 colors
            color_name = self._rgb_to_color_name(color)
            tags.append(f"color_{color_name}")
        
        # Brightness tags
        brightness_stats = ImageStat.Stat(pil_image.convert('L'))
        mean_brightness = brightness_stats.mean[0]
        if mean_brightness > 180:
            tags.append("bright")
        elif mean_brightness < 80:
            tags.append("dark")
        else:
            tags.append("medium_light")
        
        # Contrast tags
        contrast_score = float(np.std(np.array(pil_image.convert('L'))))
        if contrast_score > 40:
            tags.append("high_contrast")
        elif contrast_score < 15:
            tags.append("low_contrast")
        else:
            tags.append("medium_contrast")
        
        # Quality tags
        sharpness = cv2.Laplacian(cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        if sharpness > 1000:
            tags.append("sharp")
        elif sharpness < 100:
            tags.append("blurry")
        
        # Resolution tags
        total_pixels = width * height
        if total_pixels > 8000000:  # > 8MP
            tags.append("high_resolution")
        elif total_pixels > 2000000:  # > 2MP
            tags.append("medium_resolution")
        else:
            tags.append("low_resolution")
        
        return tags
    
    def _calculate_overall_score(self, technical: Dict, aesthetic: Dict, prompt_match: Dict) -> float:
        """Calculate overall image quality score"""
        # Weight different aspects
        weights = {
            "technical": 0.4,
            "aesthetic": 0.4,
            "prompt_match": 0.2 if prompt_match else 0
        }
        
        scores = [
            technical.get("overall_score", 0) * weights["technical"],
            aesthetic.get("overall_score", 0) * weights["aesthetic"]
        ]
        
        if prompt_match:
            scores.append(prompt_match.get("match_score", 0) * 100 * weights["prompt_match"])
        
        # Adjust weights if no prompt matching
        if not prompt_match:
            weights["technical"] = 0.5
            weights["aesthetic"] = 0.5
            scores = [
                technical.get("overall_score", 0) * weights["technical"],
                aesthetic.get("overall_score", 0) * weights["aesthetic"]
            ]
        
        return sum(scores)
    
    def _generate_recommendations(self, technical: Dict, aesthetic: Dict, prompt_match: Dict) -> List[str]:
        """Generate actionable recommendations for improvement"""
        recommendations = []
        
        # Technical recommendations
        if technical.get("sharpness", {}).get("score", 100) < 50:
            recommendations.append("Increase image sharpness - consider higher resolution or better focus")
        
        if technical.get("noise", {}).get("score", 100) < 70:
            recommendations.append("Reduce image noise - use denoising filters or better lighting")
        
        brightness = technical.get("brightness", {}).get("mean_brightness", 128)
        if brightness < 50:
            recommendations.append("Increase image brightness - image appears too dark")
        elif brightness > 200:
            recommendations.append("Reduce image brightness - image appears overexposed")
        
        if technical.get("contrast", {}).get("score", 100) < 50:
            recommendations.append("Improve contrast - enhance dynamic range")
        
        # Aesthetic recommendations
        if aesthetic.get("color_harmony", {}).get("harmony_score", 100) < 60:
            recommendations.append("Improve color harmony - consider color grading")
        
        if aesthetic.get("composition", {}).get("rule_of_thirds_score", 100) < 50:
            recommendations.append("Improve composition - consider rule of thirds placement")
        
        if aesthetic.get("visual_balance", {}).get("balance_score", 1) < 0.5:
            recommendations.append("Improve visual balance - reposition key elements")
        
        # Prompt matching recommendations
        if prompt_match:
            if prompt_match.get("match_score", 1) < 0.7:
                recommendations.append("Better match the original prompt - adjust style or elements")
            
            if prompt_match.get("color_match", 100) < 60:
                recommendations.append("Adjust colors to better match prompt expectations")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Image quality is excellent - no major improvements needed")
        
        return recommendations
    
    # Helper methods for analysis
    def _categorize_resolution(self, total_pixels: int) -> str:
        """Categorize image resolution"""
        if total_pixels > 8000000:  # > 8MP
            return "high"
        elif total_pixels > 2000000:  # > 2MP
            return "medium"
        else:
            return "low"
    
    def _calculate_noise_level(self, gray_image) -> float:
        """Calculate image noise level"""
        # Use standard deviation of Laplacian as noise measure
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        noise_score = np.std(laplacian)
        return min(noise_score / 10, 100)  # Normalize to 0-100
    
    def _analyze_color_harmony(self, pil_image: Image.Image) -> Dict:
        """Analyze color harmony in the image"""
        # Convert to HSV for better color analysis
        hsv_image = pil_image.convert('HSV')
        hsv_array = np.array(hsv_image)
        
        # Extract hue values
        hue_values = hsv_array[:, :, 0].flatten()
        hue_std = np.std(hue_values)
        
        # Calculate color harmony score based on hue distribution
        harmony_score = max(0, 100 - hue_std / 2)  # Lower std = better harmony
        
        # Get dominant colors
        dominant_colors = self._get_dominant_colors(pil_image, k=5)
        
        return {
            "harmony_score": harmony_score,
            "hue_standard_deviation": float(hue_std),
            "dominant_colors": dominant_colors,
            "color_variety": len(set(tuple(c) for c in dominant_colors))
        }
    
    def _analyze_composition(self, cv_image) -> Dict:
        """Analyze image composition"""
        height, width = cv_image.shape[:2]
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Rule of thirds analysis
        third_x = width // 3
        third_y = height // 3
        
        # Find strong edges/features
        edges = cv2.Canny(gray, 50, 150)
        
        # Check for features near rule of thirds lines
        thirds_regions = [
            edges[third_y-10:third_y+10, :],  # Horizontal thirds
            edges[2*third_y-10:2*third_y+10, :],
            edges[:, third_x-10:third_x+10],  # Vertical thirds
            edges[:, 2*third_x-10:2*third_x+10]
        ]
        
        thirds_score = sum(np.sum(region > 0) for region in thirds_regions if region.size > 0)
        thirds_score = min(thirds_score / 1000 * 100, 100)  # Normalize
        
        return {
            "rule_of_thirds_score": thirds_score,
            "edge_density": float(np.sum(edges > 0) / edges.size),
            "composition_balance": self._calculate_composition_balance(edges)
        }
    
    def _calculate_visual_balance(self, cv_image) -> float:
        """Calculate visual balance of the image"""
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        
        # Calculate center of mass
        y_coords, x_coords = np.mgrid[0:height, 0:width]
        total_mass = np.sum(gray)
        
        if total_mass == 0:
            return 0.5  # Neutral balance for empty image
        
        center_x = np.sum(x_coords * gray) / total_mass
        center_y = np.sum(y_coords * gray) / total_mass
        
        # Calculate balance relative to image center
        balance_x = 1 - abs(center_x - width/2) / (width/2)
        balance_y = 1 - abs(center_y - height/2) / (height/2)
        
        return (balance_x + balance_y) / 2
    
    def _detect_interest_points(self, cv_image) -> Dict:
        """Detect and analyze interest points in the image"""
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Use SIFT for interest point detection
        sift = cv2.SIFT_create()
        keypoints = sift.detect(gray, None)
        
        # Calculate interest point distribution
        point_count = len(keypoints)
        
        if point_count == 0:
            return {"score": 0, "point_count": 0, "distribution": "none"}
        
        # Analyze distribution
        points = [(kp.pt[0], kp.pt[1]) for kp in keypoints]
        height, width = gray.shape
        
        # Check distribution across quadrants
        quadrants = [0, 0, 0, 0]  # TL, TR, BL, BR
        for x, y in points:
            if x < width/2 and y < height/2:
                quadrants[0] += 1
            elif x >= width/2 and y < height/2:
                quadrants[1] += 1
            elif x < width/2 and y >= height/2:
                quadrants[2] += 1
            else:
                quadrants[3] += 1
        
        # Calculate distribution score (more even = better)
        max_quad = max(quadrants)
        distribution_score = 100 - (max_quad - point_count/4) / (point_count/4) * 100 if point_count > 0 else 0
        
        return {
            "score": min(point_count / 100 * 100, 100),  # Normalize
            "point_count": point_count,
            "distribution_score": max(0, distribution_score),
            "quadrant_distribution": quadrants
        }
    
    def _get_dominant_colors(self, pil_image: Image.Image, k: int = 3) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image using k-means clustering"""
        # Convert image to RGB array
        img_array = np.array(pil_image.convert('RGB'))
        img_array = img_array.reshape((-1, 3))
        
        # Apply k-means clustering
        from sklearn.cluster import KMeans
        
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(img_array)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        return [tuple(color) for color in colors]
    
    def _rgb_to_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB values to approximate color names"""
        r, g, b = rgb
        
        # Simple color name mapping
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r > g and r > b:
            if r > 150:
                return "red"
            else:
                return "dark_red"
        elif g > r and g > b:
            if g > 150:
                return "green"
            else:
                return "dark_green"
        elif b > r and b > g:
            if b > 150:
                return "blue"
            else:
                return "dark_blue"
        elif r > 150 and g > 150 and b < 100:
            return "yellow"
        elif r > 150 and b > 150 and g < 100:
            return "magenta"
        elif g > 150 and b > 150 and r < 100:
            return "cyan"
        else:
            return "mixed"
    
    def _extract_visual_features(self, pil_image: Image.Image) -> Dict:
        """Extract visual features for prompt matching"""
        # This is a simplified version - in practice, you'd use more sophisticated
        # computer vision models like CLIP for better feature extraction
        
        features = {}
        
        # Color features
        features["dominant_colors"] = self._get_dominant_colors(pil_image)
        
        # Brightness
        brightness_stats = ImageStat.Stat(pil_image.convert('L'))
        features["brightness"] = brightness_stats.mean[0]
        
        # Size and aspect ratio
        width, height = pil_image.size
        features["aspect_ratio"] = width / height
        features["size"] = (width, height)
        
        return features
    
    def _parse_prompt_elements(self, prompt: str) -> Dict:
        """Parse prompt to extract expected visual elements"""
        # Simple keyword-based parsing - could be enhanced with NLP
        elements = {}
        
        # Color expectations
        color_keywords = ["red", "blue", "green", "yellow", "white", "black", "colorful", "vibrant"]
        elements["expected_colors"] = [color for color in color_keywords if color in prompt.lower()]
        
        # Lighting expectations
        lighting_keywords = ["bright", "dark", "natural light", "studio light", "dramatic", "soft"]
        elements["expected_lighting"] = [light for light in lighting_keywords if light in prompt.lower()]
        
        # Style expectations
        style_keywords = ["professional", "artistic", "realistic", "detailed", "minimalist"]
        elements["expected_style"] = [style for style in style_keywords if style in prompt.lower()]
        
        return elements
    
    def _match_color_expectations(self, visual_features: Dict, prompt_elements: Dict) -> float:
        """Match image colors with prompt expectations"""
        if not prompt_elements.get("expected_colors"):
            return 75  # Neutral score if no color expectations
        
        # Simple color matching logic
        # In practice, you'd use more sophisticated color space analysis
        dominant_colors = visual_features.get("dominant_colors", [])
        expected_colors = prompt_elements["expected_colors"]
        
        # This is a simplified matching - would need proper color space analysis
        matches = 0
        for expected in expected_colors:
            # Basic matching logic (would be more sophisticated in real implementation)
            if expected == "colorful" and len(dominant_colors) > 3:
                matches += 1
            elif expected == "bright" and visual_features.get("brightness", 0) > 150:
                matches += 1
            elif expected == "dark" and visual_features.get("brightness", 255) < 100:
                matches += 1
        
        return min(100, (matches / len(expected_colors)) * 100) if expected_colors else 75
    
    def _match_composition_expectations(self, visual_features: Dict, prompt_elements: Dict) -> float:
        """Match image composition with prompt expectations"""
        # Simplified composition matching
        return 75  # Default score - would implement proper composition analysis
    
    def _match_style_expectations(self, visual_features: Dict, prompt_elements: Dict) -> float:
        """Match image style with prompt expectations"""
        # Simplified style matching
        return 75  # Default score - would implement proper style analysis
    
    def _calculate_composition_balance(self, edges) -> float:
        """Calculate composition balance from edge map"""
        height, width = edges.shape
        
        # Divide image into quadrants and calculate edge density
        h_mid, w_mid = height // 2, width // 2
        
        quadrants = [
            edges[:h_mid, :w_mid],      # Top-left
            edges[:h_mid, w_mid:],      # Top-right
            edges[h_mid:, :w_mid],      # Bottom-left
            edges[h_mid:, w_mid:]       # Bottom-right
        ]
        
        densities = [np.sum(quad > 0) / quad.size for quad in quadrants]
        
        # Calculate balance as inverse of standard deviation
        std_dev = np.std(densities)
        balance = 1 / (1 + std_dev)
        
        return balance
    
    def _save_analysis_to_db(self, analysis_result: Dict):
        """Save analysis results to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO image_analysis 
            (id, image_path, timestamp, technical_score, aesthetic_score, 
             prompt_match_score, overall_score, analysis_data, tags, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_result["id"],
            analysis_result["image_path"],
            analysis_result["timestamp"],
            analysis_result["scores"]["technical"],
            analysis_result["scores"]["aesthetic"],
            analysis_result["scores"]["prompt_match"],
            analysis_result["scores"]["overall"],
            json.dumps(analysis_result),
            json.dumps(analysis_result["auto_tags"]),
            json.dumps(analysis_result["recommendations"])
        ))
        
        conn.commit()
        conn.close()

class FeedbackLoop:
    """Automated feedback loop system for continuous improvement"""
    
    def __init__(self, analyzer: ImageQualityAnalyzer):
        self.analyzer = analyzer
        self.feedback_data = []
        
    def collect_feedback(self, image_id: str, 
                        user_rating: int,
                        specific_feedback: Dict = None):
        """Collect user feedback for generated images"""
        feedback_entry = {
            "image_id": image_id,
            "user_rating": user_rating,  # 1-5 scale
            "timestamp": datetime.now().isoformat(),
            "specific_feedback": specific_feedback or {}
        }
        
        self.feedback_data.append(feedback_entry)
        
        # Update analysis database with feedback
        self._update_analysis_with_feedback(image_id, feedback_entry)
    
    def _update_analysis_with_feedback(self, image_id: str, feedback: Dict):
        """Update image analysis with user feedback"""
        conn = sqlite3.connect(self.analyzer.db_path)
        cursor = conn.cursor()
        
        # Get existing analysis
        cursor.execute(
            "SELECT analysis_data FROM image_analysis WHERE id = ?", 
            (image_id,)
        )
        result = cursor.fetchone()
        
        if result:
            analysis_data = json.loads(result[0])
            analysis_data["user_feedback"] = feedback
            
            # Update the record
            cursor.execute(
                "UPDATE image_analysis SET analysis_data = ? WHERE id = ?",
                (json.dumps(analysis_data), image_id)
            )
        
        conn.commit()
        conn.close()
    
    def analyze_feedback_patterns(self) -> Dict:
        """Analyze patterns in user feedback to improve the system"""
        if not self.feedback_data:
            return {"message": "No feedback data available"}
        
        # Calculate average ratings
        ratings = [f["user_rating"] for f in self.feedback_data]
        avg_rating = sum(ratings) / len(ratings)
        
        # Find common issues
        common_issues = {}
        for feedback in self.feedback_data:
            issues = feedback.get("specific_feedback", {}).get("issues", [])
            for issue in issues:
                common_issues[issue] = common_issues.get(issue, 0) + 1
        
        return {
            "total_feedback_count": len(self.feedback_data),
            "average_rating": avg_rating,
            "rating_distribution": {i: ratings.count(i) for i in range(1, 6)},
            "common_issues": common_issues,
            "improvement_suggestions": self._generate_improvement_suggestions(avg_rating, common_issues)
        }
    
    def _generate_improvement_suggestions(self, avg_rating: float, common_issues: Dict) -> List[str]:
        """Generate suggestions based on feedback analysis"""
        suggestions = []
        
        if avg_rating < 3:
            suggestions.append("Overall quality needs significant improvement")
        elif avg_rating < 4:
            suggestions.append("Focus on consistency and reliability")
        
        # Address common issues
        for issue, count in common_issues.items():
            if count > len(self.feedback_data) * 0.3:  # More than 30% have this issue
                suggestions.append(f"Address common issue: {issue}")
        
        return suggestions


if __name__ == "__main__":
    # Example usage and testing
    analyzer = ImageQualityAnalyzer()
    
    print("AI Image Studio - Image Analyzer initialized")
    print("Ready to analyze images for quality, aesthetics, and prompt matching")
    
    # Example prompt data for testing
    test_prompt = {
        "prompt": "Professional product photography of Korean food, clean white background, studio lighting, high resolution",
        "category": "food",
        "style": "product_showcase"
    }
    
    print(f"\nExample prompt: {test_prompt['prompt']}")
    print("Run analyzer.analyze_image(image_path, test_prompt) to analyze an image")