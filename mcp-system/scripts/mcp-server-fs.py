"""
MCP Filesystem Server for Local File Access
ChatGPT가 제안한 Python 버전
"""

import os
import json
import sys
from datetime import datetime
import mimetypes

# pip install mcp 필요
try:
    from mcp.server import Server
    from mcp.types import Tool, ToolInputSchema
except ImportError:
    print("MCP 라이브러리 설치 필요: pip install mcp")
    sys.exit(1)

# 허용된 경로 목록
ALLOWED_PATHS = [
    r"C:\Users\8899y",
    r"D:\주문취합",
]

server = Server()

def is_allowed(path: str) -> bool:
    """경로 접근 권한 확인"""
    abs_path = os.path.abspath(path)
    for base in ALLOWED_PATHS:
        if abs_path.startswith(os.path.abspath(base)):
            return True
    return False

def format_size(size: int) -> str:
    """파일 크기를 읽기 쉽게 포맷"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"

@server.list_tools
def list_tools():
    """사용 가능한 도구 목록"""
    return [
        Tool(
            name="ls",
            description="List files in a directory with details",
            input_schema=ToolInputSchema.from_dict({
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"},
                    "pattern": {"type": "string", "description": "Optional filter pattern (e.g., *.py)"},
                    "sort_by": {"type": "string", "enum": ["name", "size", "date"], "default": "name"}
                },
                "required": ["path"]
            })
        ),
        Tool(
            name="read_file",
            description="Read file content (text files only)",
            input_schema=ToolInputSchema.from_dict({
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "max_lines": {"type": "integer", "default": 1000, "description": "Max lines to read"},
                    "encoding": {"type": "string", "default": "utf-8"}
                },
                "required": ["path"]
            })
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            input_schema=ToolInputSchema.from_dict({
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"},
                    "append": {"type": "boolean", "default": False, "description": "Append instead of overwrite"}
                },
                "required": ["path", "content"]
            })
        ),
        Tool(
            name="search",
            description="Search for files by name or content",
            input_schema=ToolInputSchema.from_dict({
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Search directory"},
                    "pattern": {"type": "string", "description": "File name pattern"},
                    "content": {"type": "string", "description": "Search in file content"},
                    "max_results": {"type": "integer", "default": 100}
                },
                "required": ["directory"]
            })
        ),
        Tool(
            name="file_info",
            description="Get detailed file information",
            input_schema=ToolInputSchema.from_dict({
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File or directory path"}
                },
                "required": ["path"]
            })
        )
    ]

@server.call_tool
def call_tool(name: str, arguments: dict):
    """도구 실행"""
    
    if name == "ls":
        path = arguments["path"]
        pattern = arguments.get("pattern", "*")
        sort_by = arguments.get("sort_by", "name")
        
        if not is_allowed(path):
            return {"error": f"Access denied: {path}"}
        if not os.path.isdir(path):
            return {"error": f"Not a directory: {path}"}
        
        items = []
        try:
            import fnmatch
            for entry in os.scandir(path):
                if pattern != "*" and not fnmatch.fnmatch(entry.name, pattern):
                    continue
                    
                try:
                    stat = entry.stat()
                    items.append({
                        "name": entry.name,
                        "path": entry.path.replace("\\", "/"),
                        "is_dir": entry.is_dir(),
                        "size": stat.st_size,
                        "size_formatted": format_size(stat.st_size) if not entry.is_dir() else "-",
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "type": "directory" if entry.is_dir() else os.path.splitext(entry.name)[1]
                    })
                except Exception as e:
                    items.append({"name": entry.name, "error": str(e)})
            
            # 정렬
            if sort_by == "size":
                items.sort(key=lambda x: x.get("size", 0), reverse=True)
            elif sort_by == "date":
                items.sort(key=lambda x: x.get("modified", ""), reverse=True)
            else:
                items.sort(key=lambda x: x.get("name", ""))
                
        except Exception as e:
            return {"error": str(e)}
        
        return {
            "path": path,
            "count": len(items),
            "items": items
        }
    
    elif name == "read_file":
        path = arguments["path"]
        max_lines = arguments.get("max_lines", 1000)
        encoding = arguments.get("encoding", "utf-8")
        
        if not is_allowed(path):
            return {"error": f"Access denied: {path}"}
        if not os.path.isfile(path):
            return {"error": f"Not a file: {path}"}
        
        try:
            with open(path, "r", encoding=encoding) as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        lines.append(f"... ({max_lines} lines shown)")
                        break
                    lines.append(line.rstrip())
            
            return {
                "path": path,
                "content": "\n".join(lines),
                "lines": len(lines),
                "encoding": encoding
            }
        except Exception as e:
            return {"error": str(e)}
    
    elif name == "write_file":
        path = arguments["path"]
        content = arguments["content"]
        append = arguments.get("append", False)
        
        if not is_allowed(path):
            return {"error": f"Access denied: {path}"}
        
        try:
            mode = "a" if append else "w"
            with open(path, mode, encoding="utf-8") as f:
                f.write(content)
            
            return {
                "path": path,
                "written": len(content),
                "mode": "append" if append else "overwrite"
            }
        except Exception as e:
            return {"error": str(e)}
    
    elif name == "search":
        directory = arguments["directory"]
        pattern = arguments.get("pattern", "*")
        content = arguments.get("content", "")
        max_results = arguments.get("max_results", 100)
        
        if not is_allowed(directory):
            return {"error": f"Access denied: {directory}"}
        
        results = []
        count = 0
        
        try:
            import fnmatch
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if count >= max_results:
                        break
                    
                    if not fnmatch.fnmatch(file, pattern):
                        continue
                    
                    file_path = os.path.join(root, file)
                    
                    # 내용 검색
                    if content:
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                file_content = f.read(10000)  # 처음 10KB만
                                if content.lower() not in file_content.lower():
                                    continue
                        except:
                            continue
                    
                    results.append({
                        "path": file_path.replace("\\", "/"),
                        "name": file,
                        "size": os.path.getsize(file_path)
                    })
                    count += 1
            
        except Exception as e:
            return {"error": str(e)}
        
        return {
            "directory": directory,
            "pattern": pattern,
            "content_search": content if content else None,
            "found": len(results),
            "results": results
        }
    
    elif name == "file_info":
        path = arguments["path"]
        
        if not is_allowed(path):
            return {"error": f"Access denied: {path}"}
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}
        
        try:
            stat = os.stat(path)
            info = {
                "path": path.replace("\\", "/"),
                "name": os.path.basename(path),
                "exists": True,
                "is_file": os.path.isfile(path),
                "is_directory": os.path.isdir(path),
                "size": stat.st_size,
                "size_formatted": format_size(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            }
            
            if os.path.isfile(path):
                info["extension"] = os.path.splitext(path)[1]
                info["mime_type"] = mimetypes.guess_type(path)[0]
            
            if os.path.isdir(path):
                try:
                    info["item_count"] = len(os.listdir(path))
                except:
                    info["item_count"] = "Access denied"
            
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    return {"error": f"Unknown tool: {name}"}

if __name__ == "__main__":
    print("=" * 60)
    print("MCP Filesystem Server (Python)")
    print("=" * 60)
    print(f"Allowed paths:")
    for path in ALLOWED_PATHS:
        print(f"  - {path}")
    print("=" * 60)
    print("Starting stdio server...")
    
    # stdio 모드로 실행 (Claude/ChatGPT가 직접 통신)
    server.run_stdio()