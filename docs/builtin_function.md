# 内置函数

在 Python 中，内置函数是随时可用的核心工具，无需导入任何模块即可直接使用。

Python 3.11 版本中包含了 69 个内置函数。它们功能广泛，涵盖了从数据类型转换、数学运算到对象操作等各个方面。

以下是一些最常用和最重要的内置函数分类总结：

## 数据类型转换

| 函数名            | 描述                       | 示例                               |
| :---------------- | :------------------------- | :--------------------------------- |
| `int(x, base)`    | 将字符串或数字转换为整数   | `int("10")` → `10`                 |
| `float(x)`        | 将字符串或数字转换为浮点数 | `float("3.14")` → `3.14`           |
| `str(x)`          | 将对象转换为字符串         | `str(100)` → `"100"`               |
| `bool(x)`         | 将值转换为布尔值           | `bool(0)` → `False`                |
| `list(iterable)`  | 将可迭代对象转换为列表     | `list((1, 2))` → `[1, 2]`          |
| `tuple(iterable)` | 将可迭代对象转换为元组     | `tuple([1, 2])` → `(1, 2)`         |
| `dict(kw)`        | 创建字典                   | `dict(a=1, b=2)`                   |
| `set(iterable)`   | 创建集合                   | `set([1, 1, 2])` → `{1, 2}`        |
| `chr(i)`          | 将整数（ASCII）转换为字符  | `chr(97)` → `'a'`                  |
| `ord(c)`          | 将字符转换为整数（ASCII）  | `ord('a')` → `97`                  |
| `hex(x)`          | 将整数转换为十六进制字符串 | `hex(255)` → `'0xff'`              |
| `bin(x)`          | 将整数转换为二进制字符串   | `bin(10)` → `'0b1010'`             |
| `oct(x)`          | 将整数转换为八进制字符串   | `oct(8)` → `'0o10'`                |
| `complex(r, i)`   | 创建复数                   | `complex(1, 2)` → `(1+2j)`         |
| `bytes(x)`        | 创建字节对象               | `bytes("abc", "utf-8")`            |
| `bytearray(x)`    | 创建可变字节数组           | `bytearray(5)`                     |
| `memoryview(x)`   | 返回内存视图对象           | `memoryview(b"abc")`               |
| `format(v, fmt)`  | 格式化数值或对象           | `format(3.1415, ".2f")` → `'3.14'` |

## 数学运算

| 函数名          | 描述                    | 示例                          |
| :-------------- | :---------------------- | :---------------------------- |
| `abs(x)`        | 返回绝对值              | `abs(-5)` → `5`               |
| `sum(iterable)` | 对序列求和              | `sum([1, 2, 3])` → `6`        |
| `max(iterable)` | 返回最大值              | `max([1, 5, 3])` → `5`        |
| `min(iterable)` | 返回最小值              | `min([1, 5, 3])` → `1`        |
| `pow(x, y)`     | 返回 x 的 y 次幂        | `pow(2, 3)` → `8`             |
| `divmod(a, b)`  | 返回商和余数的元组      | `divmod(10, 3)` → `(3, 1)`    |
| `round(x, n)`   | 对浮点数四舍五入        | `round(3.1415, 2)` → `3.14`   |
| `all(iterable)` | 所有元素为真则返回 True | `all([True, 1])` → `True`     |
| `any(iterable)` | 任一元素为真则返回 True | `any([0, False, 1])` → `True` |
| `hash(x)`       | 返回对象的哈希值        | `hash("hello")`               |

## 迭代器与序列操作

| 函数名               | 描述                     | 示例                                |
| :------------------- | :----------------------- | :---------------------------------- |
| `len(s)`             | 返回对象长度             | `len("abc")` → `3`                  |
| `range(stop)`        | 生成数字序列             | `range(3)` → `0, 1, 2`              |
| `enumerate(iter)`    | 将可迭代对象转为索引序列 | `list(enumerate(['a','b']))`        |
| `zip(*iters)`        | 打包多个可迭代对象       | `list(zip([1,2], ['a','b']))`       |
| `map(func, iter)`    | 对每个元素应用函数       | `map(str, [1, 2])`                  |
| `filter(func, iter)` | 过滤元素                 | `filter(lambda x: x>0, [-1, 1])`    |
| `sorted(iter)`       | 返回排序后的新列表       | `sorted([3, 1, 2])` → `[1, 2, 3]`   |
| `reversed(seq)`      | 返回反向迭代器           | `list(reversed([1, 2]))` → `[2, 1]` |
| `slice(stop)`        | 创建切片对象             | `slice(2)`                          |
| `next(iter)`         | 获取迭代器的下一个元素   | `next(iter([1,2]))` → `1`           |
| `iter(obj)`          | 创建迭代器               | `iter([1, 2, 3])`                   |

## 对象内省与属性操作

| 函数名                    | 描述                       | 示例                             |
| :------------------------ | :------------------------- | :------------------------------- |
| `type(obj)`               | 返回对象类型               | `type(10)` → `<class 'int'>`     |
| `id(obj)`                 | 返回对象内存地址           | `id(x)`                          |
| `isinstance(obj, cls)`    | 判断是否为类的实例         | `isinstance(10, int)` → `True`   |
| `issubclass(cls, base)`   | 判断是否为子类             | `issubclass(bool, int)` → `True` |
| `dir(obj)`                | 返回对象的属性和方法列表   | `dir(x)`                         |
| `hasattr(obj, name)`      | 检查是否有某属性           | `hasattr(x, "name")`             |
| `getattr(obj, name)`      | 获取属性值                 | `getattr(x, "name")`             |
| `setattr(obj, name, val)` | 设置属性值                 | `setattr(x, "age", 18)`          |
| `delattr(obj, name)`      | 删除属性                   | `delattr(x, "age")`              |
| `callable(obj)`           | 检查对象是否可调用         | `callable(print)` → `True`       |
| `vars(obj)`               | 返回对象的 `__dict__` 属性 | `vars(obj)`                      |

## 输入输出与执行环境

| 函数名             | 描述                     | 示例                     |
| :----------------- | :----------------------- | :----------------------- |
| `print(*args)`     | 打印输出                 | `print("Hello")`         |
| `input(prompt)`    | 获取用户输入             | `name = input("Name: ")` |
| `open(file, mode)` | 打开文件                 | `open("data.txt", "r")`  |
| `eval(expr)`       | 执行字符串表达式并返回值 | `eval("1 + 1")` → `2`    |
| `exec(obj)`        | 执行 Python 代码         | `exec("x = 1")`          |
| `help(obj)`        | 查看帮助文档             | `help(print)`            |
| `globals()`        | 返回全局变量字典         | `globals()`              |
| `locals()`         | 返回局部变量字典         | `locals()`               |

## 面向对象编程

| 函数名                 | 描述                 | 示例                       |
| :--------------------- | :------------------- | :------------------------- |
| `classmethod(func)`    | 将方法转换为类方法   | `@classmethod`             |
| `staticmethod(func)`   | 将方法转换为静态方法 | `@staticmethod`            |
| `property(func)`       | 将方法转换为属性     | `@property`                |
| `super()`              | 调用父类方法         | `super().method()`         |
| `isinstance(obj, cls)` | 类型检查             | `isinstance(obj, MyClass)` |

## 调试与特殊用途

| 函数名                     | 描述                   | 示例                                 |
| :------------------------- | :--------------------- | :----------------------------------- |
| `breakpoint()`             | 调用内置调试器         | `breakpoint()`                       |
| `compile(src, file, mode)` | 将源代码编译为代码对象 | `compile("x=1", "<string>", "exec")` |
| `delattr(obj, name)`       | 删除属性               | `delattr(obj, 'x')`                  |
| `ascii(obj)`               | 返回对象的 ASCII 表示  | `ascii("中文")`                      |
| `repr(obj)`                | 返回对象的机器可读表示 | `repr(obj)`                          |
| `credits()`                | 显示致谢信息           | `credits()`                          |
| `license()`                | 显示许可证信息         | `license()`                          |
| `quit()`                   | 退出解释器             | `quit()`                             |
