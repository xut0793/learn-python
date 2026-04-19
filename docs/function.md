# 函数

函数是程序中实现语句复用的基本方式。

## 函数的定义

一个完整的函数定义 `Definition` 包括：

- `def`: 声明函数的关键字。
- 函数名: 遵循变量命名规则（通常是小写字母和下划线），用于调用函数。
- `()`: 圆括号内可以定义参数。
- `:` 函数定义行末尾的冒号。
- 函数体: 冒号后缩进的代码块，是函数实际执行的语句块。

```python
def greet(name):
  print(f"您好， {name}!")
```

## 函数的调用

函数调用方式是 `函数名称()`，将会触发函数内部代码块的执行。

```python
greet("tom")
```

## 函数的形参

形参 (Formal Parameter): 在函数定义时括号内的变量名，它是一个“占位符”，用来接收数据。例如，上面 greet(name) 中的 name 就是形参。

函数形参有多种形式：

- 无参函数
- 位置参数
- 关键字参数
- 参数默认值
- 仅位置参数
- 仅关键字参数
- 不定长的位置形参 `*args`
- 不定长的关键字形参 `**kwargs`

```python
# 1. 元参函数，没有入参的函数
def fn1():
  pass

# 2. 位置参数，最基础的参数形式，参数定义和调用时，按参数的先后顺序对应
def fn2(arg1, arg2, arg3):
  pass

# 调用
fn2(a1, a2, a3)

# 3. 关键字参数，区别在于函数调用时，明确当前参数的名称
fn2(args1=a1, arg2=a2, arg3 = a3)
fn2(arg3=a3, arg1=a1, arg2=a2) # 此时函数调用时，实参的传入顺序就无关紧要了，不需要像位置参数那样严格限定

# 4. 参数默认值，在形参定义时，就提供一个默认值，在调用时，如果没有传入对应的实参，就使用定义时的默认值
def fn3(arg1, arg2 = "a2")
  pass

# 调用
fn3(a1) # 此时 arg2就是a2
```

像上面位置参数和关键参数，仅在调用时有区别，但是在函数定义时没有区别，没办法在函数声明时，明确表示是位置参数还是关键字参数。

在 python3之后，引入了一种语法在函数声明时明确表示仅关键字参数，然后在 python3.8版本又引入仅位置参数。

- 仅位置参数：在函数定义中，通过在参数列表中插入一个斜杠（/），可以将其之前的所有参数标记为仅位置参数
- 仅关键字参数：在函数定义中，通过在参数列表中插入一个星号（\*），可以将其后的所有参数标记为仅限关键字参数

```
def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
      -----------    ----------     ----------
        |             |                  |
        |        Positional or keyword   |
        |                                - Keyword only
         -- Positional only
```

示例

```python
# 第一个函数定义 standard_arg 是最常见的形式，它对调用约定没有任何限制，参数可以通过位置或关键字传递
def standard_arg(arg):
    print(arg)

# 第二个函数 pos_only_arg 仅限于使用位置参数，因为函数定义中有一个 /
def pos_only_arg(arg, /):
    print(arg)

# 第三个函数 kwd_only_args 仅允许关键字参数，如函数定义中的 * 所示
def kwd_only_arg(*, arg):
    print(arg)

# 最后一个在同一个函数定义中使用了所有三种调用约定
def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)
```

还有一种场景，当声明时不确定参数数量时，可以使用不定长参数的形式声明，意思收集所有传入的参数。

- 不定长位置参数，使用单个星号（*）表示 `fn(*args)`
- 不定长关键参数，使用两个星号（\*）表示 `fn(**kwargs)`

示例

```python
def fn1(*args):
  print(args) # args 是一个元组 tuple 对象

def fn2(args1, arg2, *args):
  pass

def fn3(**kwargs):
  print(kwargs) # kwargs 是一个字典 dict 对象

# 多种参数形式混合时，顺序是严格要求的：必需的位置参数，可选的不定长位置参数，可选的不定长关键字参数
def fn4(arg1, *args, **kwargs)
  pass
```

## 函数的实参

实参 (Actual Parameter): 在函数调用时传递给函数的具体值。例如，greet("小明") 中的 "小明" 就是实参。

- 实参的引用：可变实参和不可变实参

函数调用时，传入的参数要区分是可变值还是不可变值。对于可变值入参，函数内部对它的改变，在函数外部也会跟着改变。

```python
# 定义一个可变值的列表
outside = ["one", "two"]

def push(arg):
  arg.append("three")
  print(f"inner: {arg}")

push(outside) # inner: ['one', 'two', 'three']

print(f"out: {outside}") # out: ['one', 'two', 'three']
```

在python的数据结构中：

- 不可变值：基础数据类型(bool, int, float, bytes, str)，tuple
- 可变值：list、set、dict

## 函数返回值 return

函数体内部可以使用 `return` 语句将一个结果返回给调用者。如果函数没有 `return` 语句，或者 `return` 后面没有值，它会默认返回 `None`。

函数可以返回任何类型的对象，甚至可以通过 `return a, b` 的形式返回多个值（实际上是返回一个元组）。

```python
def fn1():
  # 缺省时，返回 None

def fn2():
  # return 后面没有指定值时，也是返回 None
  return

def fn3():
  # return 可以返回支持的任务类型的值，bool int float complex str bytes function list tuple set dict
  return 1

def fn4():
  return 1, 2 # 实际以元组形式返回 (1,2)
```

## 文档字符串

函数体的第一行部分添加字符串来为函数定义附加上文档，这就是函数的文档字符串（docstring）​。

```python
def fn():
  "这里写一些函数的说明文字"
```

如果内容较多，或者格式较丰富，可以使用更宽容的可以换行的字符串 `""" """`。

文档字符串定义之后，如果想要查看，有以下两种方式：

- 使用 `help(fn)` 输出函数的完整说明，包括文档字符串、参数等。
- 使用 `fn.__doc__` 输出函数的文档字符串

## 嵌套函数

在函数块中声明的函数，然后函数可以在内部被调用，或者返回

```python
def outer():
  def inner():
    print("inner")
  # 内部可以调用或者返回 inner
  inner()
  print("outer")
  return inner
```

## 作用域

### LEGB 规则：变量查找顺序

当你在代码中使用一个变量名时，Python 解释器会按照 `L → E → G → B` 的顺序依次查找该变量。一旦在某个作用域中找到，查找就会停止。

- L - Local（局部作用域）
- E - Enclosing（嵌套作用域）
- G - Global（全局作用域）
- B - Built-in（内置作用域）

### 局部作用域 (Local Scope)

在函数内部定义的变量，其作用域仅限于该函数内部。当函数执行完毕后，这些变量就会被销毁。

- 特点：只能在定义它的函数内部访问。
- 生命周期：函数调用时创建，函数返回时销毁。

```python
def my_function():
    local_var = "我是局部变量"
    print(local_var)  #  可以访问

my_function()  # 输出: 我是局部变量

# print(local_var)  #  报错: NameError，在函数外部无法访问
```

python 变量不能在赋值之前被访问，报错`UnboundLocalError: cannot access local variable 'x' where it is not associated with a value`

```python
def fn():
  print(x)
  x = 20

fn()
# UnboundLocalError: cannot access local variable 'x' where it is not associated with a value
```

这点跟现代 JavaScript 中使用 `let / const` 声明变量的“暂时性死区”的原理一致。

### 嵌套作用域 (Enclosing Scope)

当一个函数（内部函数）定义在另一个函数（外部函数）内部时，就形成了嵌套。内部函数可以访问外部函数的局部变量，这个外部函数的作用域就是嵌套作用域。

- 特点：内部函数可以访问外部函数的变量。
- 生命周期：外部函数被调用时创建，外部函数返回后，只要内部函数（闭包）还存在，该作用域就不会被销毁。

```python
def outer():
    enclosing_var = "我是外部函数的变量"

    def inner():
        print(enclosing_var)  #  内部函数可以访问外部变量

    inner()

outer()  # 输出: 我是外部函数的变量
```

通常情况下，内部函数只能读取外部函数变量，如果需要修改外部函数内的变量，需要使用 `nonlocal` 关键字声明。

```python
def outer():
    count = 0

    def inner():
        nonlocal count  # 声明要修改嵌套作用域的变量
        count += 1
        print(count)

    return inner

my_closure = outer()
my_closure()  # 输出: 1
my_closure()  # 输出: 2
```

### 全局作用域 (Global Scope)

在函数外部、模块顶层定义的变量，属于全局变量。它们在整个程序（模块）的任何地方都可以被访问。

- 特点：在整个模块中可见。
- 生命周期：模块加载时创建，解释器退出时销毁。

```python
global_var = "我是全局变量"

def my_function():
    print(global_var)  #  可以访问全局变量

my_function()  # 输出: 我是全局变量
print(global_var)  # 输出: 我是全局变量
```

默认情况下，函数内部只能读取全局变量。如果需要修改全局变量的值，必须使用 `global` 关键字进行声明。

```python
count = 0

def increment():
    global count  # 声明要修改全局变量 count
    count += 1

increment()
print(count)  # 输出: 1
```

另外，要注意的特殊情况。

```python

x = 10
def func():
    print(x)  #  报错: UnboundLocalError
    x = 20    # 这行赋值让 Python 认为 x 是局部变量

func()
```

因为 `x = 20` 的存在，Python 将 `x` 视为 func 的局部变量。但在 `print(x)` 执行时，这个局部变量还未被赋值，因此报错，跟上述局部变量提前访问行为一致。

### 内置作用域 (Built-in Scope)

这是 Python 预定义的作用域，包含了所有内置的函数、异常和常量，如 `print()`, `len()`, `True`, `False`, `Exception` 等。它们在任何地方都可以直接使用。

```python
def my_function():
    print(len([1, 2, 3]))  #  直接使用内置的 len 函数

my_function()  # 输出: 3
```

但是这里要注意，避免使用内置函数作为变量名，这样会覆盖内置功能。

```python
len = 10  #  覆盖了内置的 len() 函数
# print(len([1, 2, 3]))  #  报错: TypeError: 'int' object is not callable
```

## 闭包

闭包可以认为是嵌套函数的一种特殊情形，像上面嵌套函数的简单场景中，当内层函数可以访问外层函数中声明的变量，但是当外部函数执行完毕，在函数里面声明的变量也会被销毁，没有途径可以访问。

但是一个闭包函数，它不仅包含它函数自身的代码（内层函数），还“封闭”了函数定义时所在作用域内的变量（外层函数声明的变量）。此时即时外层函数执行完毕，它内部声明的变量也不会被销毁，仍然可以被闭包函数（内层函数）访问到。

一个函数要称为闭包函数（Closure），必须满足以下三个条件：

- 存在嵌套函数：在一个函数（外部函数）内部定义另一个函数（内部函数）。
- 引用自由变量：内部函数引用了外部函数的局部变量（这个被引用的变量被称为“自由变量”）。
- 返回内部函数：外部函数将这个内部函数作为返回值返回（注意是返回函数对象本身，而不是调用它）。

```python
def outer_function(msg):  # 1. 外部函数
    # msg 是外部函数的局部变量

    def inner_function(): # 2. 内部函数
        print(msg)        # 3. 内部函数引用了外部变量 msg

    return inner_function # 4. 外部函数返回内部函数

# 创建一个闭包
my_closure = outer_function("你好，闭包！")

# 调用闭包
my_closure()  # 输出: 你好，闭包！
```

每个函数对象都有一个 `__closure__`属性。如果一个函数是闭包，这个属性会是一个包含 cell 对象的元组，每个 cell 对象都保存了一个被捕获的自由变量。此外，`__code__.co_freevars` 属性可以告诉你这个闭包捕获了哪些自由变量的名字。

```python
def outer(x):
    def inner():
        return x
    return inner

f = outer(42)
print(f.__closure__)          # 输出: (<cell at ...>,)，不为 None 说明是闭包
print(f.__closure__[0].cell_contents)  # 输出: 42，可以查看被捕获的变量值
print(f.__code__.co_freevars)  # 输出: ('x',)
```

## 递归

简单来说，递归就是函数内部调用自身。但是递归执行需要有一个中断条件，不然会造成“死循环”。

一个正确的递归函数必须包含两个不可或缺的部分：

- 基线条件 (Base Case)：也称为终止条件或递归出口。这是递归的终点，定义了一个可以直接求解的最简单情况。当满足此条件时，函数不再调用自身，直接返回结果，防止无限递归。
- 递归步骤 (Recursive Step)：也称为递推关系。在这一步，函数会调用自身来解决一个规模更小的子问题。关键在于，每次调用都必须让问题的规模向基线条件靠近。

```python
def factorial(n):
    # 1. 基线条件
    if n == 1:
        return 1
    # 2. 递归步骤
    else:
        return n * factorial(n - 1)

print(factorial(3)) # 输出: 6
```

## 函数内部属性

在 Python 中，函数不仅是可调用的代码块，更是**一等对象（First-class objects）**。

这意味着函数本身也拥有自己的属性，这些属性存储了函数的元数据、代码结构、运行环境等信息。通过内省（Introspection）这些属性，我们可以深入了解函数的内部机制，这在调试、框架开发（如 Django、FastAPI）和编写装饰器时非常有用。

> 在 python 语言中，以双下划线（\_\_）起止的名称是保留给Python内部使用的，不要将它们与你自己的变量一起使用。

| 属性名                    | 类型          | 描述                                                                                                                     |
| :------------------------ | :------------ | :----------------------------------------------------------------------------------------------------------------------- |
| 基础身份属性              |               |                                                                                                                          |
| `__name__`                | `str`         | 函数名称                                                                                                                 |
| `__qualname__`            | `str`         | 函数的限定名称。对于嵌套在类或函数中的函数，它包含完整的路径（例如 `MyClass.my_method`），而 `__name__` 只是 `my_method` |
| `__doc__`                 | `str`         | 文档字符串                                                                                                               |
| `__module__`              | `str`         | 函数定义所在的模块名称                                                                                                   |
| 参数与默认值属性          |               |                                                                                                                          |
| `__defaults__`            | `tuple`       | 一个元组，存储位置参数的默认值。                                                                                         |
| `__kwdefaults__`          | `dict`        | 一个字典，存储仅限关键字参数（keyword-only arguments）的默认值。                                                         |
| `__annotations__`         | `dict`        | 一个字典，存储函数的类型提示（Type Hints），包括参数注解和返回值注解。                                                   |
| 代码与字节码属性          |               |                                                                                                                          |
| `__code__`                | `code object` | 字节码对象，包含以下属性                                                                                                 |
| `__code__.co_varnames`    | `tuple`       | 一个元组，包含函数所有的局部变量名（包括参数名）                                                                         |
| `__code__.co_freevars`    | `tuple`       | 如果函数是闭包，包含了闭包内的引用变量（自由变量）                                                                       |
| `__code__.co_argcount`    | `int`         | 函数的参数个数（不包含 `*args` 和 `**kwargs`）                                                                           |
| `__code__.co_filename`    | `str`         | 函数定义所在的文件名                                                                                                     |
| `__code__.co_firstlineno` | `int`         | 函数定义所在的起始行号                                                                                                   |
| `__code__.co_code`        | `str`         | 实际的字节码指令序列（通常用于底层分析）                                                                                 |
| 运行环境与闭包属性        |               |                                                                                                                          |
| `__globals__`             | `dict`        | 一个字典，引用函数定义时所在的全局命名空间。即使函数被移动到其他地方，它仍然通过这个属性查找全局变量                     |
| `__closure__`             | `tuple`       | 一个元组，包含闭包单元格（cells），见上面闭包示例                                                                        |
| 用户自定义属性            |               |                                                                                                                          |
| `__dict__`                | `dict`        | 用户自定义属性                                                                                                           |

```python
def outer(x):
    """这是一个外部函数"""
    def inner(y):
        return x + y
    return inner

# 创建闭包
add_five = outer(5)

# 1. 基础属性
print(f"函数名: {add_five.__name__}")       # inner
print(f"文档: {outer.__doc__}")             # 这是一个外部函数

# 2. 代码对象属性
print(f"局部变量: {outer.__code__.co_varnames}") # ('x', 'inner')

# 3. 闭包属性 (关键)
print(f"闭包内容: {add_five.__closure__}")     # (<cell at ...>,)
# 获取闭包中捕获的变量 x 的值
print(f"捕获的x值: {add_five.__closure__[0].cell_contents}") # 5

# 4. 默认值与注解
def demo(a: int, b=10, *, c=20) -> int:
    return a + b + c

print(f"默认值: {demo.__defaults__}")       # (10,) -> 对应 b
print(f"关键字默认值: {demo.__kwdefaults__}") # {'c': 20}
print(f"注解: {demo.__annotations__}")      # {'a': <class 'int'>, 'b': <class 'int'>, 'c': <class 'int'>, 'return': <class 'int'>}

# 5. 自定义属性
demo.author = "Alice"
print(f"自定义属性: {demo.__dict__}")       # {'author': 'Alice'}
```

## lambda 函数

Python 中的 lambda 函数，也称为匿名函数，是一种用于创建小型、一次性函数的简洁语法。它允许你在需要函数对象的地方快速定义一个函数，而无需使用 def 关键字进行正式的命名。

基本语法：

```
lambda 参数列表：单个表达式
```

- `lambda`: 定义匿名函数的关键字。
- 参数列表: 与普通函数一样，可以包含任意数量的参数（位置参数、默认值、`*args`、`**kwargs`），参数之间用逗号分隔。
- 单个表达式: 这是 lambda 函数最关键的限制。它只能包含一个表达式，该表达式的计算结果会自动作为函数的返回值。不能包含 return、if-else 语句块、for 循环、try-except 等复杂语句。

> 与 JavaScript 语言中箭头函数概念一致 args => expression，但是箭头函数可以是使用 { expression } 形成多语句的代码块，python限制只能单个表达式。觉得更纯粹。

```python
# 使用 lambda 定义
add_lambda = lambda a, b: a + b

# 等价的 def 定义
def add(a, b):
  return a + b

print(add_lambda(2, 3))  # 输出: 5
print(add(2, 3))         # 输出: 5
```

lambda 函数的最大价值在于作为参数传递给高阶函数（即接收函数作为参数的函数），比如与内置的序列处理函数（map / filter / reduce 等）结合。

```python
numbers = [1, 2, 3, 4, 5]

# map: 计算每个数字的平方
squares = list(map(lambda x: x * x, numbers))
print(squares)  # 输出: [1, 4, 9, 16, 25]

# filter: 筛选出偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)    # 输出: [2, 4]

# reduce: 计算所有数字的乘积
from functools import reduce
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 输出: 120

# 在排序或查找最值时，key 参数允许你指定一个函数来定义排序或比较的规则。
users = [
    {'name': 'Alice', 'age': 25, 'score': 85},
    {'name': 'Bob', 'age': 30, 'score': 90},
    {'name': 'Charlie', 'age': 25, 'score': 95}
]

# 按年龄升序排序
sorted_users = sorted(users, key=lambda x: x['age'])

# 按年龄升序，同年龄则按分数降序排序
sorted_users = sorted(users, key=lambda x: (x['age'], -x['score']))

# 找出分数最高的人
top_scorer = max(users, key=lambda x: x['score'])
```

在许多情况下，列表推导式（List Comprehension） 或 生成器表达式 是比 `map()/filter() + lambda` 更符合 Python 风格的替代方案，通常也更易读。

```python
numbers = [1, 2, 3, 4, 5]

# 使用 map + lambda
squares_map = list(map(lambda x: x * x, numbers))

# 使用列表推导式 (更 Pythonic)
squares_lc = [x * x for x in numbers]
```

## 生成器函数

在 Python 中，生成器函数（Generator Function）是一种用于创建迭代器的特殊函数。生成器函数与普通函数最根本的区别在于它使用了 yield 关键字返回值，而不是 return。

### 生成器函数的声明和调用

声明一个生成器函数，只需要把 `return` 替换成 `yield` 即可。

```python
def gen()
  yield 1
  yield 2
```

与普通函数最大区别在于函数调用。普通函数调用后直接返回 `return` 的值。但是生成器函数调用后，返回的是一个迭代器对象。要想手动获取内部 `yield` 返回值，需要通过内置函数 `next` 调用。

```python
itor = gen()
next(itor) # 1
next(itor) # 2
next(itor) # StopIteration 异常
```

生成的迭代器一般入参给 `for` 循环自动迭代。

```python
for n in itor
  print(n) # 输出 1 2
```

### 生成器表达式

生成器函数另一种生成方式是 **生成器表达式**，与列表推导式语法类似，但使用圆括号 () 而不是方括号 []。它同样会返回一个生成器对象，而不是一个完整的列表。

```python
# 列表推导式：立即创建并存储整个列表
squares_list = [x * x for x in range(10)]

# 生成器表达式：创建一个生成器对象，按需计算
squares_gen = (x * x for x in range(10))

print(type(squares_gen))  # <class 'generator'>

for n in squares_gen
  print(n)
```

### 生成器函数的优势和应用场景

生成器函数的核心优势在于惰性求值和内存效率，它能优雅地解决一些特定问题，比如大列表数据，数据流等。它的惰性求值，与一次性将所有数据加载到内存中的列表不同，生成器函数能够按需生成并返回一个值，然后暂停执行，等待下一次请求。

1. 内存效率

这是生成器最显著的优点。当处理海量数据时，使用生成器可以避免内存溢出（OOM），因为它一次只在内存中保存一个数据项。

- 列表方式 (内存占用高): `[x**2 for x in range(100000000)]` 会尝试将所有结果存入内存。
- 生成器方式 (内存占用低): `(x**2 for x in range(100000000))` 只会创建一个轻量级的生成器对象。

2. 处理数据流和大型文件

生成器非常适合处理流式数据，例如逐行读取一个巨大的日志文件，而无需一次性将整个文件加载到内存中。

```python
def read_large_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

for line in read_large_file('huge_log.txt'):
    # 处理每一行
    pass
```

### 生成器函数内部与外部的双向通信 `send`

生成器不仅可以通过 `next()` 获取值，还可以通过 `send(value)` 方法向生成器内部发送一个值。这个值会成为生成器中当前 yield 表达式的结果，实现了生成器与外部的双向通信。

```python
def counter():
    count = 0
    while True:
        # 接收外部发来的值，如果没有发送则为 None
        increment = yield count
        if increment is not None:
            count += increment

c = counter()
# 在首次调用 send() 之前，必须先用 next() 启动生成器，或者使用 send(None)。否则会引发 TypeError。
print(next(c))      # 启动生成器，输出: 0
print(c.send(5))    # 发送 5，count 变为 5，输出: 5
print(c.send(2))    # 发送 2，count 变为 7，输出: 7
```

### 错误处理

使用 generator.throw(Exception) 方法，在生成器内部的 yield 表达式处抛出一个异常。

```python
# Python
def safe_gen():
    try:
        yield 1
    except ValueError:
        yield "Caught an error!"

g = safe_gen()
print(next(g))      # 输出: 1
print(g.throw(ValueError())) # 输出: Caught an error!
```

### 委托生成器

就是一个生成器内部调用另一个生成器。使用 `yield from iterable`

```python
# Python
def gen_a():
    yield 1
    yield 2

def gen_b():
    yield "start"
    yield from gen_a()  # 委托给 gen_a
    yield "end"

print(list(gen_b()))  # 输出: ['start', 1, 2, 'end']
```

### python生成器函数与 JavaScript 生成器函数的区别

| 特性             | Python                       | JavaScript                       |
| :--------------- | :--------------------------- | :------------------------------- |
| 定义语法         | `def func():` + `yield`      | `function* func()` + `yield`     |
| 获取下一个值     | `next(generator)`            | `generator.next()`               |
| 返回值结构       | 直接返回值                   | 对象 `{ value: ..., done: ... }` |
| 向内部传值       | `generator.send(value)`      | `generator.next(value)`          |
| 抛出错误         | `generator.throw(Exception)` | `generator.throw(Exception)`     |
| 委托给其他生成器 | `yield from other_gen()`     | `yield* otherGen()`              |

## 装饰器函数

Python 装饰器（Decorator）本质上是高阶函数，它接收一个函数作为参数，并返回一个新的函数。

### 装饰器函数的声明

一个标准的、能处理任意参数的装饰器通常包含以下结构：

- 外部函数作为参数传入：接收被装饰的函数 func 作为参数。
- 内部包装函数 (wrapper)：定义新的逻辑，并使用 `*args` 和 `**kwargs` 来接收和传递任意参数给原函数 func。
- `functools.wraps`：这是一个非常重要的细节。使用 `@functools.wraps(func)` 装饰 wrapper 函数，可以保留原函数 func 的元数据（如 `__name__`, `__doc__` 等），避免在调试时产生混淆。
- 返回包装函数：外部函数返回 wrapper。

```python
import functools

def my_decorator(func):
  """装饰器函数声明"""

    @functools.wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        # --- 在原函数执行前添加逻辑 ---
        print("函数执行前...")

        # 调用原函数，并捕获其返回值
        result = func(*args, **kwargs)

        # --- 在原函数执行后添加逻辑 ---
        print("函数执行后...")

        return result # 返回原函数的结果

    return wrapper
```

### 装饰器函数的调用

装饰器使用 `@`符号作为标识，放在被装饰的函数的上方。

```python
@my_decorator
def greet(name, age):
    """一个简单的问候函数"""
    print(f"你好，{name}，今年{age}岁。")
    return "问候完成"

greet("小明", 18)
# 输出:
# 函数执行前...
# 你好，小明，今年18岁。
# 函数执行后...
```

### 多个装饰器函数调用顺序

一个函数可以被多个装饰器装饰。它们的执行顺序是从下到上，或者说从内到外。即与目标函数最近的装饰器函数先执行。

```python
@decorator_one
@decorator_two
def my_function():
    pass
```

这等价于 `my_function = decorator_one(decorator_two(my_function))`。decorator_two 会先包装 my_function，然后 decorator_one 再去包装 decorator_two 返回的新函数。

### 带参数的装饰器

如果你希望装饰器本身也能接收参数（例如，指定重试次数），就需要再增加一层函数嵌套。`装饰器工厂函数 -> 真正的装饰器 -> 包装函数 (wrapper)`

```python
def repeat(times): # 1. 装饰器工厂，接收装饰器参数
    def decorator(func): # 2. 真正的装饰器，接收被装饰的函数
        @functools.wraps(func)
        def wrapper(*args, **kwargs): # 3. 包装函数，接收函数参数
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3) # 使用装饰器时传入参数
def say_hello():
    print("Hello!")

say_hello()
# 输出 3 次 "Hello!"
```

### 类装饰器函数

装饰器不仅可以装饰函数，也可以装饰类。类装饰器接收一个类作为参数，并返回一个修改后的类或新的类。

```python
def add_method(cls):
    """一个为类添加新方法的装饰器"""
    cls.new_method = lambda self: print("这是一个新方法！")
    return cls

@add_method
class MyClass:
    def __init__(self):
        pass

obj = MyClass()
obj.new_method() # 输出: 这是一个新方法！
```

## 异步函数

Python 的异步编程（Asynchronous Programming）是现代 Python（Python 3.5+）新增语法。它允许程序在等待某些耗时操作（如网络响应）完成时，不阻塞线程，而是转而去执行其他任务，从而极大提升效率。通常应用于处理高并发、IO密集型任务（如网络爬虫、Web服务、文件读写）等场景。

Python 的异步编程基于 协程 (Coroutine) 实现，主要由两个关键字和一个核心对象组成：

- async def: 用于定义一个异步函数（协程函数）。
- wait: 用于等待一个异步操作完成。
- 事件循环 (Event Loop): 异步编程的“心脏”，负责调度和运行所有的协程。

通常与非阻塞的异步库（如 aiohttp, asyncpg，asyncio）结合使用。

```python
import asyncio

# 1. 定义异步函数
async def fetch_data(url):
    print(f"开始请求: {url}")
    # 2. 模拟耗时 IO 操作 (注意使用 asyncio.sleep 而不是 time.sleep)
    await asyncio.sleep(2)
    print(f"完成请求: {url}")
    return f"数据: {url}"

# 3. 定义主入口函数
async def main():
    # 直接调用不会执行，只会返回协程对象，必须使用 await 或 create_task
    await fetch_data("http://example.com")

# 4. 启动事件循环
if __name__ == "__main__":
    asyncio.run(main())
```

> 与 JavaScript 的异步语法 async / await 比较，通常需要配合实现了 Promise 的函数配合使用。只不过在 python 中类比 Promise 的功能不是内置对象，而是通过类似 asyncio 异步库实现。

### 并发执行

通常配合 `asyncio.create_task` 或 `asyncio.gather` 函数实现。

> 类比 JavaScript 中 new Promise() 和 Promise.all()

- `asyncio.create_task()` 后台调度。立即创建一个任务并在后台运行，不阻塞当前流程。适用需要“发射后不管”的后台任务，或精细控制单个任务的生命周期。
- `asyncio.gather(*tasks)` 并发聚合。并发运行多个任务，并等待所有任务完成，返回结果列表。最常用。批量处理无依赖的任务（如同时爬取10个网页）。

```python
async def main():
    # 方式一：使用 gather 并发执行（推荐），同 Promise.all() 基本一致
    results = await asyncio.gather(
        fetch_data("URL A"),
        fetch_data("URL B"),
        fetch_data("URL C")
    )
    print(results) # 所有任务几乎同时完成

    # 方式二：使用 create_task，类似自定义 new Promise() 实现。
    task1 = asyncio.create_task(fetch_data("URL A"))
    task2 = asyncio.create_task(fetch_data("URL B"))
    await task1 # 等待 task1
    await task2 # 等待 task2
```

### 注意事项

- 在异步代码中使用阻塞 IO：这是最致命的错误。如果你在 async 函数中使用了同步的阻塞库（如 time.sleep、requests），整个事件循环会被卡死，异步将退化为同步，甚至更慢。比如 `time.sleep(1)` 应改为`await asyncio.sleep(1)`; `requests.get(url)` 应改为 `aiohttp` 等异步库。
- 忘记添加 `await`: 直接调用异步函数而不加 await，只会得到一个协程对象，代码块根本不会执行，且通常会报 `RuntimeWarning: coroutine was never awaited`。
- 在同步函数中直接调用异步函数: 你不能在普通的 def 函数里直接 await 异步函数，在普通函数中要调用异步函数，可以使用 `asyncio.run(async_func())`

```python
def sync_func():
    # await fetch_data("URL") # SyntaxError
    asynio.run(fetch_data("URL"))
```
