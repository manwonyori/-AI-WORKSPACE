"""
MCP Server for Image Generation
Integrates multiple image generation models through Model Context Protocol
"""

import json
import sys
import os
import asyncio
import base64
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# MCP protocol imports
try:
    from mcp import (
        Resource,
        Tool,
        CallToolRequest,
        CallToolResult,
        TextContent,
        ImageContent,
        EmbeddedResource
    )
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP libraries not installed. Install with: pip install mcp")

# Import our image generation systems
from modules.nano_banana.gemini_flash_integration import GeminiFlashImageSystem
from modules.nano_banana.image_generation_system import NanoBananaImageSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ImageGenerationMCPServer:
    """MCP Server for image generation with multiple models"""
    
    def __init__(self):
        self.server = Server("nano-banana-image-gen")
        self.gemini_system = GeminiFlashImageSystem()
        self.nano_system = NanoBananaImageSystem()
        self.output_dir = Path("C:/Users/8899y/CUA-MASTER/generated_images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Start auto-upgrade service
        self.gemini_system.start_auto_upgrade_service()
        
        # Register tools
        self._register_tools()
        
        # Register resources
        self._register_resources()
    
    def _register_tools(self):
        """Register MCP tools for image generation"""
        
        @self.server.call_tool()
        async def generate_image(request: CallToolRequest) -> CallToolResult:
            """Generate an image using specified model"""
            try:
                args = request.params
                prompt = args.get("prompt", "")
                model = args.get("model", "gemini-flash")  # Default to Gemini
                auto_enhance = args.get("auto_enhance", True)
                style = args.get("style", None)
                
                logger.info(f"Generating image with {model}: {prompt[:50]}...")
                
                if model == "gemini-flash":
                    # Use Gemini 2.0 Flash
                    result = self.gemini_system.generate_with_gemini_flash(
                        prompt=prompt,
                        auto_enhance=auto_enhance
                    )
                    
                    # Save images
                    saved_images = []
                    for img_data in result["images"]:
                        img_path = self.output_dir / f"gemini_{img_data['id']}.png"
                        # In real implementation, save actual image data
                        saved_images.append(str(img_path))
                    
                    return CallToolResult(
                        content=[
                            TextContent(
                                text=json.dumps({
                                    "status": "success",
                                    "model": model,
                                    "prompt": result["prompt"],
                                    "enhanced_prompt": result["enhanced_prompt"],
                                    "images": saved_images,
                                    "metadata": result["metadata"]
                                }, indent=2)
                            )
                        ]
                    )
                    
                elif model in ["stable-diffusion", "dalle-mini", "midjourney"]:
                    # Use NanoBanana system
                    result = await self.nano_system.generate_image_async(
                        prompt=prompt,
                        model=model,
                        style=style
                    )
                    
                    return CallToolResult(
                        content=[
                            TextContent(
                                text=json.dumps({
                                    "status": result["status"],
                                    "model": model,
                                    "prompt": prompt,
                                    "images": result.get("images", []),
                                    "metadata": result.get("metadata", {})
                                }, indent=2)
                            )
                        ]
                    )
                else:
                    return CallToolResult(
                        content=[
                            TextContent(
                                text=json.dumps({
                                    "status": "error",
                                    "message": f"Unknown model: {model}"
                                })
                            )
                        ]
                    )
                    
            except Exception as e:
                logger.error(f"Error generating image: {e}")
                return CallToolResult(
                    content=[
                        TextContent(
                            text=json.dumps({
                                "status": "error",
                                "message": str(e)
                            })
                        )
                    ]
                )
        
        @self.server.call_tool()
        async def enhance_prompt(request: CallToolRequest) -> CallToolResult:
            """Enhance a prompt for better image generation"""
            try:
                args = request.params
                prompt = args.get("prompt", "")
                purpose = args.get("purpose", "general")  # general, product, detail_page
                
                # Use Gemini's auto-enhance
                enhanced = self.gemini_system._auto_enhance_prompt(prompt)
                
                # Get best pattern
                best_pattern = self.gemini_system._select_best_pattern(prompt)
                
                return CallToolResult(
                    content=[
                        TextContent(
                            text=json.dumps({
                                "original": prompt,
                                "enhanced": enhanced,
                                "best_pattern": best_pattern,
                                "purpose": purpose,
                                "suggestions": [
                                    "Add style keywords like: photorealistic, artistic, minimalist",
                                    "Include lighting: studio lighting, natural light, dramatic",
                                    "Specify quality: 4K, high resolution, professional",
                                    "Add mood: vibrant, moody, ethereal"
                                ]
                            }, indent=2)
                        )
                    ]
                )
            except Exception as e:
                logger.error(f"Error enhancing prompt: {e}")
                return CallToolResult(
                    content=[
                        TextContent(
                            text=json.dumps({
                                "status": "error",
                                "message": str(e)
                            })
                        )
                    ]
                )
        
        @self.server.call_tool()
        async def get_model_status(request: CallToolRequest) -> CallToolResult:
            """Get status of all available models"""
            try:
                # Get Gemini status
                gemini_status = self.gemini_system.get_upgrade_status()
                
                # Get NanoBanana status
                nano_status = self.nano_system.get_system_status()
                
                status = {
                    "gemini_flash": {
                        "available": True,
                        "version": gemini_status["current_version"],
                        "auto_upgrade": gemini_status["auto_upgrade_enabled"],
                        "last_check": gemini_status["last_check"],
                        "success_rate": gemini_status["success_rate"],
                        "features": self.gemini_system.gemini_config["features"]
                    },
                    "nano_banana": {
                        "models": nano_status["models"],
                        "queue_size": nano_status["queue_size"],
                        "processed_count": nano_status["processed_count"]
                    },
                    "available_models": [
                        "gemini-flash",
                        "stable-diffusion",
                        "dalle-mini",
                        "midjourney"
                    ]
                }
                
                return CallToolResult(
                    content=[
                        TextContent(
                            text=json.dumps(status, indent=2)
                        )
                    ]
                )
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                return CallToolResult(
                    content=[
                        TextContent(
                            text=json.dumps({
                                "status": "error",
                                "message": str(e)
                            })
                        )
                    ]
                )
        
        @self.server.call_tool()
        async def batch_generate(request: CallToolRequest) -> CallToolResult:
            """Generate multiple images in batch"""
            try:
                args = request.params
                prompts = args.get("prompts", [])
                model = args.get("model", "gemini-flash")
                
                results = []
                for prompt in prompts:
                    if model == "gemini-flash":
                        result = self.gemini_system.generate_with_gemini_flash(
                            prompt=prompt,
                            auto_enhance=True
                        )
                        results.append({
                            "prompt": prompt,
                            "status": "success",
                            "images": len(result["images"])
                        })
                    else:
                        # Queue in NanoBanana
                        task_id = self.nano_system.add_to_queue(
                            prompt=prompt,
                            model=model
                        )
                        results.append({
                            "prompt": prompt,
                            "status": "queued",
                            "task_id": task_id
                        })
                
                return CallToolResult(
                    content=[
                        TextContent(
                            text=json.dumps({
                                "batch_size": len(prompts),
                                "model": model,
                                "results": results
                            }, indent=2)
                        )
                    ]
                )
            except Exception as e:
                logger.error(f"Error in batch generation: {e}")
                return CallToolResult(
                    content=[
                        TextContent(
                            text=json.dumps({
                                "status": "error",
                                "message": str(e)
                            })
                        )
                    ]
                )
    
    def _register_resources(self):
        """Register MCP resources"""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available image generation resources"""
            return [
                Resource(
                    uri="image-gen://models",
                    name="Available Models",
                    description="List of available image generation models",
                    mimeType="application/json"
                ),
                Resource(
                    uri="image-gen://patterns",
                    name="Prompt Patterns",
                    description="Learned prompt patterns for better results",
                    mimeType="application/json"
                ),
                Resource(
                    uri="image-gen://gallery",
                    name="Generated Images",
                    description="Gallery of recently generated images",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a specific resource"""
            if uri == "image-gen://models":
                return json.dumps({
                    "models": [
                        {
                            "id": "gemini-flash",
                            "name": "Gemini 2.0 Flash",
                            "features": self.gemini_system.gemini_config["features"],
                            "status": "active"
                        },
                        {
                            "id": "stable-diffusion",
                            "name": "Stable Diffusion XL",
                            "status": "simulated"
                        },
                        {
                            "id": "dalle-mini",
                            "name": "DALL-E Mini",
                            "status": "simulated"
                        },
                        {
                            "id": "midjourney",
                            "name": "Midjourney v6",
                            "status": "simulated"
                        }
                    ]
                }, indent=2)
            elif uri == "image-gen://patterns":
                return json.dumps(
                    self.gemini_system.learning_engine["patterns"],
                    indent=2
                )
            elif uri == "image-gen://gallery":
                # List recent images
                images = list(self.output_dir.glob("*.png"))[:10]
                return json.dumps({
                    "gallery": [
                        {
                            "file": str(img),
                            "created": datetime.fromtimestamp(
                                img.stat().st_mtime
                            ).isoformat()
                        }
                        for img in images
                    ]
                }, indent=2)
            else:
                return json.dumps({"error": "Unknown resource"})
    
    async def run(self):
        """Run the MCP server"""
        if not MCP_AVAILABLE:
            print("MCP libraries not available. Please install with:")
            print("pip install mcp")
            return
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point"""
    print("=" * 60)
    print("Nano Banana MCP Image Generation Server")
    print("=" * 60)
    
    server = ImageGenerationMCPServer()
    
    print("\nAvailable tools:")
    print("  - generate_image: Generate images with any model")
    print("  - enhance_prompt: Improve prompts for better results")
    print("  - get_model_status: Check model availability")
    print("  - batch_generate: Generate multiple images")
    
    print("\nStarting MCP server...")
    print("Configure in claude_desktop_config.json:")
    print(json.dumps({
        "nano-banana": {
            "command": "python",
            "args": ["C:\\Users\\8899y\\CUA-MASTER\\modules\\nano_banana\\mcp_image_server.py"]
        }
    }, indent=2))
    
    # Run server
    asyncio.run(server.run())


if __name__ == "__main__":
    main()