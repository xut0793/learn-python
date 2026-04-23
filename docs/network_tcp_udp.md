# TCP / UDP

TCP / UDP 是实现计算机网络的核心协议，位于传输层层（Transport Layer），负责信息数据的传输。

## UDP

UDP (User Datagram Protocol) 一种无连接、不可靠但高效的传输层协议。它就像寄信，只管发出，不保证对方一定能收到，也不保证收到的顺序。

核心特性

- 无连接：发送数据前无需建立连接（无三次握手），直接发送，延迟极低。
- 不可靠：不保证数据包的送达、顺序，也无重传机制。如果数据包丢失或损坏，UDP协议本身不会处理。
- 面向数据报：保留应用层消息的边界。发送方调用一次sendto()，接收方就必须用一次recvfrom()来完整接收，否则数据可能被截断或丢弃。
- 开销小：协议头部固定为8字节，比TCP的20字节以上要小得多，传输效率高。
- 支持广播/多播：可以向网络中的多个或所有主机同时发送数据。
- 64KB限制：单个UDP数据报的最大长度为65535字节（包括8字节头部），实际可用数据约为64KB。传输更大数据需要在应用层手动分片。
- 可靠性需自行实现：如果业务需要可靠性，必须在应用层自行添加序列号、确认应答(ACK)和超时重传等机制。

## TCP

TCP (Transmission Control Protocol) 一种面向连接、可靠的、基于字节流的传输层协议。它就像打电话，通信前必须先建立连接，并保证通话内容准确无误地传达。

核心特性：

- 面向连接：通信前必须通过“三次握手”建立连接，通信结束后通过“四次挥手”断开连接。
- 可靠传输：通过序列号、确认应答(ACK)、超时重传等机制，确保数据无差错、不丢失、不重复且按序到达。
- 面向字节流：不保留应用层消息边界。发送方多次发送的数据，接收方可能一次性读取；反之，一次发送的大数据，接收方也可能分多次读取。这会导致“粘包”和“拆包”问题。
- 流量控制与拥塞控制：通过滑动窗口机制，防止发送方淹没接收方，并根据网络状况调整发送速率。

### 三次握手 (建立连接)：

客户端 -> 服务器 (SYN)：客户端发送一个SYN包，请求建立连接。
服务器 -> 客户端 (SYN+ACK)：服务器收到请求后，回复一个SYN+ACK包，表示同意建立连接。
客户端 -> 服务器 (ACK)：客户端收到服务器的同意后，再发送一个ACK包进行确认。至此，连接建立成功。

### 四次挥手 (断开连接)：

客户端 -> 服务器 (FIN)：客户端发送FIN包，表示数据已发送完毕，请求关闭连接。
服务器 -> 客户端 (ACK)：服务器收到FIN后，先回复一个ACK包进行确认。此时，服务器可能还有数据要发送。
服务器 -> 客户端 (FIN)：服务器数据发送完毕后，也发送一个FIN包，请求关闭连接。
客户端 -> 服务器 (ACK)：客户端收到服务器的FIN后，回复ACK包进行确认。连接正式关闭。

## Socket

Socket 就是网络通信的“插座”，应用程序（微信、浏览器等）装到电脑上，需要通过这个“插座”与操作系统的网络连接，就好比房子（操作系统）买了个家电（应用程序）需要插上电才能正常工作一样。

从本质上讲，Socket 是应用层与 TCP/IP 协议族通信的中间抽象层，表现为一组编程接口（API）。它屏蔽了底层网络硬件和协议（如三次握手、数据包分片）的复杂实现，为程序员提供了一个统一的接口来发送和接收数据。

- 进程间通信（IPC）：它不仅支持不同计算机（跨网络）的进程通信，也支持同一台计算机内部的进程通信（如 Unix 域套接字）。
- 数据传输的桥梁：它是应用程序（如 Python 代码）与操作系统内核（网络协议栈）之间的桥梁。应用层通过 Socket 将数据写入内核缓冲区，由操作系统负责将数据发送到网络。
- 抽象与解耦：它让开发者无需关心数据是如何在光纤、路由器之间传输的，只需关注“发给谁”和“发什么”。

形象类比：如果把网络通信比作打电话，IP 地址相当于“对方的电话号码”，端口号相当于“分机号”，而 Socket 就是你手中的“电话机”。你不需要知道电话线内部是如何传输信号的（底层协议细节），只需要拿起电话（调用 Socket 接口）说话（发送数据）即可。

一个 Socket 由 IP 地址 和 端口号 唯一标识，`Socket = (IP地址 : 端口号)`。

在 python 语言中，提供了 `socket` 模块，用于创建 Socket 对象。

以最经典的模型是 `客户端-服务器（C/S）模型`，分解下通信流程：

- 服务器端 (Server)：
  1. `socket()`: 创建一个“监听”插座。
  1. `bind()`: 绑定 IP 和端口（比如 127.0.0.1:8080）。
  1. `listen()`: 开始监听，等待敲门声。
  1. `accept()`: 阻塞等待客户端连接。一旦连接建立，会返回一个新的 Socket 对象用于通信。
  1. `recv() / send()`: 接收和发送数据。
  1. `close()`: 关闭连接（比如，如果是 TCP 套接字，则触发四次挥手）。
- 客户端 (Client)：
  1. `socket()`: 创建一个客户端插座。
  1. `connect()`: 向服务器发起连接请求（比如，如果是 TCP 套接字，则触发三次握手）。
  1. `send() / recv()`: 发送请求和接收响应。
  1. `close()`: 关闭连接（比如，如果是 TCP 套接字，则触发四次挥手）。

## socket 参数

函数签名：

```python
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
```

在日常开发中，你只需要关注 family 和 type 这两个参数，proto 使用默认值，fileno 几乎用不到。

| 参数   | 常用值               | 含义                                         |
| :----- | :------------------- | :------------------------------------------- |
| family | `socket.AF_INET`     | 使用 IPv4 地址进行通信。                     |
| type   | `socket.SOCK_STREAM` | 使用 TCP 协议，提供可靠、面向连接的字节流。  |
| type   | `socket.SOCK_DGRAM`  | 使用 UDP 协议，提供不可靠、无连接的数据报。  |
| proto  | `0` (默认)           | 由系统根据 `family` 和 `type` 自动选择协议。 |

### family (地址族)

这个参数决定了套接字通信所使用的网络协议族，通俗讲就是使用哪种类型的地址来定位设备，确定 IP 地址。

- socket.AF_INET
  - 含义: 这是最常用的选项，代表 IPv4 协议。它使用 xxx.xxx.xxx.xxx 格式的地址（如 127.0.0.1 或 192.168.1.100）来定位网络中的主机。
  - 场景: 绝大多数基于互联网或局域网的通信都使用此选项。
- socket.AF_INET6
  - 含义: 代表 IPv6 协议。这是为了解决 IPv4 地址耗尽问题而设计的下一代互联网协议，地址格式更长。
  - 场景: 在需要支持 IPv6 网络的环境中使用。
- socket.AF_UNIX
  - 含义: 也称为 AF_LOCAL，用于 Unix 系统内部的进程间通信 (IPC)。它不使用网络协议，而是通过文件系统路径来标识通信端点。
  - 场景: 在同一台 Unix/Linux 机器上，两个或多个进程需要高效通信时使用。

### type (套接字类型)

这个参数定义了数据传输的方式，它直接决定了使用哪种传输层协议，是面向连接还是无连接，确定 TCP 还是 UDP。

- socket.SOCK_STREAM
  - 含义: 提供 面向连接的、可靠的字节流 服务。它对应 TCP 协议。
  - 特性: 在数据传输前必须建立连接（三次握手），保证数据无差错、不丢失、不重复且按序到达。它不保留应用层消息的边界，会产生粘包/拆包问题。
  - 场景: 文件传输、网页浏览、邮件发送等对数据准确性要求高的场景。
- socket.SOCK_DGRAM
  - 含义: 提供 无连接的、不可靠的数据报 服务。它对应 UDP 协议。
  - 特性: 发送数据前无需建立连接，直接发送。不保证数据包的送达和顺序，但保留了消息边界。开销小，传输效率高，并支持广播和多播。
  - 场景: 视频直播、在线游戏、DNS查询等对实时性要求高、可容忍少量丢包的场景。
- socket.SOCK_RAW
  - 含义: 原始套接字。它允许应用程序直接访问底层网络协议（如 ICMP, IGMP），可以处理普通的 SOCK_STREAM 或 SOCK_DGRAM 无法处理的网络报文，甚至允许用户自己构造 IP 数据包的头部。
  - 场景: 网络诊断工具（如 ping、traceroute）、网络嗅探器等需要深度网络操作的开发。

### proto (协议编号)

这个参数用于指定具体的协议。

- 默认值 0: 在绝大多数情况下，你不需要手动指定这个参数，保持默认值 0 即可。
- 自动匹配: 当 proto=0 时，操作系统会根据你选择的 family 和 type 自动匹配最合适的默认协议。例如，当 type 为 SOCK_STREAM 时，系统会自动选择 TCP 协议；当 type 为 SOCK_DGRAM 时，则选择 UDP 协议。
- 手动指定: 只有在一些特殊场景下，比如使用 SOCK_RAW 创建原始套接字时，才需要显式地指定协议编号（例如 socket.IPPROTO_ICMP）。

### fileno (文件描述符)

这是一个高级选项，用于从现有的套接字创建一个 Python 套接字对象。

- 含义: fileno 参数接受一个已有的套接字文件描述符（一个整数）。当你从其他库或系统调用中获得了一个套接字，并希望用 Python 的 socket 对象来操作它时，可以使用这个参数。
- 场景: 通常用于与 C 语言扩展交互或处理通过 subprocess 等方式传递的套接字。在常规的 Python 网络编程中很少用到。

> - 文件描述符：在 Linux/Unix 系统（Python 常运行的环境）中，“一切皆文件”。Socket 本质上也是一个文件描述符（File Descriptor），你可以像读写文件一样读写 Socket。
> - 阻塞与非阻塞：默认的 Socket 是阻塞的（例如 accept() 和 recv() 会卡住程序等待数据）。在开发高并发服务器（如聊天室）时，通常会结合 select、epoll 或使用 asyncio 库将 Socket 设置为非阻塞或异步模式。

## UDP 代码示例

```python
# udp_server.py
import socket

# --- UDP 服务器端 ---
def udp_server():
    # 创建UDP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定地址和端口
    server_socket.bind(('0.0.0.0', 9999))
    print("UDP服务器已启动，等待消息...")

    while True:
        # 接收数据和客户端地址
        data, client_addr = server_socket.recvfrom(1024) # 缓冲区大小1024字节
        print(f"收到来自 {client_addr} 的消息: {data.decode()}")

        # 向客户端回复消息
        server_socket.sendto(b"ACK: Message Received", client_addr)

if __name__ == '__main__':
    udp_server()
```

```python
# udp_client.py
import socket
# --- UDP 客户端 ---
def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = ('127.0.0.1', 9999)

    # 发送消息
    client_socket.sendto(b"Hello, UDP Server!", server_addr)

    # 接收回复
    response, _ = client_socket.recvfrom(1024)
    print(f"收到服务器回复: {response.decode()}")

    client_socket.close()

if __name__ == '__main__':
    udp_client()
```

## TCP 代码示例

```python
# tcp_server.py
import socket

# --- TCP 服务器端 ---
def tcp_server():
    # 创建TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 允许端口复用，防止重启时报"Address already in use"错误
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定地址和端口
    server_socket.bind(('0.0.0.0', 8888))
    # 开始监听， backlog参数指定等待连接队列的最大长度
    server_socket.listen(5)
    print("TCP服务器已启动，等待连接...")

    while True:
        # 接受客户端连接，返回一个新的套接字和客户端地址
        client_socket, client_addr = server_socket.accept()
        print(f"新连接来自: {client_addr}")

        # 与新套接字通信
        data = client_socket.recv(1024)
        print(f"收到消息: {data.decode()}")

        client_socket.send(b"ACK: Message Received")
        client_socket.close()

if __name__ == '__main__':
    tcp_server() # 在一个终端运行
```

```python
# tcp_client.py
import socket

# --- TCP 客户端 ---
def tcp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接服务器
    client_socket.connect(('127.0.0.1', 8888))

    # 发送消息
    client_socket.send(b"Hello, TCP Server!")

    # 接收回复
    response = client_socket.recv(1024)
    print(f"收到服务器回复: {response.decode()}")

    client_socket.close()

if __name__ == '__main__':
    tcp_client() # 在另一个终端运行
```

## 聊天室demo

- 服务器端代码：

```python
import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # 存储所有客户端连接
        self.clients = {}

        print(f"🟢 聊天服务器已在 {host}:{port} 启动")

    def broadcast(self, message, exclude_client=None):
        """向所有客户端广播消息，可选择排除某个客户端"""
        print(f"📢 广播消息: {message.decode('utf-8')}")

        for client_socket, client_name in self.clients.items():
            if client_socket != exclude_client:
                try:
                    client_socket.send(message)
                except Exception as e:
                    print(f"❌ 客户端可能已断开连接: {e}")
                    client_socket.close()
                    del self.clients[client_socket]

    def handle_client(self, client_socket, client_address):
        """处理单个客户端连接的线程函数"""
        try:
            # 获取客户端名称
            client_name = client_socket.recv(1024).decode('utf-8')
            welcome_message = f"✨欢迎 {client_name} 加入聊天室！".encode('utf-8')
            self.clients[client_socket] = client_name

            # 通知所有人新客户端加入
            self.broadcast(f"{client_name} 已加入聊天室！".encode('utf-8'))

            # 持续接收该客户端的消息
            while True:
                try:
                    message = client_socket.recv(1024)
                    if message:
                        # 格式化消息并广播
                        broadcast_message = f"{client_name}: {message.decode('utf-8')}".encode('utf-8')
                        self.broadcast(broadcast_message)
                    else:
                        # 空消息，客户端可能已断开
                        break
                except:
                    # 出错，退出循环
                    break

        except Exception as e:
            print(f"处理客户端 {client_address} 时出错: {e}")
        finally:
            # 客户端离开
            if client_socket in self.clients:
                client_name = self.clients[client_socket]
                del self.clients[client_socket]
                self.broadcast(f"{client_name} 已离开聊天室！".encode('utf-8'))
            client_socket.close()

    def run(self):
        """运行服务器主循环"""
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"接受来自 {client_address} 的连接")

                # 为每个客户端创建新线程
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

        except KeyboardInterrupt:
            print("🔴 服务器关闭")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer('0.0.0.0', 8888)
    server.run()
```

- 客户端代码

```python
import socket
import threading
import sys

class ChatClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """连接到服务器"""
        try:
            self.client_socket.connect((self.host, self.port))
            # 发送用户名
            self.client_socket.send(self.username.encode('utf-8'))
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def receive_messages(self):
        """从服务器接收消息的线程函数"""
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(message)
                else:
                    # 空消息表示连接已关闭
                    print("与服务器的连接已关闭")
                    self.client_socket.close()
                    break
            except Exception as e:
                print(f"接收消息时出错: {e}")
                self.client_socket.close()
                break

    def send_message(self, message):
        """向服务器发送消息"""
        try:
            self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"发送消息时出错: {e}")
            self.client_socket.close()

    def run(self):
        """运行客户端"""
        if not self.connect():
            return

        # 创建接收消息的线程
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        # 主线程处理用户输入
        try:
            while True:
                message = input()
                if message.lower() == 'quit':
                    break
                self.send_message(message)
        except KeyboardInterrupt:
            pass
        finally:
            self.client_socket.close()
            print("已断开连接")

if __name__ == "__main__":
    # 用法: python chat_client.py <username>
    username = sys.argv[1] if len(sys.argv) > 1 else f"User_{hash(threading.get_ident()) % 1000}"
    client = ChatClient('localhost', 8888, username)
    client.run()
```
