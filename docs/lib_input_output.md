# input 输入和 output 输出

## input 输入

Python 主要通过内置函数 `input()` 函数来获取用户的键盘输入。

`input()` 函数会暂停程序运行，等待用户输入内容并按下回车。它会接收一个可选的字符串参数作为提示信息。

```python
name = input("请输入您的姓名: ")
print(f"你好, {name}!")
```

所有通过 `input()` 获取的内容，默认都是字符串（str）类型。即使用户输入的是数字，也需要进行类型转换才能进行数学运算。

```python
# 获取整数
age = int(input("请输入您的年龄: "))
# 获取浮点数
height = float(input("请输入您的身高(米): "))
```

在实际开发中，直接转换类型可能会因为用户输入了非数字内容而导致程序崩溃（ValueError）。更健壮的做法是使用 `try...except` 语句来捕获并处理异常。

```python
try:
    num = int(input("请输入一个数字: "))
    print(f"您输入的数字是: {num}")
except ValueError:
    print("输入无效，请输入一个有效的数字！")
```

## output 输出

Python 主要使用 print() 函数将信息输出到控制台，或者指定的文件中。

基本用法

```python
# 直接输出字符串、数字、变量或表达式的结果
print("Hello, World!")
print(100 + 200)
```

`print()` 函数的签名：

```python
def print(
    *values: object,
    sep: str | None = " ", # 定义多个对象之间的分隔符，默认为空格。
    end: str | None = "\n", # 定义输出结束时的字符，默认为换行符 `\n`
    file: SupportsWrite[str] | None = None, # 定义输出的流，默认为标准输出(sys.stdout)，即终端直接输出，也可以指定文件流，输出到指定文件中。
    flush: Literal[False] = False, # 定义是否刷新缓冲区，默认为不刷新
) -> None:
```

示例

```python
# 自定义分隔符
print("2024", "04", "19", sep="-") # 输出: 2024-04-19

# 取消自动换行
for i in range(5):
    print(i, end=" ") # 输出: 0 1 2 3 4

# 输出到文件流
with open("output.txt", "w") as f:
    print("Hello, World!", file=f)
```

## 格式化输出

Python 的字符串格式化经历了从简单到强大、从晦涩到直观的演进过程，主要可以分为三个阶段。

- `%` 语法
- `str.format()` 方法
- `f-string`

### % 格式化 (Python 早期)

这是 Python 最早的格式化方式，直接借鉴了 C 语言的 printf 风格。

虽然在现代 Python 中仍然被支持，但已不推荐在新代码中使用，主要见于一些旧项目的维护。

`%` 语法

语法为 `%[宽度][.精度][类型] % 变量`

- 宽度：指定输出字符串的最小长度，不足时用空格填充（默认右对齐）；
- 精度：对浮点数表示小数位数，对字符串表示最大长度；
- 左对齐：在宽度前加 - 实现左对齐。
- 类型：指定输出字符串的类型。

- `%s`：字符串格式化，将变量的值转换为字符串。
- `%d`：整数格式化，将变量的值转换为整数。
- `%f`：浮点数格式化，将变量的值转换为浮点数。
- `%c`：字符格式化，将变量的值转换为字符。
- `%x`：十六进制数格式化，将变量的值转换为十六进制数。
- `%o`：八进制数格式化，将变量的值转换为八进制数。
- `%b`：二进制数格式化，将变量的值转换为二进制数。
- `%r`：原始字符串格式化，将变量的值转换为原始字符串。
- `%e`：科学计数法格式化，将变量的值转换为科学计数法。

```python
# 控制浮点数精度
pi = 3.1415926535
print("PI: %.2f" % pi)  # 输出：PI: 3.14（保留2位小数）

# 控制宽度与对齐
num = 42
print("Number: %5d" % num)   # 输出：Number:    42（宽度5，右对齐）
print("Number: %-5d" % num)  # 输出：Number: 42   （宽度5，左对齐）

# 字符串截断
text = "Hello, World!"
print("Text: %.5s" % text)  # 输出：Text: Hello（最多5个字符）
```

尽管 % 格式化历史悠久，但它存在诸多设计缺陷，导致在现代 Python 开发中逐渐被替代：

- 类型严格匹配：若占位符类型与值不匹配（如用 %d 接收字符串），会直接抛出 TypeError，灵活性差；
- 元组传递限制：当需要格式化的变量较多时，必须用元组包裹，且顺序不能错，可读性低；
- 嵌套与复杂逻辑支持弱：无法直接嵌套表达式或调用函数，需先将结果存入变量；
- 扩展性不足：不支持自定义格式化逻辑，对复杂对象（如日期、枚举）的格式化需手动转换。

```python
# 类型不匹配报错
print("Age: %d" % "30")  # 抛出 TypeError: %d format: a real number is required, not str

# 多变量顺序易错
print("%s is %d years old, score: %.1f" % (age, name, score))  # 顺序错误导致结果混乱

```

### `str.format()` 方法 (Python 2.6 / 3.0)

为了解决 % 格式化的局限性而引入，提供了更强大和灵活的格式化功能。`str.format()` 是 Python 2.6 引入的格式化方法，使用 `{}` 来指定参数的位置，并使用 `:` 来指定格式控制。

- 特点：支持位置参数、命名参数，以及更复杂的格式控制（如对齐、填充、精度等）。
- 现状：功能依然强大，但在 f-string 出现后，因其语法相对冗长，不再是首选。

```python
# 基本用法
print("姓名: {}, 年龄: {}".format("Bob", 30)) # 输出: 姓名: Bob, 年龄: 30
# 命名参数
print("姓名: {name}, 年龄: {age}".format(name="Charlie", age=28)) # 输出: 姓名: Charlie, 年龄: 28
# 位置参数
print("{1} 比 {0} 大".format(10, 20)) # 输出: 20 比 10 大

# 对齐与宽度（<左对齐，>右对齐，^居中）
print("|{:<10}|{:^10}|{:>10}|".format("Left", "Center", "Right"))
# 输出：|Left      |  Center  |     Right|

# 浮点数精度
pi = 3.1415926535
print("PI: {:.3f}".format(pi))  # 输出：PI: 3.142（保留3位小数）

# 千位分隔符（适用于数字）
num = 1234567
print("Large number: {:,}".format(num))  # 输出：Large number: 1,234,567

# 通过 ! 指定类型转换（类似 %s 与 %r）：
text = "Hello"
print("str: {!s}, repr: {!r}".format(text, text))
# 输出：str: Hello, repr: 'Hello'

# 可通过 . 访问字典键，通过 [] 访问列表索引：
person = {"name": "Eve", "age": 32}
hobbies = ["reading", "hiking"]

print("Name: {p[name]}, Hobby: {h[0]}".format(p=person, h=hobbies))
# 输出：Name: Eve, Hobby: reading


# 可在占位符中直接调用对象的方法（无参数）
text = "hello world"
print("Uppercase: {.upper()}".format(text))  # 输出：Uppercase: HELLO WORLD

# 通过在类中实现 __format__ 方法，可自定义对象的格式化行为：
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    # 自定义格式化：支持 'c'（摄氏度）和 'f'（华氏度）
    def __format__(self, format_spec):
        if format_spec == 'f':
            fahrenheit = self.celsius * 9/5 + 32
            return f"{fahrenheit:.1f}°F"
        else:  # 默认摄氏度
            return f"{self.celsius:.1f}°C"

temp = Temperature(25)
print("Temp: {t:c}".format(t=temp))  # 输出：Temp: 25.0°C
print("Temp: {t:f}".format(t=temp))  # 输出：Temp: 77.0°F

# 特定类型格式化，为常见类型（如日期、百分比）提供了专用格式符：
from datetime import datetime
now = datetime(2025, 11, 12, 15, 30)

# 日期格式化
print("Date: {:%Y-%m-%d %H:%M}".format(now))  # 输出：Date: 2025-11-12 15:30

# 百分比格式化
ratio = 0.753
print("Ratio: {:.1%}".format(ratio))  # 输出：Ratio: 75.3%（自动乘以100并加%）

```

### f-string (Python 3.6+)

通过 PEP 498 引入，全称为“格式化字符串字面量”（Formatted String Literals）。`f-string` 是在字符串前加上 f 或 F，并在花括号 `{}` 内直接写入变量或表达式。

- 特点：这是当前官方推荐的首选方式。它语法最简洁，可读性最强，并且性能最优（在编译时进行优化）。
- 现状：现代 Python 开发中的标准做法

```python
name = "Alice"
age = 25
print(f"姓名: {name}, 年龄: {age}")
# 输出: 姓名: Alice, 年龄: 25

# 支持表达式，三目运算、函数调用等
price = 99.9
print(f"明年价格: {price * 1.1:.2f} 元") # 输出: 明年价格: 109.89 元
print(f"Result: {'Pass' if price >= 60 else 'Fail'}")  # 输出：Result: Pass

# 日期格式化
from datetime import datetime
now = datetime.now()
print(f"Today: {now:%Y年%m月%d日}")  # 输出：Today: 2025年11月12日

# 在 Python 3.8 及更高版本中，可以在花括号内变量后加上 =，快速输出变量名和其值，非常便于调试。
print(f"{name = }, {age = }") # 输出: name = 'Alice', age = 25

# 多行模板，使用三引号
name = "Jack"
age = 33
bio = f"""
User Profile:
- Name: {name}
- Age: {age}
- Status: {'Active' if age < 40 else 'Inactive'}
"""
print(bio.strip())  # 输出：
# User Profile:
# - Name: Jack
# - Age: 33
# - Status: Active

```

### 微语法规则

`str.format()` 和 `f-string` 共享一套强大的格式控制语法，在 `{表达式:格式规范}` 中添加格式控制。

| 语法    | 含义                  | 示例 (以 f-string 为例) | 输出结果      |
| :------ | :-------------------- | :---------------------- | :------------ |
| `:<10`  | 左对齐，总宽度10      | `f"{'hi':<10}"`         | `'hi '`       |
| `:>10`  | 右对齐，总宽度10      | `f"{'hi':>10}"`         | `' hi'`       |
| `:^10`  | 居中对齐，总宽度10    | `f"{'hi':^10}"`         | `' hi '`      |
| `:*^10` | 居中对齐，用 `*` 填充 | `f"{'hi':*^10}"`        | `'hi'`        |
| `:.2f`  | 保留两位小数          | `f"{3.14159:.2f}"`      | `'3.14'`      |
| `:,`    | 添加千位分隔符        | `f"{1234567:,}"`        | `'1,234,567'` |

## 性能与安全性

- 性能优势：`f-string` 在编译时解析，比 % 和 `format()` 更快，尤其在循环中差距明显；
- 安全性：`f-string` 中的表达式在当前作用域执行，避免了 `format()` 可能的变量注入风险（但仍需注意动态生成模板的安全问题）。

```python
import timeit

# 测试三种方式的性能
def test_percent():
    name = "test"
    return "%s" % name

def test_format():
    name = "test"
    return "{}".format(name)

def test_fstring():
    name = "test"
    return f"{name}"

print("Percent:", timeit.timeit(test_percent, number=10_000_000))  # 约1.2秒
print("Format:", timeit.timeit(test_format, number=10_000_000))    # 约1.5秒
print("F-string:", timeit.timeit(test_fstring, number=10_000_000))# 约0.8秒（最快）

```
