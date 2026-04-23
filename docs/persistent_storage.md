# 数据持久化存储

在 [web章节](./network_web_cgi_wsgi_asgi.md)中，提到一条计算机格言：

“**All problems in computer science can be solved by another level of indirection（计算机科学中的所有问题都可以通过增加一个间接层来解决）**” -- David Wheeler（剑桥大学计算机科学教授）

在这章也可以找到一条计算机格言：

“**程序=数据结构+算法**”，由瑞士计算机科学家 尼克劳斯·沃斯（Niklaus Wirth）在其 1976 年出版的经典著作《算法 + 数据结构 = 程序》中提出。

在进行日常软件开发的编码工作中，应该要形成本能地思考：“这块功能要处理什么数据？如何组织这些数据？需要哪些操作？哪种算法最有效？”。 引导自己从 算法 和 数据结构 两个维度切入进行软件设计。

作为最关键的数据以及数据持久化的问题，从计算机科学的演变历程来看，数据存储的本质就是

如何将**内存中的易失性数据（0和1）映射到磁盘上的非易失性介质中**。这个过程经历了从“人读为主为文本类型文件”到“机读为主二进制类型文件”，数据组织从简单 → 结构化 → 高效 → 分布式”进行演变。

在 Python 中，我们处理这些数据的方式也随着格式的演进而变得日益丰富和抽象。按上述演变历程进行梳理和总结。

## 文本数据 Text Data

演变逻辑：从纯字符到具有语义的结构化描述。文本文件的核心优势是通用性和可读性，但往往牺牲了存储空间和解析性能。

### 简单文本文件

纯文本文件，比如 txt、log 这类文件，仅存储纯字符串，无任何结构，适合极简数据。需要注意的是文件编码格式（如 utf-8），写入编码和读取编码不一致会出现乱码。

```python
# 写入纯文本
with open("simple.txt", "w", encoding="utf-8") as f:
    f.write("姓名:张三李四\n年龄:25\n地址:中国浙江省杭州市")

# 读取纯文本
with open("simple.txt", "r", encoding="utf-8") as f:
    data = f.read()
print(data)
```

### 填充式文本文件

在这种格式中，记录中的每个字段都有固定的宽度，如果内容宽度不够，通常会使用空格字符进行填充，使得每行（记录）保持一样的宽度。python语言可以使用`seek()`在文件内跳转，读写所需的记录和字段。此时数据已经有了简单结构，但因为填充的冗余的空格字符，导致数据存储空间和读取性能都比纯文本文件要高，但好处是数据操作方便。

```python
# 写入：姓名(10字符)、年龄(5字符)、城市(15字符)
data = "张三      25   中国浙江省杭州市       "
with open("fixed.txt", "w", encoding="utf-8") as f:
    f.write(data)

# 按位置读取
with open("fixed.txt", "r", encoding="utf-8") as f:
    content = f.read()
name = content[0:10].strip()  # 截取并去空格
age = content[10:15].strip()
city = content[15:30].strip()
print(name, age, city)
```

### 结构化文本文件

对于简单或者填充式的文本文件，其唯一的组织层次就是行。有时候，你希望有更多的结构，表达数据的意义。常见的格式约束有：

- 分隔符（separator）或界定符（delimiter）​，比如制表符（'\t'）​、逗号（','）或竖线（'|'）​。典型文件格式就是逗号分隔值的CSV文件（comma-separated value）就是这种格式。
- 标签周围的'<'和'>'，比如XML和HTML。
- 标点符号，比如JSON。
- 缩进，比如YAML（​“YAML Ain't Markup Language”的递归缩写）​。
- 杂项，比如程序配置文件 .ini 文件。

#### CSV

CSV 格式是一种最常用的数据格式，它将数据存储为行和列，行和列之间用逗号分隔。也称为表格文件格式，excel处理软件和数据库可以直接导入导出 CSV 文件。

```python
import csv

# 写入CSV
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "年龄", "城市"])  # 表头
    writer.writerow(["张三", 25, "北京"])

# 文件的实际内容如下：
# 姓名,年龄,城市
# 张三,25,北京

# 读取CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

#### xml

XML (Extensive Markup Language 可扩展标记语言) 是早期互联网数据交换标准，结构严谨但冗余。

XML 文件的格式如下：

```xml
<users>
  <user>
    <name>张三</name>
    <age>25</age>
    <city>北京</city>
  </user>
</users>
```

python 提供了内置模块 `xml` 来处理 XML 文件。

```python
import xml.etree.ElementTree as ET

# 写入XML
root = ET.Element("users")
user = ET.SubElement(root, "user")
ET.SubElement(user, "name").text = "张三"
ET.SubElement(user, "age").text = "25"
ET.SubElement(user, "city").text = "北京"
tree = ET.ElementTree(root)
tree.write("data.xml", encoding="utf-8")

# 读取XML
tree = ET.parse("data.xml")
root = tree.getroot()
print(root.find("user/name").text)
```

#### json

JSON (JavaScript Object Notation) 是一种数据格式规范，它基于 JavaScript 语言，但与 JavaScript 不同的是，JSON 是一种数据格式，而不是一种编程语言。

JSON 的数据结构非常简单，它基于键值对。是当前最主流文本格式，Python 字典数据结构直接映射，无冗余。

JSON 文件的格式如下：

```json
{
  "name": "张三",
  "age": 25,
  "city": "北京"
}
```

python 模块 `json` 可以处理 JSON 文件。

```python
import json

# 写入JSON
data = {"name": "张三", "age": 25, "city": "北京"}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 读取JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data["name"])
```

#### yaml

YAML（YAML Ain’t a Markup Language）是一种可读性极高的数据序列化格式，常用于配置文件和数据交换。它通过缩进表示层级关系，支持对象、数组和纯量三种数据结构，语法简洁且易于手工编辑。

YAML 文件的格式如下：

```yaml
server:
  host: 127.0.0.1
  port: 8080
users:
  - name: Tom
    role: admin
  - name: Jerry
    role: user
features:
  logging: true
  cache_size: 256
```

python 模块 `yaml` 可以处理 YAML 文件。

```python
import yaml

# 写入YAML
data = {"name": "张三", "age": 25, "city": "北京"}
with open("data.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True)

# 读取YAML
with open("data.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
    print(data)
```

#### toml

TOML（Tom’s Obvious, Minimal Language）是一种简洁、可读性强的配置文件格式，由 GitHub 前 CEO Tom Preston-Werner 于 2013 年创建，设计目标是语义清晰且能无歧义映射为哈希表结构。它常被用于替代 JSON、YAML 和 INI，广泛应用于 Rust Cargo、Python Poetry、Hugo 等项目。

Toml 文件的格式如下：

```toml
# 应用配置
[app]
name = "我的应用"
version = "1.0.0"
debug = false
# 数据库配置
[database]
url = "postgresql://user:pass@localhost:5432/db"
pool_size = 10
# 嵌套表格
[servers.alpha]
ip = "10.0.0.1"
dc = "east"
# 表格数组
[[products]]
name = "Hammer"
price = 29.99
[[products]]
name = "Nail"
price = 2.99"
```

python 模块 `toml` 可以处理 TOML 文件。

```python
import toml

# 写入TOML
data = {"name": "张三", "age": 25, "city": "北京"}
with open("data.toml", "w", encoding="utf-8") as f:
  toml.dump(data, f)

# 读取TOML
with open("data.toml", "r", encoding="utf-8") as f:
  data = toml.load(f)
  print(data)
```

## 二进制数据 Binary Data

演变逻辑：追求极致的性能、空间效率以及复杂对象的还原。二进制文件对人类不可读（乱码），但对机器极其高效。

### 简单的二进制文件

直接存储原始的字节数据，速度最快，适合图片、音频、原始数据。

Python 使用 `open()` 函数配合 `b` (代表二进制) 模式操作二进制数据。

```python
# 写入二进制
data = b"hello binary"  # bytes 类型
with open("simple.bin", "wb") as f:
    f.write(data)

# 读取二进制
with open("simple.bin", "rb") as f:
    data = f.read()
print(data)
```

### 填充式二进制文件

二进制版固定格式，用字节填充字段，比文本更快更小。按照 C 语言的结构体方式，将整数、浮点数紧密排列，没有分隔符。

Python 处理: struct 模块。它可以将 Python 数值打包成字节流，也可以解包。

```python
import struct

# 打包：10字节字符串 + 4字节整数 + 15字节字符串
data = struct.pack("10sI15s", b"张三", 25, b"北京")
with open("fixed.bin", "wb") as f:
    f.write(data)

# 解包
with open("fixed.bin", "rb") as f:
    data = f.read()
name, age, city = struct.unpack("10sI15s", data)
print(name.decode().strip(), age, city.decode().strip())
```

### 结构化二进制文件

复杂的结构化数据，比较 python 语言中的数据结构字段、对象、函数等存储。通常涉及到数据序列化和反序列化：

- 序列化（Serialization）是将数据结构或对象状态转换为一个可以存储或传输的格式的过程。这意味着我们可以将复杂的数据结构转换为简单的字节流或字符串，以便于存储或传输。
- 反序列化（Deserialization）则是将这些数据恢复为其原始形式的过程。

python 模块 `pickle` 是专用的序列化和反序列化工具包，能够处理几乎任何 Python 对象（类实例、函数等）。

```python
import pickle

data = {"key": "value"}
# 序列化 (Dump)
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# 反序列化 (Load)
with open("data.pkl", "rb") as f:
    loaded_data = pickle.load(f)
```

其它结构化二进制数据，比如 excel 文件（.xlsx）、word 文件（.docx）、pdf 文件（.pdf）等等，这类文件通常使用第三模块来处理，比如：

- `openpyxl` 模块处理 Excel 文件。
- `docx` 模块处理 Word 文件。
- `pdfplumber` 模块处理 PDF 文件。

```python
import openpyxl  # 需安装：pip install openpyxl

# 写入Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["姓名", "年龄"])
ws.append(["张三", 25])
wb.save("data.xlsx")

# 读取Excel
wb = openpyxl.load_workbook("data.xlsx")
ws = wb.active
print(ws.cell(row=2, column=1).value)
```

## 数据库系统 Database System

当数据量超越单机文件处理能力，且需要并发访问、事务安全和复杂查询时，数据库成为必然选择。

### 关系型数据库 (RDBMS)

- 代表: SQLite, MySQL, PostgreSQL。
- 特点: 结构化查询语言 (SQL)，强一致性，表与表之间有关联。
- Python 处理: sqlite3 (内置), mysql-connector。

```python
import sqlite3

# 连接+建表
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user (name TEXT, age INT)")

# 写入
cursor.execute("INSERT INTO user VALUES (?, ?)", ("张三", 25))
conn.commit()

# 查询
cursor.execute("SELECT * FROM user")
print(cursor.fetchall())

conn.close()
```

### 非关系型数据库 (NoSQL)

- 代表：MongoDB (文档型) 直接存储类似 JSON 的 BSON 文档; Redis (内存存储的键值对/缓存)。
- 特点：无固定表结构，数据结构灵活，适合需要高并发读写的大数据、分布式场景
- Python 处理: pymongo (MongoDB), redis (Redis)。

```python
from pymongo import MongoClient  # pip install pymongo

# 连接
client = MongoClient("mongodb://localhost:27017/")
db = client["test_db"]
collection = db["user"]

# 写入
data = {"name": "张三", "age": 25}
collection.insert_one(data)

# 查询
print(collection.find_one({"name": "张三"}))
```

## 总结

| 数据层级 | 格式类型              | Python 核心库/工具                | 适用场景                     | 优点                  | 缺点                        |
| :------- | :-------------------- | :-------------------------------- | :--------------------------- | :-------------------- | :-------------------------- |
| 文本     | 简单/Padding          | `open()`, `struct`                | 日志、配置、老式数据交换     | 极简、人可读          | 解析繁琐、无结构            |
| 文本     | 结构化 (CSV/JSON/XML) | `csv`, `json`, `pandas`, `pyyaml` | Web API、数据交换、报表      | 通用性强、跨语言      | 体积大、解析慢于二进制      |
| 二进制   | 简单/Struct           | `open()`, `struct`                | 图片、音频、底层协议         | 紧凑、极速            | 人不可读、依赖格式定义      |
| 二进制   | 序列化 (Pickle/Excel) | `pickle`, `pandas`                | Python 内部缓存、办公文档    | 保存复杂对象 (Pickle) | 安全风险 (Pickle)、依赖库多 |
| 数据库   | 关系型 (SQL)          | `sqlite3`, `SQLAlchemy`           | 核心业务数据、金融系统       | 强一致性、复杂查询    | 扩展性受限、部署较重        |
| 数据库   | 非关系型 (NoSQL)      | `pymongo`, `redis`                | 缓存、海量日志、非结构化数据 | 高性能、灵活扩展      | 事务支持较弱 (部分)         |
