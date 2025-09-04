"""
Google Vertex AI Provider Implementation
"""

import os
import logging
from typing import List, Dict, Any, Optional
from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class VertexProvider(BaseProvider):
    """Google Vertex AI provider"""
    
    @property
    def name(self) -> str:
        return "vertex"
    
    @property
    def default_model(self) -> str:
        return "claude-3-opus@20240229"
    
    @property
    def supported_models(self) -> List[str]:
        return [
            "claude-3-opus@20240229",
            "claude-3-sonnet@20240229",
            "claude-3-haiku@20240229"
        ]
    
    def _initialize(self):
        """Initialize Vertex AI client"""
        try:
            from google.cloud import aiplatform
            from anthropic import AnthropicVertex
            
            # Initialize Vertex AI
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
            
            aiplatform.init(project=project_id, location=location)
            
            self.client = AnthropicVertex(
                region=location,
                project_id=project_id
            )
            logger.info("Vertex AI client initialized")
        except ImportError:
            logger.warning("Google Cloud or Anthropic Vertex library not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize Vertex client: {e}")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> ProviderResponse:
        """Generate response from Vertex AI"""
        if not self.client:
            return ProviderResponse(content="Vertex AI client not initialized")
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 1000),
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", 0.7)
            )
            
            return ProviderResponse(
                content=response.content[0].text if response.content else "",
                metadata={"model": self.model}
            )
        except Exception as e:
            logger.error(f"Vertex generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")
    
    def generate_with_image(self, prompt: str, image: Any, **kwargs) -> ProviderResponse:
        """Generate response with image context"""
        if not self.client:
            return ProviderResponse(content="Vertex AI client not initialized")
        
        try:
            # Convert image to base64
            import base64
            import io
            from PIL import Image
            
            if isinstance(image, Image.Image):
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                image_base64 = base64.b64encode(buffer.getvalue()).decode()
            else:
                image_base64 = image
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 1000),
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                temperature=kwargs.get("temperature", 0.7)
            )
            
            return ProviderResponse(
                content=response.content[0].text if response.content else "",
                metadata={"model": self.model}
            )
        except Exception as e:
            logger.error(f"Vertex image generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")