"""
Base Provider Interface
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ProviderResponse:
    """Standard response from providers"""
    content: str
    actions: Optional[List[Dict]] = None
    metadata: Optional[Dict] = None
    usage: Optional[Dict] = None


class BaseProvider(ABC):
    """Base class for all AI providers"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model or self.default_model
        self.client = None
        self._initialize()
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model for this provider"""
        pass
    
    @property
    @abstractmethod
    def supported_models(self) -> List[str]:
        """List of supported models"""
        pass
    
    @abstractmethod
    def _initialize(self):
        """Initialize the provider client"""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> ProviderResponse:
        """Generate response from the provider"""
        pass
    
    @abstractmethod
    def generate_with_image(self, prompt: str, image: Any, **kwargs) -> ProviderResponse:
        """Generate response with image context"""
        pass
    
    def validate_model(self, model: str) -> bool:
        """Check if model is supported"""
        return model in self.supported_models
    
    def set_model(self, model: str):
        """Set the active model"""
        if self.validate_model(model):
            self.model = model
        else:
            raise ValueError(f"Model {model} not supported by {self.name}")