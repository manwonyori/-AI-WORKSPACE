import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import mimetypes
import base64
from datetime import datetime

app = Flask(__name__)
CORS(app)  # ChatGPT에서 접근 허용

@app.route('/mcp/list', methods=['POST'])
def list_directory():
    """디렉토리 목록 반환"""
    data = request.json
    path = data.get('path', 'C:\\Users\\8899y')
    
    try:
        items = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            items.append({
                'name': name,
                'path': full_path,
                'is_directory': os.path.isdir(full_path),
                'size': os.path.getsize(full_path) if os.path.isfile(full_path) else 0,
                'modified': os.path.getmtime(full_path)
            })
        
        return jsonify({
            'success': True,
            'path': path,
            'items': items,
            'count': len(items)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/mcp/read', methods=['POST'])
def read_file():
    """파일 내용 읽기"""
    data = request.json
    file_path = data.get('path')
    
    try:
        # 텍스트 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'path': file_path,
            'content': content,
            'type': 'text'
        })
    except UnicodeDecodeError:
        # 바이너리 파일 처리
        try:
            with open(file_path, 'rb') as f:
                content = base64.b64encode(f.read()).decode('utf-8')
            
            return jsonify({
                'success': True,
                'path': file_path,
                'content': content,
                'type': 'binary',
                'mime': mimetypes.guess_type(file_path)[0]
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/mcp/write', methods=['POST'])
def write_file():
    """파일 쓰기"""
    data = request.json
    file_path = data.get('path')
    content = data.get('content', '')
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'path': file_path,
            'message': 'File written successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/mcp/search', methods=['POST'])
def search_files():
    """파일 검색"""
    data = request.json
    directory = data.get('directory', 'C:\\Users\\8899y')
    pattern = data.get('pattern', '*')
    
    try:
        import glob
        search_path = os.path.join(directory, '**', pattern)
        files = glob.glob(search_path, recursive=True)
        
        results = []
        for file in files[:100]:  # 최대 100개
            results.append({
                'path': file,
                'name': os.path.basename(file),
                'size': os.path.getsize(file) if os.path.isfile(file) else 0
            })
        
        return jsonify({
            'success': True,
            'query': pattern,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/mcp/status', methods=['GET'])
def server_status():
    """서버 상태"""
    return jsonify({
        'status': 'running',
        'version': '1.0',
        'capabilities': ['list', 'read', 'write', 'search'],
        'base_path': 'C:\\Users\\8899y',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def home():
    """홈페이지"""
    return '''
    <html>
    <head>
        <title>ChatGPT Filesystem Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .status { background: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; }
            pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
            .endpoint { margin: 20px 0; padding: 15px; background: #fafafa; border-left: 4px solid #2196F3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ChatGPT Filesystem Server for MCP</h1>
            <div class="status">✅ Server Running</div>
            
            <h2>Available Endpoints:</h2>
            
            <div class="endpoint">
                <h3>POST /mcp/list</h3>
                <p>List directory contents</p>
                <pre>
fetch('http://localhost:7000/mcp/list', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({path: 'C:\\\\Users\\\\8899y'})
}).then(r => r.json()).then(console.log);
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>POST /mcp/read</h3>
                <p>Read file content</p>
                <pre>
fetch('http://localhost:7000/mcp/read', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({path: 'C:\\\\Users\\\\8899y\\\\README.md'})
}).then(r => r.json()).then(console.log);
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>POST /mcp/write</h3>
                <p>Write file content</p>
                <pre>
fetch('http://localhost:7000/mcp/write', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        path: 'C:\\\\Users\\\\8899y\\\\test.txt',
        content: 'Hello from ChatGPT!'
    })
}).then(r => r.json()).then(console.log);
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>POST /mcp/search</h3>
                <p>Search files</p>
                <pre>
fetch('http://localhost:7000/mcp/search', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        directory: 'C:\\\\Users\\\\8899y',
        pattern: '*.py'
    })
}).then(r => r.json()).then(console.log);
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>GET /mcp/status</h3>
                <p>Check server status</p>
                <pre>
fetch('http://localhost:7000/mcp/status')
    .then(r => r.json())
    .then(console.log);
                </pre>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("=" * 60)
    print("    ChatGPT Filesystem Server for MCP")
    print("=" * 60)
    print("\nServer running at: http://localhost:7000")
    print("\nWeb Interface: http://localhost:7000")
    print("\nStatus Check: http://localhost:7000/mcp/status")
    print("\nChatGPT에서 위 코드를 복사해서 사용하세요!")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=7000, debug=True)