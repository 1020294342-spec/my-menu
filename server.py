import http.server
import json
import os
from urllib.parse import urlparse, parse_qs

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # 1. 处理图片上传 (/upload)
        if self.path == '/upload':
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                
                if not os.path.exists('images'):
                    os.makedirs('images')

                # 获取文件名
                name_start = body.find(b'filename="') + 10
                name_end = body.find(b'"', name_start)
                filename = body[name_start:name_end].decode('utf-8')

                # 获取文件数据（去除表单边界）
                data_start = body.find(b'\r\n\r\n', name_start) + 4
                boundary = body[:body.find(b'\r\n')]
                data_end = body.find(boundary, data_start) - 4
                file_data = body[data_start:data_end]

                file_path = os.path.join('images', filename)
                with open(file_path, 'wb') as f:
                    f.write(file_data)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(filename.encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
            return

        # 2. 处理新增菜品 (/add)
        if self.path == '/add':
            content_length = int(self.headers['Content-Length'])
            new_dish = json.loads(self.rfile.read(content_length).decode('utf-8'))
            
            data = {"dishes": []}
            if os.path.exists('menu.json'):
                with open('menu.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            data['dishes'].append(new_dish)
            with open('menu.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.send_response(200)
            self.end_headers()
            return

        # 3. 处理修改菜品 (/edit)
        if self.path.startswith('/edit'):
            query = parse_qs(urlparse(self.path).query)
            index = int(query.get('index', [0])[0])
            content_length = int(self.headers['Content-Length'])
            updated_dish = json.loads(self.rfile.read(content_length).decode('utf-8'))

            with open('menu.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 0 <= index < len(data['dishes']):
                data['dishes'][index] = updated_dish
                with open('menu.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
            else:
                self.send_response(404)
            self.end_headers()
            return

        # 4. 处理删除菜品 (/delete)
        if self.path.startswith('/delete'):
            query = parse_qs(urlparse(self.path).query)
            index = int(query.get('index', [0])[0])

            with open('menu.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 0 <= index < len(data['dishes']):
                data['dishes'].pop(index)
                with open('menu.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
            else:
                self.send_response(404)
            self.end_headers()
            return

# 启动服务器
print("🚀 [全能版厨房后台已就绪]")
print("管理地址: http://localhost:8000/admin.html")
http.server.HTTPServer(('0.0.0.0', 8000), MyHandler).serve_forever()