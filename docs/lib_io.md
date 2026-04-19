# I/O 操作

Python 的 io 模块是处理各种输入/输出操作的基石，它提供了一套统一的抽象，它将所有输入输出（文件、内存、网络套接字等）都视为“流”（stream）或“类文件对象”（file-like object）。这使得我们可以用同一套 `read()`、`write()` 等接口来操作不同来源和去向的数据。

## 文件对象

对外暴露有 `read()`、`write()`、`seek()` 等方法的资源的对象都可以称为文件对象 `file object`。

- 根据其创建方式的不同，文件对象可以是真实磁盘文件、其他类型的存储或通信设备的访问（例如标准输入/输出、内存缓冲区、套接字、管道等）。 文件对象也被称为流 stream，类似 Node.js 中的流的概念。
- 根据内容类型的不同，可以分为三种类别的文件对象：文本文件 StringIO、二进制字节文件 BytesIO（进一步分为：原始的二进制文件、缓冲二进制文件）。

## 文件描述符

文件描述符（File Descriptor）是操作系统为每个打开的文件（真实的磁盘文件，标准输入输出、内存缓存区、网套接字、管道等）分配的编号，用于引用一个打开的文件（I/O流）。用户进程可以通过文件描述符来操作文件。

现代操作系统不允许普通的程序直接操作磁盘，所以，读写文件就是请求操作系统打开一个文件对象（通常称为文件描述符），然后通过操作系统提供的接口从这个文件对象中读取数据（读文件），或者把数据写入这个文件对象（写文件）。 所以文件描述符的创建和销毁都由操作系统完成，用户进程无法直接创建和销毁文件描述符。

文件描述符是一个小型的整数，对应于当前进程所打开的文件。例如，标准输入的文件描述符通常是0，标准输出是1，标准错误是2。之后被进程打开的文件的文件描述符会被依次指定为3，4，5等。

可以通过 `fileno()` 方法返回当前流的 文件描述符。

## io 模块

`io` 模块核心类的继承关系

```
 IOBase (所有 I/O 类的根类)                       定义了所有流对象的基本行为，比如 close(), readable(), writable(), seekable()。它本身不能被实例化。
   │
   ├── RawIOBase (原始 I/O 基类)                 定义了所有原始 I/O 类的基本行为，比如 read(), write(), flush(), seek(), tell()。它本身不能被实例化。
   │   │
   │   └── FileIO (文件I/O)                      直接与操作系统的文件描述符打交道
   │
   ├── BufferedIOBase (缓冲 I/O 基类)
   │   │
   │   ├── BufferedReader (缓冲读取)             负责分批读取数据入到内存中，避免一次性加载大数据到内存中。
   │   ├── BufferedWriter (缓冲写入)             负责把数据暂存在内存里，凑够一波再写入操作（比如写入硬盘、标准输出等），大大减少系统调用次数。
   │   ├── BufferedRWPair (成对缓冲)
   │   └── BytesIO (内存中的二进制流)             直接在内存里模拟一个二进制文件，不需要底层硬盘文件，速度极快。
   │
   └── TextIOBase (文本 I/O 基类)
       │
       ├── TextIOWrapper (核心包装器：解码/换行处理) 这是 open(..., encoding='utf-8') 返回的那个对象，负责把底层的 bytes 解码成 str，并处理换行符（\n vs \r\n）
       └── StringIO (内存中的文本流)               直接在内存里模拟一个文本文件。

(具体实现层 - 实际使用)
```

## 文件操作的底层实现

当你使用内置的 open() 函数时，Python 实际上是在幕后为你组合了 io 模块中的这些类。

- 文本模式 (`open('file.txt', 'r', encoding='utf-8')`)：会返回一个 `io.TextIOWrapper` 对象，它包裹着一个 io.BufferedReader，而 BufferedReader 又包裹着一个 io.FileIO 对象。
- 二进制模式 (`open('file.jpg', 'rb')`)：open() 会返回一个 `io.BufferedReader` 对象，它直接包裹着 io.FileIO。

## String IO 和 Bytes IO

很多时候，数据读写不一定是直接的磁盘文件，也可以在内存中读写。

- StringIO 就是在内存中读写文本内容
- BytesIO 就是在内存中读写二进制内容

StringIO：用于在内存中操作文本数据（str）。你可以像操作普通文件一样对它进行读写。

```python
import io

# 创建一个 StringIO 对象
text_stream = io.StringIO()

# 写入文本
text_stream.write("Hello, World!\n")
text_stream.write("这是一行中文。")

# 移动指针到开头
text_stream.seek(0)

# 读取所有内容
print(text_stream.read())
text_stream.close()
```

BytesIO：用于在内存中操作二进制数据（bytes）。处理图片、音频或网络数据包时经常用到它。

```python
import io
# 创建一个 BytesIO 对象
binary_stream = io.BytesIO()

# 写入二进制数据
binary_stream.write(b"\x00\x01\x02")
binary_stream.write("中文".encode('utf-8'))

# 获取缓冲区的全部内容
print(binary_stream.getvalue())
binary_stream.close()
```

网络套接字（socket）本身也可以看作一个字节流，用 io.BufferedReader 包装以获得缓冲能力，再用 io.TextIOWrapper 包装以自动处理文本解码。

```python
import io
import socket

# 假设 client_socket 是一个已建立的 socket 连接
# client_socket, _ = server_socket.accept()

# 1. 获取原始流
raw_stream = client_socket.makefile('rb', buffering=0)

# 2. 包装成缓冲流，提高读取效率
buffered_stream = io.BufferedReader(raw_stream)

# 3. 包装成文本流，自动解码
text_stream = io.TextIOWrapper(buffered_stream, encoding='utf-8')

# 现在可以直接像读取文件一样从网络流中读取文本
# line = text_stream.readline()
```

## 方法总结

io 模块中核心类的方法与属性总结，可以将它们分为了三个层级：基类（通用接口）、二进制流（处理 bytes） 和 文本流（处理 str）。

通用基类 (IOBase)：这是所有 I/O 类的“祖先”，定义了文件对象最基本的行为（如关闭、检查状态）。

| 方法/属性     | 说明                                                | 适用范围 |
| :------------ | :-------------------------------------------------- | :------- |
| `close()`     | 关闭流并释放系统资源。                              | 所有流   |
| `seekable()`  | 返回 `True` 如果流支持随机访问（即支持 `seek()`）。 | 所有流   |
| `readable()`  | 返回 `True` 如果流可以被读取。                      | 所有流   |
| `writable()`  | 返回 `True` 如果流可以被写入。                      | 所有流   |
| `isatty()`    | 返回 `True` 如果流是交互式的终端（TTY）。           | 所有流   |
| `__enter__()` | 支持 `with` 语句上下文管理器。                      | 所有流   |
| `__exit__()`  | 支持 `with` 语句上下文管理器。                      | 所有流   |

二进制流 (Raw & Buffered)，直接操作系统底层，无缓冲。

| 方法/属性       | 说明                              | 备注                       |
| :-------------- | :-------------------------------- | :------------------------- |
| `read(size=-1)` | 从流中读取最多 `size` 个字节。    | `size=-1` 表示读取全部     |
| `readinto(b)`   | 将字节读入预分配的缓冲区 `b` 中。 | 减少内存拷贝，高性能场景用 |
| `write(b)`      | 将字节 `b` 写入流中。             | 返回写入的字节数           |

缓冲 I/O (BufferedIOBase -> BufferedReader, BytesIO)，提供缓冲机制，提升性能或在内存中模拟文件。

| 方法/属性        | 说明                                           | 适用范围                   |
| :--------------- | :--------------------------------------------- | :------------------------- |
| `read(size=-1)`  | 读取字节。如果底层是原始流，这里会先查缓冲区。 | 缓冲流                     |
| `read1(size=-1)` | 调用底层原始流的 `read` 方法，最多一次。       | 缓冲流特有                 |
| `write(b)`       | 写入字节到缓冲区。                             | 缓冲流                     |
| `getvalue()`     | 特有方法。返回缓冲区中的全部内容（字节）。     | 仅限 `BytesIO`             |
| `detach()`       | 分离底层原始流并返回它。                       | 包装类 (如 BufferedReader) |

文本流 (TextIOBase)，这一层处理的是 字符串 (str) 数据，负责编码解码。

| 方法/属性                | 说明                                              | 备注                                 |
| :----------------------- | :------------------------------------------------ | :----------------------------------- |
| `read(size=-1)`          | 读取字符串。                                      | 返回 `str`                           |
| `write(s)`               | 写入字符串。                                      | 返回写入的字符数                     |
| `readline(size=-1)`      | 读取一行（直到遇到换行符）。                      | 文本流常用                           |
| `readlines(hint=-1)`     | 读取所有行并返回列表。                            | `hint` 用于限制总字符数              |
| `writelines(lines)`      | 将字符串列表写入流。                              | 注意：不会自动添加换行符             |
| `seek(offset, whence=0)` | 移动文件指针。                                    | 文本流通常只支持从开头定位           |
| `tell()`                 | 返回当前文件指针的位置。                          | 返回的是不透明数字（通常指字节偏移） |
| `detach()`               | 分离底层的缓冲二进制流。                          | 仅限 `TextIOWrapper`                 |
| `encoding`               | 属性：获取当前使用的编码格式（如 'utf-8'）。      | 仅限 `TextIOWrapper`                 |
| `errors`                 | 属性：获取错误处理策略（如 'strict', 'ignore'）。 | 仅限 `TextIOWrapper`                 |
| `newlines`               | 属性：查看已读取的换行符类型。                    | 仅限 `TextIOWrapper`                 |
