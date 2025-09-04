"""
OpenAI Provider Implementation
"""

import os
import logging
from typing import List, Dict, Any, Optional
from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseProvider):
    """OpenAI GPT provider"""
    
    @property
    def name(self) -> str:
        return "openai"
    
    @property
    def default_model(self) -> str:
        return "gpt-4-vision-preview"
    
    @property
    def supported_models(self) -> List[str]:
        return [
            "gpt-4-vision-preview",
            "gpt-4-turbo-preview",
            "gpt-4",
            "gpt-3.5-turbo"
        ]
    
    def _initialize(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized")
        except ImportError:
            logger.warning("OpenAI library not installed")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> ProviderResponse:
        """Generate response from OpenAI"""
        if not self.client:
            return ProviderResponse(content="OpenAI client not initialized")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7)
            )
            
            return ProviderResponse(
                content=response.choices[0].message.content,
                usage={
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")
    
    def generate_with_image(self, prompt: str, image: Any, **kwargs) -> ProviderResponse:
        """Generate response with image context"""
        if not self.client:
            return ProviderResponse(content="OpenAI client not initialized")
        
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
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7)
            )
            
            return ProviderResponse(
                content=response.choices[0].message.content,
                usage={
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
        except Exception as e:
            logger.error(f"OpenAI image generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")