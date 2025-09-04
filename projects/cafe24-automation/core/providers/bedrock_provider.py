"""
AWS Bedrock Provider Implementation
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class BedrockProvider(BaseProvider):
    """AWS Bedrock provider"""
    
    @property
    def name(self) -> str:
        return "bedrock"
    
    @property
    def default_model(self) -> str:
        return "anthropic.claude-3-opus-20240229-v1:0"
    
    @property
    def supported_models(self) -> List[str]:
        return [
            "anthropic.claude-3-opus-20240229-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-v2:1",
            "anthropic.claude-v2",
            "anthropic.claude-instant-v1"
        ]
    
    def _initialize(self):
        """Initialize Bedrock client"""
        try:
            import boto3
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
            logger.info("Bedrock client initialized")
        except ImportError:
            logger.warning("Boto3 library not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> ProviderResponse:
        """Generate response from Bedrock"""
        if not self.client:
            return ProviderResponse(content="Bedrock client not initialized")
        
        try:
            # Prepare request body based on model
            if "claude-3" in self.model:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": kwargs.get("max_tokens", 1000),
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": kwargs.get("temperature", 0.7)
                }
            else:
                body = {
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens_to_sample": kwargs.get("max_tokens", 1000),
                    "temperature": kwargs.get("temperature", 0.7)
                }
            
            response = self.client.invoke_model(
                modelId=self.model,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            
            if "claude-3" in self.model:
                content = response_body.get('content', [{}])[0].get('text', '')
            else:
                content = response_body.get('completion', '')
            
            return ProviderResponse(
                content=content,
                metadata={"model": self.model}
            )
        except Exception as e:
            logger.error(f"Bedrock generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")
    
    def generate_with_image(self, prompt: str, image: Any, **kwargs) -> ProviderResponse:
        """Generate response with image context"""
        if not self.client:
            return ProviderResponse(content="Bedrock client not initialized")
        
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
            
            # Only Claude 3 models support images
            if "claude-3" not in self.model:
                return ProviderResponse(content="Current model does not support image input")
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": kwargs.get("max_tokens", 1000),
                "messages": [
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
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            response = self.client.invoke_model(
                modelId=self.model,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            content = response_body.get('content', [{}])[0].get('text', '')
            
            return ProviderResponse(
                content=content,
                metadata={"model": self.model}
            )
        except Exception as e:
            logger.error(f"Bedrock image generation failed: {e}")
            return ProviderResponse(content=f"Error: {str(e)}")