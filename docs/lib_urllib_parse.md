# URL

## URI / URL / URN

URI = Uniform Resource Identifier 统一资源标志符
URL = Uniform Resource Locator 统一资源定位符
URN = Uniform Resource Name 统一资源名称

看了全称大概也不好理解三者的区别。

在互联网上，一个文件，一张图片、一段语音都可以被称为一种资源，那服务器上海量的资源，如何快速找到它呢？不管用什么方法表示，只要能唯一标识一个资源，这个标识符 Identifier 就叫URI。

通常会有两种方法来实现定位，一种是用 URL 地址定位；另一种是用 URN 名称定位。

举个例子：去村子找个具体的人（URI），如果用地址：某村多少号房子第几间房的主人就是URL， 如果用身份证号+名字 去找就是URN了。

所以这三者概念上的关系是 uri 包括 url 和 urn。URI 只是一个抽象的定义，URL 和 RNN 是具体实现。

```
+------------------------------------------------+
|                                                |
|  URI(Uniform Resource Identifier)              |
|                                                |
|   +--------------------------------------+     |
|   |                                      |     |
|   | URL(Uniform Resource Locator)        |     |
|   | eg:ftp://192.168.0.111/index.html    |     |
|   | eg:https://blog.csdn.net/index.html  |     |
|   |                                      |     |
|   +--------------------------------------+     |
|                                                |
|   +---------------------------------------+    |
|   | URN(Uniform Resource Name)            |    |
|   | eg:isbn:7-5387-1705-6                 |    |
|   |                                       |    |
|   +---------------------------------------+    |
|                                                |
+------------------------------------------------+

```

只是在互联网上 urn 没流行起来，导致几乎目前所有的 uri 都是以 url 形式表示，比如定位服务器上的一个文件，如果是在本地环境下，可以使用 `ftp://192.168.0.111/index.html`，如果是在 web 环境下，可以使用 `https://blog.csdn.net/index.html`。

但是在现实场景中，urn 却被广泛使用，比如图书的 ISBN 编码就是 urn 的例子 `isbn:7-5387-1705-6`。

> 国际标准书号（International Standard Book Number），简称ISBN，是专门为识别图书等文献而设计的国际编号.2007年1月1日之前，ISBN由10位数字组成，分四个部分：组号（国家、地区、语言的代号），出版者号，书序号和检验码。中国的组号为7.

## URL 格式

通常情况下，一个 URL 是一个特定格式的字符串，它包含多个部分。基本格式如下：

```
scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]

```

每一部分表示的名称如下：

```
"  https:   //    user   :   pass   @ sub.example.com : 8080   /p/a/t/h  ?  query=string   #fragment "
│          │  │          │          │                 │      │          │ │              │           │
│ scheme   │  │ username │ password │    hostname     │ port │ path     │ │    query     │ fragment  │
└──────────┴──┴──────────┴──────────┴────────────────────────┴──────────┴─┴──────────────┴───────────┘
```

## urllib.parse 模块

python 中内置的标准库 urllib.parse 模块，专门用于对 URL 字符串进行解析、构建、编码和解码等操作。它提供了一系列函数，让你能轻松地处理 URL 的各个组成部分。

主要分为三大类功能：

- 解析与构建
- 编码与解码
- 查询参数处理

## 解析和构建

urllib.parse 模块提供了 `urlparse / urlunparse / urlsplit / urlunsplit` 函数，将一个完整 URL 字符串拆解成多个部分。

```python
from urllib.parse import urlsplit, urlunsplit

# 1. 解析 URL
url = "https://admin:secret@www.example.com:8080/path/to/file?query=1#top"
result = urlsplit(url)

print("--- 核心字段 ---")
print(f"scheme  : {result.scheme}")   # https
print(f"netloc  : {result.netloc}")   # admin:secret@www.example.com:8080
print(f"path    : {result.path}")     # /path/to/file
print(f"query   : {result.query}")    # query=1
print(f"fragment: {result.fragment}") # top

print("\n--- 辅助属性 ---")
print(f"username: {result.username}") # admin
print(f"password: {result.password}") # secret
print(f"hostname: {result.hostname}") # www.example.com
print(f"port    : {result.port}")     # 8080

print("\n--- 获取原始 URL ---")
print(result.geturl())
# https://admin:secret@www.example.com:8080/path/to/file?query=1#top

# 2. 构建 URL
parts = ('https', 'www.example.com', '/path', '', 'query=arg', 'fragment')
constructed_url = urlunsplit(parts)
print(constructed_url)
# https://www.example.com/path?query=arg#fragmen
```

`SplitResult` 是 `urllib.parse.urlsplit()` 函数返回的对象类型。它是一个命名元组（Named Tuple），包含 5 个核心字段（对应 URL 的 5 个部分），以及 4 个辅助属性。同时，还有两个特有的方法：`geturl()` 和 `_asdict()`

- `geturl()` 方法返回一个字符串，表示当前 SplitResult 对象所代表的 URL。
- `_asdict()` 方法将 `SplitResult` 的具名元组对象转成字典，包含当前 SplitResult 对象的所有字段。

## （`urlparse/urlunparse` 和 `urlsplit/urlunsplit`）区别

这两对函数（`urlparse/urlunparse` 和 `urlsplit/urlunsplit`）的核心区别在于对 URL 中“参数（params）”的处理方式，而这背后反映了 URL 标准（RFC）的演进历史。

回溯到互联网早期的标准：

1. 早期标准 (RFC 1738 / RFC 1808)：在早期的 URL 规范(RFC 1738 / RFC 1808)中，定义了一种名为 params 的组件。它紧跟在路径（path）之后，用分号 ; 分隔。结构：`scheme://netloc/path;params?query#fragment`，`urlparse` 就是为了兼容这个旧标准而设计的，它会尝试把 `;` 后面的内容单独提取出来。
1. 现代标准 (RFC 2396 及后续 RFC 3986)：随着 Web 的发展，新的标准（如 RESTful API）不再推荐使用路径参数（params），或者说分号 `;` 在路径中更多地被视为路径本身的一部分，而不是参数的分隔符。`urlsplit` 是为了适应这种更现代的 URL 语法而引入的。它不再尝试分割 params，而是将其视为 path 的一部分。

所以 `urlparse` (6元组): 返回 `ParseResult`。它包含 `params` 字段（索引为 3），`urlsplit` (5元组): 返回 `SplitResult`。它不包含 `params` 字段，原本属于 `params` 的内容会被直接归入 `path`。

```python
from urllib.parse import urlparse, urlsplit

url = "http://example.com/path/to/file;sessionid=123?query=1#top"

# 使用 urlparse (兼容旧标准)
parsed = urlparse(url)
print(f"urlparse path:   {parsed.path}")    # 输出: /path/to/file
print(f"urlparse params: {parsed.params}")  # 输出: sessionid=123

# 使用 urlsplit (现代标准)
splitted = urlsplit(url)
print(f"urlsplit path:   {splitted.path}")  # 输出: /path/to/file;sessionid=123
# urlsplit 没有 params 属性
```

Python 官方文档也指出，除非你需要专门处理路径分段参数，否则通常应该使用 `urlsplit()` 替代 `urlparse()`。大多数时候我们根本不关心 params 字段，使用 `urlsplit` 返回的结构更符合直觉。

## `urljoin`

这个函数非常实用，它能智能地将一个基础 URL 和一个相对 URL 合并成一个绝对 URL。这在处理网页中的相对链接时尤其方便。

```python
from urllib.parse import urljoin

base = 'https://example.com/path/to/page/'

# 合并相对路径
print(urljoin(base, 'subpage'))           # https://example.com/path/to/page/subpage
# 合并绝对路径
print(urljoin(base, '/absolute/path'))    # https://example.com/absolute/path
# 向上导航
print(urljoin(base, '../parent'))         # https://example.com/path/to/parent
# 添加查询参数
print(urljoin(base, '?query=value'))      # https://example.com/path/to/page/?query=value
```

## 编码和解码

- `quote(string, ...)`: 对字符串进行 URL 编码（也称百分号编码）。它会将空格、中文、特殊符号等转换为 % 后跟两位十六进制的形式。例如，空格通常被编码为 %20。
- `unquote(string, ...)`: `quote()` 的逆操作，将已编码的 URL 字符串解码回原始字符串。

```python
from urllib.parse import quote, unquote

text = 'Hello World! 你好'
encoded = quote(text)
print(encoded)   # Hello%20World%21%20%E4%BD%A0%E5%A5%BD

decoded = unquote(encoded)
print(decoded)   # Hello World! 你好
```

## query 查询参数的处理

提供了以下函数专门用于处理 URL 中 `?` 后面的查询字符串（query）部分。

- `urllib.parse.urlencode()` 方法可以将字典对象转换成查询参数字符串。这是构建 GET 请求参数或 POST 表单数据（application/x-www-form-urlencoded ）时的常用操作。
- `urllib.parse.parse_qs()` 方法可以将查询参数字符串转换成字典对象。这是解析 GET 请求参数或 POST 表单数据（application/x-www-form-urlencoded ）时常用的操作。
- `parse_qsl(query_string)`: 将查询字符串解析成一个由 (键, 值) 元组组成的列表。

```python

from urllib.parse import urlencode, parse_qs, parse_qsl

params = {'name': 'Alice', 'age': 30, 'city': 'New York'}
query_string = urlencode(params)
print(query_string) # name=Alice&age=30&city=New+York


query = 'name=Alice&age=30&hobby=reading&hobby=coding'

# 解析为字典
qs_dict = parse_qs(query)
print(qs_dict)
# {'name': ['Alice'], 'age': ['30'], 'hobby': ['reading', 'coding']}

# 解析为列表
qs_list = parse_qsl(query)
print(qs_list)
# [('name', 'Alice'), ('age', '30'), ('hobby', 'reading'), ('hobby', 'coding')]
```
