# 异常

异常处理是 Python 编程中至关重要的一环，它不仅能让程序在遇到错误时不至于直接崩溃，还能帮助我们优雅地处理各种意外情况，保证程序的健壮性。

## 产生异常

python 中使用 `raise` 语句来产生异常。

raise 的基本语法是 `raise [异常类型] [异常信息]`

### 主要抛出异常

当程序遇到不符合业务逻辑的情况时，可以使用 raise 关键字手动抛出异常。

```python
# 主动抛出 ValueError 异常
raise ValueError("除数不能为零")
```

### 重新抛出异常

在 except 代码块中，你可以使用不带任何参数的 raise 语句来重新抛出当前正在处理的异常。这在你想记录错误日志，但又不想完全处理该错误，而是希望上层调用者也能感知到时非常有用。

```python
def risky_operation():
    try:
        # 这里可能会出错
        result = 1 / 0
    except ZeroDivisionError:
        print("记录日志：发生了除零错误")
        raise  # 重新抛出当前的 ZeroDivisionError

try:
    risky_operation()
except ZeroDivisionError:
    print("上层捕获到了重新抛出的异常")

```

### 异常链

Python 3 引入了异常链的概念，允许你将一个新的异常与一个已存在的异常关联起来。这通常发生在处理一个异常时又引发了另一个异常。使用 `raise ... from ...` 语法可以保留原始异常的上下文信息，这对于调试非常有帮助。

```python
try:
    with open("nonexistent_file.txt") as f:
        f.read()
except FileNotFoundError as e:
    # 在处理 FileNotFoundError 时，抛出一个新的 RuntimeError
    # 并使用 'from e' 将两者关联起来
    raise RuntimeError("配置文件加载失败") from e
```

### 语言内置的异常类

Python 内置了大量的异常类，它们都是 Exception 的子类（或子类的子类），用于精确描述不同类型的错误。

Python 的异常层次结构设计得非常清晰：

- BaseException: 所有异常的“祖先”。
- Exception: BaseException 的一个直接子类，它是所有非系统退出类异常的基类。

这意味着，当你使用 `except Exception:` 时，你捕获的是几乎所有程序运行时可能遇到的错误，但会放过像 `KeyboardInterrupt`（用户按 Ctrl+C）或 `SystemExit`（程序请求退出）这类系统级异常，这是一个非常好的实践，可以避免程序无法正常退出。

```txt
BaseException
+-- SystemExit                      系统退出
+-- KeyboardInterrupt               键盘中断
+-- GeneratorExit                   生成器退出
+-- Exception                       常规错误的基类
    +-- StopIteration               当迭代器没有更多值时，由 next() 函数抛出，用于通知循环结束
    +-- ArithmeticError             所有数值计算错误的基类
    |   +-- ZeroDivisionError           当除法或取模运算的除数为零时抛出
    |   +-- OverflowError               当结果太大溢出时抛出
    +-- LookupError                 数据查询错误
    |   +-- IndexError                  当尝试访问序列（如列表、元组）中不存在的索引时抛出
    |   +-- KeyError                    当尝试访问字典中不存在的键时抛出
    |   +-- TypeError                   当尝试访问字典中不存在的键时抛出
    |   +-- KeyError                    当尝试访问字典中不存在的键时抛出
    |   +-- KeyError                    当尝试访问字典中不存在的键时抛出
    +-- AttributeError             当尝试访问或赋值一个对象不存在的属性时抛出
    +-- TypeError                  当操作或函数应用于不适当类型的对象时抛出
    +-- NameError                  当尝试访问一个未定义的变量名时抛出
    +-- ValueError                 当函数接收到一个类型正确但值不合适的参数时抛出 eg: int('a')
    +-- ImportError                当 import 语句无法找到要导入的模块时抛出
    |   +-- ModuleNotFoundError
    +-- OSError                    操作系统错误的基类
    |   +-- PermissionError           当操作因权限不足而失败时抛出
    |   +-- FileNotFoundError         尝试打开一个不存在的文件时抛出
    +-- SyntaxError                当代码存在语法错误时抛出，这是唯一一类在代码执行前就会被解释器捕获的错误
    +-- RuntimeError               当发生一个不属于任何其他类别的错误时抛出，通常表示一个通用的运行时错误
    ...等等
```

### 自定义异常类

Python 允许我们定义自己的异常类，以便更清晰地表达业务错误。通常继承自 Exception 类即可。

```python
class SensorError(Exception):
    """自定义传感器异常"""
    def __init__(self, sensor_id, message):
        self.sensor_id = sensor_id
        self.message = message
        super().__init__(f"[传感器 {sensor_id}] 发生错误: {message}")

# 使用
try:
    raise SensorError("S01", "温度读取超时")
except SensorError as e:
    print(e)
```

## 捕获异常

Python 的异常处理主要依赖这四个关键字的组合。

- try: 放置可能会抛出异常的代码。
- except: 捕获并处理 try 块中发生的特定异常。
- else: 当 try 块没有抛出任何异常时执行的代码。
- finally: 无论是否发生异常，都一定会执行的代码，通常用于资源清理（如关闭文件、断开连接）

理解它们的执行顺序是掌握异常处理的关键。

| 步骤 | 描述                                               |
| :--- | :------------------------------------------------- |
| 1    | 执行 `try` 块中的代码。                            |
| 2a   | 如果发生异常：跳转到匹配的 `except` 块处理。       |
| 2b   | 如果未发生异常：跳过 `except` 块，执行 `else` 块。 |
| 3    | 无论上述哪种情况，最后都会执行 `finally` 块。      |

```python
def divide_numbers(a, b):
    try:
        print(f"正在计算 {a} / {b}...")
        result = a / b  # 可能抛出 ZeroDivisionError
    except ZeroDivisionError:
        print("错误：除数不能为零！")
        return None
    except TypeError as e:
        print(f"类型错误: {e}")
        return None
    else:
        print("计算成功！")
        return result
    finally:
        print("清理工作：无论成功失败，这里都会执行。")

# 调用示例
divide_numbers(10, 2)  # 正常路径
divide_numbers(10, 0)  # 异常路径
```

### except 捕获异常的多种方式

在实际开发中，我们需要灵活地捕获不同类型的错误。

- 捕获特定异常：这是推荐的做法，例如 `except ValueError:` 或 `except FileNotFoundError:`。
- 捕获多种异常：可以使用元组来一次性捕获多种异常，例如 `except (ValueError, FileNotFoundError) as e:`，或者 `except ValueError, FileNotFoundError:`。
- 捕获所有异常（慎用）：使用 `except Exception as e`: 可以捕获大部分非系统退出的异常。尽量避免使用裸的 except:，因为它会捕获包括 KeyboardInterrupt（Ctrl+C）在内的所有异常，导致程序难以终止。

## 排查异常

python 异常的调试方式有：

- 使用 print 语句来打印异常信息。
- 使用 logging 模块记录异常信息。
- 使用 pdb 模块进行调试。
- 增强版神器：PySnooper
- IDE 图形化调试 (PyCharm / VS Code)

```python
import logging

logging.basicConfig(level=logging.INFO, filename='app.log')

try:
    result = 10 / 0
    # 简单的问题调试
    print(result)
except Exception as e:
    # exc_info=True 是关键，它会记录完整的错误堆栈信息
    logging.error("发生异常", exc_info=True)
```

pdb (Python Debugger) 是标准库中的内置的调试工具。它允许程序在运行中“暂停”，进入交互模式，然后输入命令，观察程序输出。

```python


def divide(a, b):
    import pdb; pdb.set_trace()  # 程序运行到这里会暂停
    return a / b

divide(10, 2)
```

`pdb.set_trace()` 进入交互的调试模式后，可以使用以下命令：

| 命令 | 全称     | 作用                             |
| :--- | :------- | :------------------------------- |
| `n`  | next     | 执行下一行代码（不进入函数内部） |
| `s`  | step     | 执行下一行代码（会进入函数内部） |
| `c`  | continue | 继续执行，直到遇到下一个断点     |
| `p`  | print    | 打印变量值，如 `p my_variable`   |
| `l`  | list     | 查看当前代码上下文               |
| `q`  | quit     | 退出调试器（终止程序）           |

另外，pdb 模块还提供了 `post-mortem` 模式，当程序抛出异常并崩溃时，你可以让 Python 自动进入调试模式，直接定位到报错的那一行。

两种使用方式

- 命令行方式：使用 `python -m pdb your_script.py` 运行脚本。当脚本出错时，它不会直接退出，而是进入 (Pdb) 模式，你可以查看当时的变量状态。
- 代码方式：在 except 块中直接启动调试器。

```sh
try:
    risky_code()
except Exception:
    import pdb; pdb.post_mortem() # 异常发生后立即进入调试
```

如果你觉得 pdb 需要一步步单步执行太麻烦，想要一次性看到整个函数的执行流程和变量变化，PySnooper 是目前的“版本之子”。它会自动记录函数执行过程中的每一行代码和所有变量的变化，并打印出来。

用法：只需加一个装饰器 @pysnooper.snoop()。

```python
import pysnooper

@pysnooper.snoop()  # 加上这个装饰器
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

number_to_bits(6)
# 控制台会自动输出：每一行代码的执行顺序、变量的变化过程
```

如果你使用现代 IDE，这是最高效的方式，完全可视化。

- 断点 (Breakpoints)：点击行号旁边的红点。
- 单步执行：点击“小虫子”图标启动调试，使用工具栏上的“Step Over” (跨过) 或 “Step Into” (进入) 按钮。
- 变量视图：IDE 会在侧边栏自动显示当前作用域内所有变量的值，无需手动输入命令。

## 预防异常

要想预防或减少异常的发生，可以在程序开发中进行单元测试。在 python 中，单元测试可以通过以下几种方式实现：

1. 使用 unittest 模块：unittest 是 Python 标准库自带的测试框架，它借鉴了 Java 的 JUnit，采用基于类的面向对象风格。它是构建结构化测试套件的基础。
2. 使用 pytest 模块：pytest 是一个功能强大的第三方测试框架，以其简洁的语法、自动发现测试和强大的插件生态而闻名，是目前 Python 社区最流行的选择。
3. 使用 doctest 模块：doctest 模块允许你在文档字符串中编写测试用例。它将函数文档字符串（docstring）中的交互式示例直接作为测试用例来执行。这确保了你的代码示例和文档永远是同步的，避免了“文档过时”的尴尬。

示例：

### unittest

核心特点：

- 开箱即用：作为标准库的一部分，无需额外安装。
- 结构清晰：通过继承 unittest.TestCase 类来组织测试用例。
- 功能丰富：提供了丰富的断言方法（如 assertEqual, assertTrue）和测试固件（setUp, tearDown）。

```python
import unittest

def add(a, b):
    return a + b

# 1. 创建一个继承自 unittest.TestCase 的测试类
class TestMathOperations(unittest.TestCase):
    # 2. 定义以 test_ 开头的测试方法
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5) # 使用断言方法验证结果

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

# 3. 运行测试
if __name__ == '__main__':
    unittest.main()
```

### pytest

核心特点：

- 语法简洁：直接使用 assert 语句进行断言，无需记忆各种 self.assert\* 方法。
- 自动发现：能自动识别并运行以 test\_ 开头的文件和函数。
- 生态强大：支持参数化测试、丰富的插件（如并行测试、覆盖率报告）和友好的错误信息。

```python
# 1. 安装: uv add pytest

# 2. 编写测试，可以直接用函数写测试用例，也可以用测试类组织测试用例
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5  # 使用原生 assert
    assert add(-1, 1) == 0

# 3. 运行测试：在命令行直接输入 pytest
# pytest 会自动发现 test_ 开头的函数并执行
```

### doctest

核心特点：

- 一举两得：既是使用示例，也是自动化测试。
- 简单直观：测试用例就是 Python 交互式会话的格式，以 >>> 开头。
- 适用于：验证简单的函数逻辑、编写教学文档或教程。

```python
# 运行这个脚本时，doctest 会自动查找并执行 docstring 中的示例，验证实际输出是否与预期输出（5 和 0）一致。如果一切正常，则没有任何输出；如果有失败，则会打印出详细的错误信息。
def add(a, b):
    """
    计算两个数的和。

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b

# 在模块末尾添加这两行代码来运行测试
if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

如何选择？

1. 小型项目或编写教程：优先考虑 doctest，让文档和代码示例永远保持最新。
1. 标准库或简单需求：如果不想引入第三方依赖，unittest 是一个可靠的选择。
1. 中大型项目或团队协作：强烈推荐 pytest。它的简洁语法能显著提升开发效率，强大的插件生态（如 pytest-cov 测覆盖率，pytest-xdist 并行测试）能应对各种复杂的测试需求。

在现代 Python 开发中，pytest 因其卓越的开发体验而成为事实上的标准。
