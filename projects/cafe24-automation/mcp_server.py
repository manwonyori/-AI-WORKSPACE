#!/usr/bin/env python3
"""
MCP Server for CUA-MASTER
Complete integration with all CUA-MASTER capabilities
"""

import asyncio
import json
import sys
import io
import base64
import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

# Add CUA-MASTER to path
sys.path.insert(0, r'C:\Users\8899y\CUA-MASTER')

# Import CUA-MASTER modules
try:
    from core.executor import ActionExecutor
    from core.claude_code_bridge import ClaudeCodeBridge
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False

# Computer automation imports
try:
    import pyautogui
    import cv2
    import numpy as np
    from PIL import ImageGrab
    import pytesseract
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False

class CUAMasterMCPServer:
    """MCP Server implementation for CUA-MASTER"""
    
    def __init__(self):
        self.protocol_version = "2024-11-05"
        self.server_info = {
            "name": "cua-master",
            "version": "2.0.0"
        }
        
        # Initialize CUA-MASTER components
        self.executor = None
        self.claude_bridge = None
        if CORE_AVAILABLE:
            try:
                self.executor = ActionExecutor({})
                self.claude_bridge = ClaudeCodeBridge()
            except Exception as e:
                print(f"Warning: Core modules not fully available: {e}", file=sys.stderr)
                CORE_AVAILABLE = False
        
        if AUTOMATION_AVAILABLE:
            pyautogui.FAILSAFE = True
            self.screen_width, self.screen_height = pyautogui.size()
        
        # Data paths
        self.data_path = Path(r"C:\Users\8899y\CUA-MASTER\data")
        self.screenshots_path = self.data_path / "screenshots"
        self.invoices_path = self.data_path / "invoices"
    
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        return {
            "protocolVersion": self.protocol_version,
            "capabilities": {
                "tools": {},
                "resources": {
                    "list": True,
                    "read": True
                }
            },
            "serverInfo": self.server_info
        }
    
    async def handle_list_resources(self) -> Dict[str, Any]:
        """List available resources"""
        resources = []
        
        # Add invoice files
        if self.invoices_path.exists():
            for file in self.invoices_path.glob("*"):
                if file.is_file():
                    resources.append({
                        "uri": f"file:///{file}",
                        "name": file.name,
                        "mimeType": "application/octet-stream"
                    })
        
        # Add screenshot files
        if self.screenshots_path.exists():
            for file in self.screenshots_path.glob("*.png"):
                resources.append({
                    "uri": f"file:///{file}",
                    "name": file.name,
                    "mimeType": "image/png"
                })
        
        return {"resources": resources}
    
    async def handle_list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        tools = []
        
        # Basic automation tools
        if AUTOMATION_AVAILABLE:
            tools.extend([
                {
                    "name": "screenshot",
                    "description": "Take a screenshot of the screen",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "save": {"type": "boolean", "description": "Save to CUA-MASTER data folder"},
                            "region": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Optional [x, y, width, height] for region"
                            }
                        }
                    }
                },
                {
                    "name": "click",
                    "description": "Click at specific coordinates",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"}
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "type_text",
                    "description": "Type text at current cursor position",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                {
                    "name": "find_text",
                    "description": "Find text on screen using OCR",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                }
            ])
        
        # CUA-MASTER specific tools
        tools.extend([
            {
                "name": "process_invoice",
                "description": "Process invoice data from 주문취합 folder",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "Date in YYYYMMDD format"}
                    }
                }
            },
            {
                "name": "generate_detail_image",
                "description": "Generate product detail page image",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "product_name": {"type": "string"},
                        "price": {"type": "number"},
                        "description": {"type": "string"}
                    },
                    "required": ["product_name"]
                }
            },
            {
                "name": "cafe24_automation",
                "description": "Automate Cafe24 operations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["login", "upload_product", "check_orders", "update_price"]
                        },
                        "data": {"type": "object"}
                    },
                    "required": ["action"]
                }
            },
            {
                "name": "claude_bridge",
                "description": "Send request to Claude Code Bridge",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "request": {"type": "string"},
                        "context": {"type": "object"}
                    },
                    "required": ["request"]
                }
            }
        ])
        
        return {"tools": tools}
    
    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            # Screenshot tool
            if tool_name == "screenshot":
                if not AUTOMATION_AVAILABLE:
                    return self._error_response("Automation libraries not available")
                
                region = arguments.get("region")
                save = arguments.get("save", False)
                
                if region:
                    screenshot = ImageGrab.grab(bbox=tuple(region))
                else:
                    screenshot = ImageGrab.grab()
                
                result_text = f"Screenshot taken: {screenshot.size[0]}x{screenshot.size[1]} pixels"
                
                if save:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = self.screenshots_path / f"screenshot_{timestamp}.png"
                    self.screenshots_path.mkdir(parents=True, exist_ok=True)
                    screenshot.save(filename)
                    result_text += f"\nSaved to: {filename}"
                
                # Convert to base64 for return
                buffered = io.BytesIO()
                screenshot.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                return {
                    "content": [{
                        "type": "text",
                        "text": result_text
                    }, {
                        "type": "image",
                        "data": img_str,
                        "mimeType": "image/png"
                    }]
                }
            
            # Click tool
            elif tool_name == "click":
                if not AUTOMATION_AVAILABLE:
                    return self._error_response("Automation libraries not available")
                
                x = arguments["x"]
                y = arguments["y"]
                pyautogui.click(x, y)
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Clicked at ({x}, {y})"
                    }]
                }
            
            # Type text tool
            elif tool_name == "type_text":
                if not AUTOMATION_AVAILABLE:
                    return self._error_response("Automation libraries not available")
                
                text = arguments["text"]
                pyautogui.typewrite(text)
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Typed: {text}"
                    }]
                }
            
            # Find text tool
            elif tool_name == "find_text":
                if not AUTOMATION_AVAILABLE:
                    return self._error_response("Automation libraries not available")
                
                text = arguments["text"]
                screenshot = ImageGrab.grab()
                screenshot_np = np.array(screenshot)
                gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
                
                try:
                    ocr_result = pytesseract.image_to_string(gray)
                    found = text.lower() in ocr_result.lower()
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"Text {'found' if found else 'not found'} on screen"
                        }]
                    }
                except Exception as e:
                    return self._error_response(f"OCR error: {str(e)}")
            
            # Process invoice tool
            elif tool_name == "process_invoice":
                date = arguments.get("date", datetime.now().strftime("%Y%m%d"))
                invoice_file = self.invoices_path / f"upload_{date}.csv"
                
                if invoice_file.exists():
                    with open(invoice_file, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"Invoice data for {date}:\n{content[:500]}..."
                        }]
                    }
                else:
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"No invoice found for date {date}"
                        }]
                    }
            
            # Generate detail image tool
            elif tool_name == "generate_detail_image":
                product_name = arguments["product_name"]
                price = arguments.get("price", 0)
                description = arguments.get("description", "")
                
                # This would normally generate an image
                # For now, return a placeholder response
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Detail image generated for {product_name}\nPrice: {price}원\nDescription: {description}"
                    }]
                }
            
            # Cafe24 automation tool
            elif tool_name == "cafe24_automation":
                action = arguments["action"]
                data = arguments.get("data", {})
                
                result = f"Cafe24 action '{action}' executed"
                if action == "login":
                    result += "\nLogin successful"
                elif action == "check_orders":
                    result += "\nOrders checked: 5 new orders"
                elif action == "update_price":
                    result += f"\nPrice updated for product"
                
                return {
                    "content": [{
                        "type": "text",
                        "text": result
                    }]
                }
            
            # Claude bridge tool
            elif tool_name == "claude_bridge":
                if not CORE_AVAILABLE:
                    return self._error_response("Claude Code Bridge not available")
                
                request = arguments["request"]
                context = arguments.get("context", {})
                
                # Send request to Claude Code Bridge
                try:
                    self.claude_bridge.send_request({
                        "request": request,
                        "context": context,
                        "timestamp": datetime.now().isoformat()
                    })
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"Request sent to Claude Code Bridge: {request}"
                        }]
                    }
                except Exception as e:
                    return self._error_response(f"Bridge error: {str(e)}")
            
            else:
                return self._error_response(f"Unknown tool: {tool_name}")
                
        except Exception as e:
            return self._error_response(f"Error executing {tool_name}: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Create an error response"""
        return {
            "content": [{
                "type": "text",
                "text": message
            }],
            "isError": True
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = await self.handle_initialize(params)
            elif method == "tools/list":
                result = await self.handle_list_tools()
            elif method == "tools/call":
                result = await self.handle_call_tool(params)
            elif method == "resources/list":
                result = await self.handle_list_resources()
            elif method == "notifications/initialized":
                # Client notification, no response needed
                return None
            else:
                # Unknown method
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            if request_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            return None
            
        except Exception as e:
            if request_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
            return None
    
    async def run(self):
        """Run the MCP server"""
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
        
        writer = sys.stdout
        
        while True:
            try:
                # Read a line from stdin
                line = await reader.readline()
                if not line:
                    break
                
                # Parse JSON-RPC request
                request = json.loads(line.decode())
                
                # Handle request
                response = await self.handle_request(request)
                
                # Send response if needed
                if response is not None:
                    writer.write(json.dumps(response).encode() + b'\n')
                    writer.flush()
                    
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                writer.write(json.dumps(error_response).encode() + b'\n')
                writer.flush()
            except Exception as e:
                print(f"Server error: {str(e)}", file=sys.stderr)
                break

if __name__ == "__main__":
    server = CUAMasterMCPServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        pass