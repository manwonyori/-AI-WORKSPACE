#!/usr/bin/env python3
"""
Simplified MCP Server for CUA-MASTER
Minimal dependencies, maximum compatibility
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

class SimpleCUAServer:
    """Simplified MCP Server for CUA-MASTER"""
    
    def __init__(self):
        self.protocol_version = "2024-11-05"
        self.server_info = {
            "name": "cua-master",
            "version": "3.0.0"
        }
        
        # Data paths
        self.base_path = Path(r"C:\Users\8899y\CUA-MASTER")
        self.data_path = self.base_path / "data"
        self.screenshots_path = self.data_path / "screenshots"
        self.invoices_path = self.data_path / "invoices"
        
        # Try to import optional modules
        self.automation_available = False
        try:
            import pyautogui
            from PIL import ImageGrab
            self.pyautogui = pyautogui
            self.ImageGrab = ImageGrab
            self.automation_available = True
            pyautogui.FAILSAFE = True
        except ImportError:
            pass
    
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
        
        # Add data files
        for folder in [self.invoices_path, self.screenshots_path]:
            if folder.exists():
                for file in folder.iterdir():
                    if file.is_file():
                        resources.append({
                            "uri": f"file:///{file}",
                            "name": file.name,
                            "mimeType": self._get_mime_type(file.suffix)
                        })
        
        return {"resources": resources}
    
    def _get_mime_type(self, suffix: str) -> str:
        """Get MIME type from file extension"""
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".json": "application/json",
            ".csv": "text/csv",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".txt": "text/plain"
        }
        return mime_types.get(suffix.lower(), "application/octet-stream")
    
    async def handle_list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        tools = [
            {
                "name": "list_files",
                "description": "List files in CUA-MASTER data folders",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "folder": {
                            "type": "string",
                            "enum": ["screenshots", "invoices", "all"],
                            "description": "Which folder to list"
                        }
                    }
                }
            },
            {
                "name": "read_file",
                "description": "Read a file from CUA-MASTER data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "File name to read"}
                    },
                    "required": ["filename"]
                }
            },
            {
                "name": "get_status",
                "description": "Get CUA-MASTER system status",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        # Add automation tools if available
        if self.automation_available:
            tools.extend([
                {
                    "name": "screenshot",
                    "description": "Take a screenshot",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "save": {"type": "boolean", "description": "Save to screenshots folder"}
                        }
                    }
                },
                {
                    "name": "click",
                    "description": "Click at coordinates",
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
                    "description": "Type text",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                }
            ])
        
        return {"tools": tools}
    
    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            # List files tool
            if tool_name == "list_files":
                folder = arguments.get("folder", "all")
                files = []
                
                folders_to_check = []
                if folder == "all" or folder == "screenshots":
                    folders_to_check.append(self.screenshots_path)
                if folder == "all" or folder == "invoices":
                    folders_to_check.append(self.invoices_path)
                
                for folder_path in folders_to_check:
                    if folder_path.exists():
                        for file in folder_path.iterdir():
                            if file.is_file():
                                files.append({
                                    "name": file.name,
                                    "size": file.stat().st_size,
                                    "modified": file.stat().st_mtime
                                })
                
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Found {len(files)} files:\n" + 
                               "\n".join([f"- {f['name']} ({f['size']} bytes)" for f in files[:10]])
                    }]
                }
            
            # Read file tool
            elif tool_name == "read_file":
                filename = arguments["filename"]
                
                # Search for file in data folders
                file_path = None
                for folder in [self.screenshots_path, self.invoices_path, self.data_path]:
                    potential_path = folder / filename
                    if potential_path.exists():
                        file_path = potential_path
                        break
                
                if not file_path:
                    return self._error_response(f"File not found: {filename}")
                
                # Read file based on type
                if file_path.suffix in ['.png', '.jpg', '.jpeg']:
                    with open(file_path, 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode()
                    return {
                        "content": [{
                            "type": "image",
                            "data": img_data,
                            "mimeType": self._get_mime_type(file_path.suffix)
                        }]
                    }
                else:
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    return {
                        "content": [{
                            "type": "text",
                            "text": content[:5000]  # Limit to 5000 chars
                        }]
                    }
            
            # Get status tool
            elif tool_name == "get_status":
                status = {
                    "server": "CUA-MASTER MCP Server",
                    "version": "3.0.0",
                    "automation": "Available" if self.automation_available else "Not available",
                    "data_path": str(self.data_path),
                    "screenshots": len(list(self.screenshots_path.glob("*"))) if self.screenshots_path.exists() else 0,
                    "invoices": len(list(self.invoices_path.glob("*"))) if self.invoices_path.exists() else 0
                }
                return {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(status, indent=2)
                    }]
                }
            
            # Screenshot tool
            elif tool_name == "screenshot":
                if not self.automation_available:
                    return self._error_response("Automation not available")
                
                screenshot = self.ImageGrab.grab()
                
                result_text = f"Screenshot taken: {screenshot.size[0]}x{screenshot.size[1]}"
                
                if arguments.get("save", False):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = self.screenshots_path / f"screenshot_{timestamp}.png"
                    self.screenshots_path.mkdir(parents=True, exist_ok=True)
                    screenshot.save(filename)
                    result_text += f"\nSaved to: {filename.name}"
                
                # Convert to base64
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
                if not self.automation_available:
                    return self._error_response("Automation not available")
                
                x = arguments["x"]
                y = arguments["y"]
                self.pyautogui.click(x, y)
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Clicked at ({x}, {y})"
                    }]
                }
            
            # Type text tool
            elif tool_name == "type_text":
                if not self.automation_available:
                    return self._error_response("Automation not available")
                
                text = arguments["text"]
                self.pyautogui.typewrite(text)
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Typed: {text}"
                    }]
                }
            
            else:
                return self._error_response(f"Unknown tool: {tool_name}")
                
        except Exception as e:
            return self._error_response(f"Error in {tool_name}: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "content": [{
                "type": "text",
                "text": f"Error: {message}"
            }],
            "isError": True
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            # Route to appropriate handler
            if method == "initialize":
                result = await self.handle_initialize(params)
            elif method == "tools/list":
                result = await self.handle_list_tools()
            elif method == "tools/call":
                result = await self.handle_call_tool(params)
            elif method == "resources/list":
                result = await self.handle_list_resources()
            elif method == "notifications/initialized":
                return None  # No response for notifications
            else:
                if request_id is not None:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                return None
            
            # Return result if request has ID
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
        # Setup async stdin reader
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        
        try:
            await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
        except Exception:
            # Fallback for Windows
            pass
        
        # Main loop
        while True:
            try:
                # Read line from stdin
                if sys.stdin.isatty():
                    # Interactive mode - for testing
                    line = sys.stdin.readline()
                else:
                    # Pipe mode - normal operation
                    line = await reader.readline()
                
                if not line:
                    break
                
                # Parse JSON-RPC request
                if isinstance(line, bytes):
                    line = line.decode('utf-8')
                
                request = json.loads(line.strip())
                
                # Handle request
                response = await self.handle_request(request)
                
                # Send response if needed
                if response is not None:
                    print(json.dumps(response), flush=True)
                    
            except json.JSONDecodeError:
                # Invalid JSON - send error
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except KeyboardInterrupt:
                break
            except Exception as e:
                # Log error but continue
                print(f"Error: {e}", file=sys.stderr, flush=True)

if __name__ == "__main__":
    server = SimpleCUAServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        pass