"""
Anthropic Provider Implementation
"""

import os
import logging
from typing import List, Dict, Any, Optional
from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseProvider):
    """Anthropic Claude provider"""
    
    @property
    def name(self) -> str:
        return "anthropic"
    
    @property
    def default_model(self) -> str:
        return "claude-3-opus-20240229"
    
    @property
    def supported_models(self) -> List[str]:
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-2.1",
            "claude-2.0",
            "claude-instant-1.2"
        ]
    
    def _initialize(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            logger.info("Anthropic client initialized")
        except ImportError:
            logger.warning("Anthropic library not installed")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> ProviderResponse:
        """Generate response from Anthropic"""
        if not self.client:
            return ProviderResponse(content="Anthropic client not initialized")
        
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
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            )
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")
    
    def generate_with_image(self, prompt: str, image: Any, **kwargs) -> ProviderResponse:
        """Generate response with image context"""
        if not self.client:
            return ProviderResponse(content="Anthropic client not initialized")
        
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
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            )
        except Exception as e:
            logger.error(f"Anthropic image generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")