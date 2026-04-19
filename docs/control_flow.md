# 流程控制语句

## 条件语句 if elif else

```python
if condition1:
    # 执行代码块1
elif condition2:
    # 执行代码块2
else:
    # 执行代码块3
```

简单的条件语句，可以使用三元运算符(一行)

```python
# 如果 condition 为真，返回 true_value，否则返回 false_value
value = true_value if condition else false_value

```

## 循环语句 while for

```python
while condition:
    # 执行代码块


for item in iterable:
    # 执行代码块
```

## 中断语句 break continue

- `break`：立即退出当前循环。
- `continue`：跳过本次循环剩余部分，进入下一次循环。

```python
for i in range(10):
    if i == 5:
        break
    print(i)
else:
    print("循环正常结束")

# 最后输出 0 1 2 3 4
```

## pass 语句

占位符，不执行任何操作，用于语法需要但逻辑暂空的情况。

```python
if condition:
  pass # 日后实现

# 或者函数定义占位符
def fn():
  pass
```

## 结构模式匹配 match

类似其它语言的 `switch`，但它应用范围更广。

基本语法

```python
match value:
    case pattern1:
        # 执行代码块1
    case pattern2:
        # 执行代码块2
    case _:  # 通配符，相当于 else
        # 默认情况
```

示例：简单值匹配，同 switch

```python
status = 404

match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case _: # _ 是通配符，必须放在最后（否则会屏蔽后续分支）。
        print("Unknown status")
```

示例：使用条件模式

```python
match status:
    case 200 | 201 | 202:
        print("Success")
    case 400 | 401 | 403 | 404:
        print("Client error")
```

数据结构匹配

```python
#  元组，列表类似
point = (1, 2)

match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"Point at ({x}, {y})")

# 对象结构匹配
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)

match p:
    case Point(x=0, y=0):
        print("Origin")
    case Point(x=0, y=y):
        print(f"On Y axis at {y}")
    case Point(x=x, y=y):
        print(f"Point at ({x}, {y})")

# case 后加 if 条件语句
point = (3, 5)

match point:
    case (x, y) if x == y:
        print("On diagonal")
    case (x, y):
        print(f"Off diagonal: ({x}, {y})")
```
