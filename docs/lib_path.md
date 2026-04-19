# Path 文件路径

## 演进历史：从字符串到面向对象

Python 的文件路径处理的方式经历了一个从“字符串拼接”到“面向对象”的演进过程。主要经历了三个阶段的演变：

1. 早期阶段（字符串拼接时代）：
   - 在 Python 早期，开发者主要通过字符串拼接来处理路径。这种方式非常脆弱，因为 Windows 使用反斜杠 \，而 Unix-like 系统（Linux/macOS）使用正斜杠 /。手动拼接字符串（如 dir + "/" + file）会导致严重的跨平台兼容性问题。

2. os.path 时代（过程式抽象）：
   - 为了解决跨平台问题，Python 引入了 os.path 模块。它提供了一系列函数（如 os.path.join）来自动处理不同操作系统的路径分隔符。这是很长一段时间内的标准做法，但它本质上是基于字符串的操作，代码往往显得冗长，且缺乏面向对象的直观性。

3. pathlib 时代（面向对象现代化）：
   - 从 Python 3.4 开始，标准库引入了 pathlib 模块。它将文件路径视为对象（Path 类），而不是简单的字符串。这是目前官方推荐的现代方式，它通过重载运算符（如 /）让路径拼接变得极其优雅，并提供了丰富的方法来完成文件系统的各种操作。

## pathlib 核心架构

很多开发者只知道 Path，但 pathlib 其实有一套严谨的类继承体系。理解这个体系，你才能明白为什么它既能处理字符串，又能操作硬盘。

pathlib 将路径操作分为了两类：

- 纯路径操作 (Pure Paths)：只处理字符串逻辑，不触碰硬盘。
- 具体路径操作 (Concrete Paths)：既处理字符串，也能调用系统 API 操作硬盘。

```
PurePath：所有路径类的基类，仅用于路径字符串的解析和拼接，不涉及 IO 操作。
  - PurePosixPath：Unix/Linux/macOS 风格
  - PureWindowsPath：Windows 风格。
Path：最常用。自动适配当前系统， 继承自 PurePath。实现文件 IO 操作（读写、创建、删除等操作）。
  - PosixPath
  - WindowsPath
```

> 当你写 Path('...') 时，Python 会自动根据操作系统实例化为 PosixPath 或 WindowsPath。但如果你需要处理跨平台路径字符串（例如在 Linux 服务器上解析一个 Windows 格式的路径字符串），你可以强制使用 PureWindowsPath('C:\\Users\\...')，而无需真正拥有那个文件。

## pathlib 常用操作

pathlib 的对象是不可变的。修改路径不会改变原对象，而是返回一个新的 Path 对象。

### 基础构造与拼接

| 方法/属性    | 描述                             | 示例代码                            | 返回值类型                 |
| :----------- | :------------------------------- | :---------------------------------- | :------------------------- |
| `Path()`     | 创建路径对象（自动适配系统）     | `p = Path('/home/user')`            | `PosixPath 或 WindowsPath` |
| `PurePath()` | 仅处理路径字符串，不触碰硬盘     | `p = PurePath('dir/file')`          | PurePath 对象              |
| `/` 运算符   | 最核心用法，拼接路径             | `new_p = p / 'subdir' / 'file.txt'` | Path 对象                  |
| `joinpath()` | 类似 `/`，用于多次拼接           | `p.joinpath('a', 'b') `             | Path 对象                  |
| `as_posix()` | 强制转换为 Unix 风格字符串 (`/`) | `p.as_posix() `                     | str                        |

### 属性访问（获取信息）

| 方法/属性   | 描述                       | 示例 (`p = Path('/data/archive.tar.gz')`)                  | 返回值    |
| :---------- | :------------------------- | :--------------------------------------------------------- | :-------- |
| `.name`     | 获取文件名（含后缀）       | `p.name` → `'archive.tar.gz'`                              | str       |
| `.stem`     | 获取文件名（不含后缀）     | `p.stem` → `'archive.tar'`                                 | str       |
| `.suffix`   | 获取文件扩展名             | `p.suffix` → `'.gz'`                                       | str       |
| `.suffixes` | 获取所有扩展名列表         | `p.suffixes` → `['.tar', '.gz'] `                          | list      |
| `.parent`   | 获取父目录                 | `p.parent` → `PosixPath('/data') `                         | Path 对象 |
| `.parents`  | 获取所有祖先目录（可迭代） | `list(p.parents)` → `[PosixPath('/data'), PosixPath('/')]` | sequence  |
| `.parts`    | 将路径拆分为元组           | `p.parts` → `('/', 'data', 'archive.tar.gz')`              | tuple     |
| `.anchor`   | 获取根目录部分             | `p.anchor` → `'/'`                                         | str       |

### 修改路径（返回新对象）

| 方法/属性       | 描述           | 示例代码                      | 注意                   |
| :-------------- | :------------- | :---------------------------- | :--------------------- |
| `with_name()`   | 替换文件名     | `p.with_name('new_file.txt')` | 仅替换名字，不改变目录 |
| `with_suffix()` | 替换后缀       | `p.with_suffix('.zip')`       | 若后缀不存在则添加     |
| `with_stem()`   | 替换文件名主干 | `p.with_stem('backup')`       | Python 3.9+            |

### 文件系统操作（IO与状态）

| 方法/属性      | 描述               | 示例代码              | 常用参数                                                |
| :------------- | :----------------- | :-------------------- | :------------------------------------------------------ |
| `exists()`     | 检查路径是否存在   | `p.exists()`          | 无                                                      |
| `is_file()`    | 检查是否为文件     | `p.is_file()`         | 无                                                      |
| `is_dir()`     | 检查是否为目录     | `p.is_dir()`          | 无                                                      |
| `is_symlink()` | 检查是否为符号链接 | `p.is_symlink()`      | 无                                                      |
| `mkdir()`      | 创建目录           | `p.mkdir()`           | `parents=True` (递归创建), `exist_ok=True` (存在不报错) |
| `rmdir()`      | 删除\**空*目录     | `p.rmdir()`           | 无                                                      |
| `unlink()`     | 删除文件           | `p.unlink()`          | missing_ok=True (文件不存在不报错)                      |
| `rename()`     | 重命名或移动       | `p.rename(new_path)`  | 目标路径可以是字符串或Path对象                          |
| `replace()`    | 强制重命名/移动    | `p.replace(new_path)` | 如果目标存在，会覆盖它                                  |

### 文件内容读写（简化IO）

| 方法/属性       | 描述           | 示例代码                  | 常用参数                       |
| :-------------- | :------------- | :------------------------ | :----------------------------- |
| `read_text()`   | 读取文本内容   | `content = p.read_text()` | `encoding='utf-8' `            |
| `write_text()`  | 写入文本内容   | `p.write_text('Hello')`   | `encoding='utf-8'`, `mode='w'` |
| `read_bytes()`  | 读取二进制内容 | `data = p.read_bytes()`   | 无                             |
| `write_bytes()` | 写入二进制内容 | `p.write_bytes(data) `    | 无                             |

### 遍历与查找

| 方法/属性   | 描述                   | 示例代码                        | 说明                              |
| :---------- | :--------------------- | :------------------------------ | :-------------------------------- |
| `iterdir()` | 遍历当前目录下的所有项 | `for child in p.iterdir(): ...` | 类似 `ls`，只遍历一层             |
| `glob()`    | 模式匹配查找           | `p.glob('.py') `                | 不递归，通配符 ``, ?, [] `        |
| `rglob()`   | 递归模式匹配查找       | `p.rglob('.py')`                | 相当于 `\*_/_.py`，遍历所有子目录 |

### 系统信息与转换

| 方法/属性    | 描述                 | 示例代码           | 说明                                      |
| :----------- | :------------------- | :----------------- | :---------------------------------------- |
| `resolve()`  | 获取绝对路径         | `p.resolve()`      | 解析符号链接，消除 ..                     |
| `absolute()` | 获取绝对路径         | `p.absolute()`     | 不解析符号链接，不消除 ..                 |
| `stat()`     | 获取文件状态信息     | `p.stat().st_size` | 返回 `os.stat_result` 对象 (大小, 时间等) |
| `cwd() `     | 获取当前工作目录     | `Path.cwd()`       | 类方法，等同于 `os.getcwd()`              |
| `home()`     | 获取用户主目录       | `Path.home()`      | 类方法，等同于 `~ `                       |
| `touch()`    | 创建空文件或更新时间 | `p.touch()`        | 类似 `Linux touch` 命令                   |
| `chmod()`    | 修改权限             | `p.chmod(0o755)`   | 类似 `Linux chmod` 命令                   |

### 实践

- `parents=True` 是神器：在调用 `mkdir()` 时，几乎总是应该加上 `parents=True, exist_ok=True`，这样可以避免因目录已存在或父目录缺失而导致的报错。
- `/` 运算符：这是 pathlib 的灵魂。请习惯使用 `Path('dir') / 'file.txt'` 而不是 `os.path.join`。
- `resolve()` vs `absolute()`：如果你需要获取文件的真实物理路径（例如为了防重复或安全校验），请务必使用 `resolve()`，因为它会处理软链接和相对路径符号。

这份表格涵盖了 pathlib` 95% 的常用功能。建议你在写代码时把它放在手边，遇到不确定的方法时快速查阅，很快就能形成肌肉记忆了！
