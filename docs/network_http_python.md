# HTTP 在 Python 的实现

HTTP 通常使用请求-响应（request-response）模型进行通信。

Python 的网络编程生态非常丰富，从底层的 Socket 到高层的 Web 框架，涵盖了不同抽象层级的需求。

## HTTP client

python 语言实现客户端联网，有多种方式：

| 库名称         | 协议层 | 核心特点                                 | 适用场景                                            |
| :------------- | :----- | :--------------------------------------- | :-------------------------------------------------- |
| socket (UDP)   | 传输层 | 无连接、不可靠、极速、保留消息边界       | DNS 查询、视频流缓冲、IoT 设备上报、心跳包          |
| socket (TCP)   | 传输层 | 面向连接、可靠传输、字节流、有粘包风险   | 自定义私有协议、即时通讯客户端、游戏客户端          |
| http.client    | 应用层 | 标准库、底层 HTTP 实现、无第三方依赖     | 学习 HTTP 协议原理、极简环境下的 HTTP 交互          |
| urllib.request | 应用层 | 标准库、功能全但 API 繁琐、支持代理/认证 | 简单的网页抓取、不想安装第三方库时的 HTTP 请求      |
| requests       | 应用层 | 人类使用的 HTTP 库，API 优雅、生态丰富   | 绝大多数 API 调用、自动化测试、日常业务开发         |
| aiohttp        | 应用层 | 异步非阻塞、基于 asyncio、高并发         | 高并发爬虫、WebSocket 通信、构建高性能异步 Web 服务 |

### Socket (UDP)：无连接的极速客户端

基于 UDP 的 Socket 客户端不需要建立连接（三次握手），直接发送数据包。

- 核心特点：
  - 无连接： 不需要 connect，直接 sendto。
  - 不可靠： 发送后不保证对方收到，也不保证顺序。
  - 保留边界： 发送什么长度的包，接收端就收到什么长度的包（不会粘包）。
- 适用场景： 对实时性要求极高但对丢包不敏感的场景，如 DNS 解析、直播弹幕、游戏位置同步。

```python
import socket

# 创建 UDP 套接字 (SOCK_DGRAM)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 目标地址
server_addr = ('127.0.0.1', 9999)
msg = "Hello UDP Server"

try:
    # UDP 客户端不需要 connect，直接 sendto
    # 也可以先 connect，然后使用 send，但本质还是 UDP
    client.sendto(msg.encode('utf-8'), server_addr)

    # 接收数据
    data, server = client.recvfrom(1024)
    print(f"收到回复: {data.decode('utf-8')}")
finally:
    client.close()
```

### Socket (TCP)：可靠的流式客户端

基于 TCP 的 Socket 客户端是网络编程的基础，它提供可靠的、双向的字节流传输。

- 核心特点：
  - 面向连接： 必须通过 connect 建立连接（三次握手）。
  - 可靠传输： 保证数据无差错、不丢失、不重复、按序到达。
  - 字节流： 没有消息边界，发送多次小数据可能会被接收方一次性收到（粘包），需要在应用层处理。
- 适用场景： 文件传输、聊天软件、数据库连接、自定义 RPC 调用。

```python
import socket

# 创建 TCP 套接字 (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 1. 建立连接
    client.connect(('127.0.0.1', 8888))

    # 2. 发送数据
    client.send("Hello TCP Server".encode('utf-8'))

    # 3. 接收数据
    response = client.recv(1024)
    print(f"收到回复: {response.decode('utf-8')}")

finally:
    # 4. 关闭连接
    client.close()
```

### http.client

`http` 模块是 Python 标准的 HTTP 协议实现，其中`http.client`用于 HTTP 协议的客户端实现，基于 socket(TCP) 封装了 HTTP 协议解析逻辑。

- 核心特点：
  - 直接操作 HTTP 协议层，需要手动处理请求头、请求体。
  - 响应对象包含状态码、理由短语、头部信息等原始信息。
- 缺点： API 设计较为繁琐，需要手动管理连接，不支持自动重定向或复杂的会话保持。
- 适用性： 除非是为了学习 HTTP 协议底层细节，否则不推荐在现代开发中作为首选。

```python
import http.client

# 1. 创建连接对象 (注意：HTTPS 需要传入 context 或自动处理)
conn = http.client.HTTPConnection("httpbin.org", timeout=10)

try:
    # 2. 发送请求 (方法, 路径)
    conn.request("GET", "/get", headers={"User-Agent": "Python-Client"})

    # 3. 获取响应
    response = conn.getresponse()

    print(f"状态码: {response.status}")
    print(f"原因: {response.reason}")

    # 读取 body
    data = response.read().decode('utf-8')
    print(f"响应体: {data}")

finally:
    conn.close()
```

### urllib.request

urllib 是 Python 内置的 URL 处理模块，其中 `urllib.request` 也是内置的 HTTP 客户端，基于 `http.request` 实现，加强了功能。

- 核心特点：
  - 内置支持： 无需安装，支持 HTTP, HTTPS, FTP 等协议。
  - 功能： 支持基本的认证、代理、Cookie 处理。
- 缺点： 接口设计偏向面向对象且较为生硬（如处理 POST 请求需要将数据编码为 bytes），代码可读性不如 requests。
- 适用性： 简单的脚本编写，或者无法使用第三方库的环境。

```python
import urllib.request
import urllib.parse

url = 'https://httpbin.org/post'

# 准备 POST 数据
data = {'key': 'value'}
data_bytes = urllib.parse.urlencode(data).encode('utf-8')

# 构建请求对象 (可选，用于添加 Headers)
req = urllib.request.Request(url, data=data_bytes, method='POST')
req.add_header('User-Agent', 'Python-urllib/3.x')

try:
    # 发送请求并获取响应
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
        print(f"状态码: {response.status}")
        print(f"响应体: {html}")
except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code}")
except urllib.error.URLError as e:
    print(f"URL 错误: {e.reason}")
```

### requests

requests 是 Python 第三方库，以“给人类使用的 HTTP 库”为设计哲学，是目前使用最广泛的网络库，实现标准的 HTTP 库。

- 核心优势：
  - API 极其优雅： requests.get(url) 即可完成请求。
  - 功能完善： 自动处理 Keep-Alive 连接池、自动解码内容、支持 Session 会话保持。
- 最佳实践： 使用 Session 对象复用 TCP 连接，提升性能。

```python
import requests

# 使用 Session 复用连接
session = requests.Session()
session.headers.update({'User-Agent': 'MyApp/1.0'})

try:
    # 发送 GET 请求，设置超时时间
    resp = session.get('https://api.github.com', timeout=5)

    # 检查 HTTP 错误 (4xx, 5xx)
    resp.raise_for_status()

    print(f"状态码: {resp.status_code}")
    print(f"JSON 数据: {resp.json()}")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

### aiohttp：异步高并发客户端

aiohttp 是基于 asyncio 实现的异步 HTTP 客户端框架。

- 核心优势：
  - 高并发： 单线程即可处理数千个并发连接，非常适合 IO 密集型任务。
  - WebSocket 支持： 原生支持 WebSocket 协议，适合实时通信场景。
- 最佳实践： ClientSession 应当作为上下文管理器使用，不要为每个请求单独创建。

```python
import aiohttp
import asyncio

async def fetch(url):
    # 创建 ClientSession
    async with aiohttp.ClientSession() as session:
        # 发送请求
        async with session.get(url) as resp:
            # 确保状态码正常
            assert resp.status == 200
            return await resp.text()

async def main():
    url = 'https://www.python.org'
    html = await fetch(url)
    print(f"获取长度: {len(html)}")

# 运行异步主函数
asyncio.run(main())
```

## HTTP server

socket 模块是 Python 网络编程的基石，提供了对底层网络接口的直接访问。

### Socket - UDP (无连接)

UDP 提供无连接的数据报服务。服务端不需要 listen 和 accept，直接循环接收数据。

- 特点：不可靠、无序、速度快。

```python
import socket

def udp_server():
    # 创建 UDP 套接字 (SOCK_DGRAM=UDP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', 9998))
    print("UDP 服务端启动，监听端口 9998...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"收到来自 {addr} 的消息: {data.decode()}")
        # 发送回包
        server_socket.sendto(f"Echo: {data.decode()}".encode(), addr)

if __name__ == '__main__':
    udp_server()
```

### Socket - TCP (面向连接)

TCP 提供可靠的、面向连接的字节流服务。最典型的模式是：服务端监听 -> 接受连接 -> 循环收发数据。

- 特点： 可靠、有序、基于流。

```python
import socket
import threading

def handle_client(client_socket, address):
    print(f"接受来自 {address} 的连接")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"收到: {data.decode()}")
        client_socket.send(f"Echo: {data.decode()}".encode())
    client_socket.close()
    print(f"{address} 断开连接")

def tcp_server():
    # 创建 TCP 套接字 (AF_INET=IPv4, SOCK_STREAM=TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 允许端口复用，防止重启报错 Address already in use
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('127.0.0.1', 9999))
    server_socket.listen(5)
    print("TCP 服务端启动，监听端口 9999...")

    try:
        while True:
            client_socket, address = server_socket.accept()
            # 使用线程处理并发（简单示例）
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()
    finally:
        server_socket.close()

if __name__ == '__main__':
    tcp_server()
```

### socketserver - UDP

socketserver 是对 socket 的封装，它简化了服务器的编写，内置了并发处理机制（如 Forking, Threading）。

对于 UDP 服务器的实现，使用 DatagramRequestHandler。

注意 UDP 的 request 属性是一个包含 [data, socket] 的列表。

```python
import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # data 是字节流，socket 是用于回包的接口
        data = self.request[0].strip()
        socket = self.request[1]
        print(f"{self.client_address[0]} 发送: {data.decode()}")
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9998
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    print("SocketServer UDP 启动...")
    server.serve_forever()
```

### SocketServer - TCP

对于 UDP 服务器的实现，使用 BaseRequestHandler 处理请求，配合 ThreadingMixIn 轻松实现多线程 TCP 服务。

```python
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request 是连接的 socket
        while True:
            data = self.request.recv(1024).strip()
            if not data:
                break
            print(f"{self.client_address[0]} 发送: {data.decode()}")
            self.request.sendall(data.upper())

# 引入 ThreadingMixIn 实现多线程并发
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    print("SocketServer TCP 启动...")
    server.serve_forever()
```

### http.server

这是 Python 标准库中用于处理 HTTP 请求的模块，它是 Web 服务的基础。

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        response = f"路径: {self.path}, 方法: GET"
        self.wfile.write(response.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"收到 POST 数据: " + post_data)

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPHandler)
    print("HTTP Server 启动于端口 8000")
    server.serve_forever()
```

### WSGI 标准和实现wsgiref

WSGI (Web Server Gateway Interface) 是 Python Web 应用和服务器之间的通用接口标准。

wsgiref 是 WSGI 的参考实现，也是现代 Python Web 框架（Flask, Django）的底层原型。

> python web 网络编程为什么需要 WSGI ？

```python
from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    """
    environ: 包含请求信息的字典
    start_response: 用于开始 HTTP 响应的回调函数
    """
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)

    path = environ.get('PATH_INFO')
    return [f"WSGI 应用收到请求: {path}".encode('utf-8')]

if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8001, simple_app)
    print("WSGI Server 启动于端口 8001")
    httpd.serve_forever()
```

### 同步 Web 框架 Flask

标准库通常用于学习或脚本，生产级服务更多使用第三方库，特别是异步框架。

Flask 最流行的轻量级 Web 框架，基于 Werkzeug WSGI。

```python
# 需安装: pip install flask
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return f"Hello from Flask! 路径: {request.path}"

@app.route('/post', methods=['POST'])
def post_data():
    return f"收到数据: {request.json}"

if __name__ == '__main__':
    # 生产环境通常使用 gunicorn 启动
    app.run(host='127.0.0.1', port=5000, debug=True)
```

### 异步高性能框架 FastAPI

现代 Python 框架的代表，原生支持 async/await，性能极高。

FastAPI 默认使用 uvicorn（也是 WSGI 实现） 运行，基于 asyncio 协程，性能高。

```python
# 需安装: pip install fastapi uvicorn
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    # 模拟异步 IO 操作
    await asyncio.sleep(0.1)
    return {"message": "Hello from FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 启动命令通常在终端执行: uvicorn main:app --reload
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
```

### 高性能消息队列

ZeroMQ / PyZMQ (高性能消息队列)，用于构建分布式系统，比 Socket 更高级，支持多种模式（请求-响应、发布-订阅）。

```python
# 需安装: pip install pyzmq
import zmq
import time

def zmq_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP) # 回复模式
    socket.bind("tcp://*:5555")

    print("ZeroMQ 服务端启动...")
    while True:
        # 等待请求
        message = socket.recv()
        print(f"收到: {message}")
        time.sleep(1) # 模拟工作
        socket.send(b"World")

if __name__ == '__main__':
    zmq_server()
```
