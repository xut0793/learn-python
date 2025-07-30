# 数据转换

数据类型的操作通过内置函数实现：`type()`、`isinstance()`、`bool()`、`int()`、`float()`、`str()`。

## 查看数据类型

使用 `type()` 函数可以查看一个变量的数据类型。

```python
print(type(10))  # <class 'int'>
print(type(10.0))  # <class 'float'>
print(type('abc'))  # <class 'str'>
print(type(True))  # <class 'bool'>
```

## 检测类型

使用 `isinstance()` 函数可以检测一个变量是否是某个类型。

```python
print(isinstance(10, int))  # True
print(isinstance(10.0, float))  # True
print(isinstance('abc', str))  # True
print(isinstance(True, bool))  # True
```

## 转换为布尔值

使用 `bool()` 函数可以将一个值转换为布尔值。

```python
print(bool(10))  # True
print(bool(0))  # False
print(bool(10.123))  # True
print(bool('0.0'))  # False
print(bool(''))  # False
print(bool('abc'))  # True
```

- 假值 Falsy: `0, 0.0, '', (), [], {}, None, False`
- 真值 Truthy: 非假值，即为真

## 转换为整数

使用 `int()` 函数可以将一个值转换为整数。

```python
print(int(10.123))  # 10
print(int('10'))  # 10
print(int('10.123'))  # 10
print(int(True))  # 1
print(int(False))  # 0
print(int('123'))  # 123
```

- 浮点数转为整数时，会去掉小数部分，直接取整数部分。
- 字符串转为整数时，字符串必须是数字格式，否则会报错。
- 布尔值转为整数时，`True` 转为 `1`，`False` 转为 `0`。

## 转换为浮点数

使用 `float()` 函数可以将一个值转换为浮点数。

```python
print(float(10))  # 10.0
print(float('10'))  # 10.0
print(float('10.123'))  # 10.123
print(float(True))  # 1.0
print(float(False))  # 0.0
```

- 整数转为浮点数时，会在整数后面添加 `.0`。
- 字符串转为浮点数时，字符串必须是数字格式，否则会报错。
- 布尔值转为浮点数时，`True` 转为 `1.0`，`False` 转为 `0.0`。

## 转换为字符串

使用 `str()` 函数可以将一个值转换为字符串。

```python
print(str(10))  # '10'
print(str(10.123))  # '10.123'
print(str(True))  # 'True'
print(str(False))  # 'False'
print(str('123'))  # '123'
```
