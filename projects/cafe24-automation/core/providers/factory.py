"""
Provider Factory for creating AI providers
"""

import os
from typing import Optional
from .anthropic_provider import AnthropicProvider
from .openai_provider import OpenAIProvider
from .bedrock_provider import BedrockProvider
from .vertex_provider import VertexProvider


class ProviderFactory:
    """Factory for creating AI provider instances"""
    
    _providers = {
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider,
        "bedrock": BedrockProvider,
        "vertex": VertexProvider
    }
    
    @classmethod
    def create(cls, provider_type: str, 
              api_key: Optional[str] = None,
              model: Optional[str] = None):
        """Create a provider instance"""
        
        provider_type = provider_type.lower()
        
        if provider_type not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_type}")
        
        provider_class = cls._providers[provider_type]
        
        # Get API key from environment if not provided
        if not api_key:
            if provider_type == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
            elif provider_type == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
            elif provider_type == "bedrock":
                # AWS credentials handled differently
                pass
            elif provider_type == "vertex":
                # Google credentials handled differently
                pass
        
        return provider_class(api_key=api_key, model=model)
    
    @classmethod
    def list_providers(cls):
        """List available providers"""
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Register a new provider"""
        cls._providers[name] = provider_class