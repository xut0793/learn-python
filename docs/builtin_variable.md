# 全局变量

Python 中没有像 PI 或 VERSION 这样预定义的“内置全局常量”。通常所说的“全局变量”是指在整个模块或程序级别定义的变量。Python 提供了一些内置函数来访问和操作这些变量所在的作用域。

1. `globals()`: 返回一个字典，表示当前的全局符号表。这个字典包含了当前模块中定义的所有全局变量、函数和类。你可以通过这个字典来访问甚至修改全局变量。
2. `locals()`: 返回一个字典，表示当前的局部符号表。在函数内部调用时，它会返回该函数内的局部变量。
3. `vars()`: 如果没有参数，那它与 `locals()` 相同。如果传入一个对象（如模块、类或实例），它会返回该对象的 `__dict__` 属性，即包含其所有属性和值的字典。

```python
x = 10
def my_func():
    y = 20
    print(locals()) # 输出: {'y': 20}

global_vars = globals()
print(global_vars['x'])  # 输出: 10
print(global_vars['my_func']) # 输出: <function my_func at ...>

```

### `vars()` 函数

`vars()` 只能用于有 `__dict__` 属性的对象。模块、类、实例都有，但内置类型（如 int, list, str）通常没有 `__dict__`，使用时会报 `TypeError` 错误。

```python
def test_function():
    a = 10
    b = "hello"
    # 无参数时，返回当前函数内的局部变量字典
    print(vars())

test_function()
# 输出示例: {'a': 10, 'b': 'hello'}
```

查看模块的全局变量

```python
import math

# 查看 math 模块的所有属性和值
# 输出会很长，包含 sin, cos, pi 等
print(vars(math))

# 也可以查看当前脚本的全局变量
print(vars())
```

查看类或实例的属性，这是 `vars()` 最常见的用法之一，用于检查对象的属性。

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.city = "Beijing"

    def say_hello(self):
        pass

# 1. 查看实例的属性
p = Person("Alice", 25)
print(vars(p))
# 输出: {'name': 'Alice', 'age': 25, 'city': 'Beijing'}

# 2. 查看类的属性 (包含方法)
print(vars(Person))
# 输出包含: {'__module__': '__main__', '__init__': <function...>, 'say_hello': <function...>, ...}
```

实用技巧：动态属性访问，`vars()` 返回的是字典，因此可以结合字典操作来动态获取或修改属性，比 `getattr` 和 `setattr` 更直观。

```python
class Config:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080

config = Config()

# 获取属性名列表
attr_names = vars(config).keys()
print(f"属性列表: {list(attr_names)}")
# 输出: 属性列表: ['host', 'port']

# 动态修改属性
vars(config)['port'] = 9090
print(config.port)
# 输出: 9090
```
