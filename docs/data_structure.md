<!--
 * @Date         : 2025-07-30 10:57:38 星期3
 * @Author       : xut
 * @Description  :
-->

# 基础数据结构

基本数据类型（bool、int、float、bytes）就像我们学会了认识单个字，然后字可以词、成语一样，简单的数据类型可以组成一些常用的数据结构，比如列表List、元组tuple、集合Set、字典Dict。

## 列表 List

列表是最常用的数据结构，是一种有序、可变的集合，列表的元素可以是其它各种数据类型。

### 列表创建方式

- 字面量形式 `[]`
- 构造函数 `list`
- 列表推导式 `[expression for item in iterable if condition]`
- 切片 `[start:end]`

```python
# 1. 字面量形式，最常用的方式，直接使用方括号 []
fruits = ["苹果", "香蕉", "橙子"]
empty = []
mixed = [1, "hello", false]

# 2. 使用构建函数 list,通常用于将其它数据类型转为列表时使用
empty = list()
chars = list("hello") # 构建函数支持其它数据类型入参,转为列表, chars 相当于 ["h", "e", "l", "l", "o"]

# 3. 列表推导式,这是一种高级语法,用来批量生成列表元素
numbers = [i for i in range(10)] # 结果：[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
squares = [x * x for x in range(1, 11)] # 结果：[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
evens = [x for x in range(10) if x % 2 == 0]

# 4. 切片 list[start:end]
parts = fruits[1:2] # ["香蕉"]
```

### 列表的操作

#### 列表自身的操作方法

列表的操作基本分四大类:增、删、改、查。

| 操作分类    | 常用方法/语法      | 作用说明                                    | 是否会改变原列表 |
| :---------- | :----------------- | :------------------------------------------ | ---------------- |
| 增 (Add)    | `append(x)`        | 在末尾添加一个元素                          | 是               |
|             | `extend(iterable)` | 把另一个列表的所有元素拼接到末尾            | 是               |
|             | `insert(i, x)`     | 在指定位置i插入元素x                        | 是               |
|             | `copy()`           | 返回一个浅拷贝的新列表                      | 否               |
| 删 (Delete) | `remove(x)`        | 删除第一个匹配的元素                        | 是               |
|             | `pop(i)`           | 删除并返回指定位置i的元素（默认删最后一个） | 是               |
|             | `clear()`          | 清空整个列表                                | 是               |
| 改 (Modify) | `list[i] = x`      | 直接修改指定索引的值                        | 是               |
|             | `sort()`           | 对列表进行排序                              | 是               |
|             | `reverse()`        | 反转列表顺序                                | 是               |
|             | `reverse()`        | 反转列表顺序                                | 是               |
| 查 (Query)  | `l[i]`             | 返回位置 i 上的元素                         | 否               |
|             | `index(x)`         | 查找元素第一次出现的位置                    | 否               |
|             | `count(x)`         | 统计元素x出现的次数                         | 否               |
|             | `x in list`        | 判断元素是否中列表中                        | 否               |

上述是这些方法都是 list 实例自身上定义的，通常 `list.method()` 调用，基本上都会改变 list 自身。

<details>
<summary>
代码示例
</summary>
<pre>
<code>
numbers = [1, 2, 3]
numbers.append(4)
print(numbers)  # Output: [1, 2, 3, 4]

numbers.extend([5, 6])
print(numbers) # Output: [1, 2, 3, 4, 5, 6]

numbers.insert(0, 0)
print(numbers) # Output: [0, 1, 2, 3, 4, 5, 6]

numbers.remove(3)
print(numbers) # Output: [0, 1, 2, 4, 5, 6]

numbers.pop()
print(numbers) # Output: [0, 1, 2, 4, 5]

numbers.reverse()
print(numbers) # Output: [5, 4, 2, 1, 0]

numbers.sort()
print(numbers) # Output: [0, 1, 2, 4, 5]

numbers.clear()
print(numbers) # Output: []

fruits = ['apple', 'banana', 'cherry']
print(fruits[0]) # Output: 'apple'
print(fruits.index('banana')) # Output: 1
print('cherry' in fruits) # Output: True
</code>

</pre>
</details>

#### 内置函数操作

还有另一类python语言全局的**内置函数**（意思是它们不需要 import 任何库，直接就能在任何地方使用）。

| 操作分类   | 常用方法/语法                | 作用说明                                                       | 是否会改变原列表 |
| :--------- | :--------------------------- | :------------------------------------------------------------- | ---------------- |
| 排序       | `sorted(iterable)`           | 排序，返回一个新的列表。不修改原数据                           | 否               |
| 迭代与生成 | `reversed(iterable)`         | 返回一个反转后的迭代器对象。不修改原数据                       | 否               |
|            | `range(start, stop)`         | 返回一个数字序列的迭代器对象，通常配合 for 循环使用            | 否               |
|            | `zip(iter1, iter2)`          | 返回一个迭代器对象，把两个列表“拉链”一样对应合并在一起         | 否               |
|            | `map(function, iterable)`    | 映射，返回一个迭代器对象，把列表里的每个元素都通过“函数”加工下 | 否               |
|            | `filter(function, iterable)` | 过滤，返回一个迭代器对象，把列表里符合条件的元素挑出来         | 否               |
| 统计查询   | `len(iterable)`              | 求长度                                                         | 否               |
|            | `sum(iterable)`              | 求和                                                           | 否               |
|            | `max(iterable)`              | 求最大值                                                       | 否               |
|            | `min(iterable)`              | 求最小值                                                       | 否是             |

像迭代相关的方法，都是返回一个迭代器对象 iterator，要将迭代器对象转为列表可以使用 list 构建函数 `list(iterator)`。

<details>
<summary>
代码示例
</summary>
<pre>
<code>
nums = [4, 2, 5, 4, 1]
sorted_numbers = sorted(nums)
print(sorted_numbers)  # Output: [1, 2, 4, 4, 5]

sort_reversed_numbers = sorted(nums, reverse=True)
print(sort_reversed_numbers) # Output: [5, 4, 4, 2, 1]

reversed_numbers = list(reversed(nums))
print(reversed_numbers) # Output: [1, 4, 5, 4, 2]

for i in reversed(nums):
print(i) # Output: 1, 4, 5, 2, 4 (in reverse order)

for i in range(1, 6):
print(i) # Output: 1, 2, 3, 4, 5

zip_numbers = zip([1, 2, 3], ['a', 'b', 'c'])
print(list(zip_numbers)) # Output: [(1, 'a'), (2, 'b'), (3, 'c')]
for i in zip_numbers:
print(i) # Output: (1, 'a'), (2, 'b'), (3, 'c')

squares = map(lambda x: x\*\*2, [1, 2, 3])
print(list(squares)) # Output: [1, 4, 9]

filtered_numbers = filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
print(list(filtered_numbers)) # Output: [2, 4]

numbers = [1, 2, 3, 4, 5]
print(len(numbers)) # Output: 5
print(sum(numbers)) # Output: 15
print(min(numbers)) # Output: 1
print(max(numbers)) # Output: 5
</code>

</pre>
</details>

#### 切片 `[start:end]`

```python
chars = ["a", "b", "c"]
a = chars[1,2] # ["b"]
b = chars[-1:] # ["c"]
c = chars[:-1] # ["a", "b"]
d = chars[:] # ["a", "b", "c"]
```

#### 解包 unpacking

解包接收的变量必须和元素个数一致，不然会报 `ValueError: too many values to unpack`

```python
chars = ["a", 1]
a, b = chars
print(a) # "a"
print(b) # 1
```

## 元组 Tuple

列表的特点是内部元素**有序、可重复，可变**，所以有相对应的增删改查的方法。

但是元组的特点是有序、可重复，但**不可变**，即元组是只读的，一量创建，里面的元素就不能改变了。

### 元组创建的方式

- 字面量形式 `()`
- 构造函数 `tuple`

```python
# 1. 字面量形式
t1 = (1, "a")
t2 = (1,) # 如果圆括号内只有一项时，必须加逗号结尾，不然就变成表达式求值了。

# 2. 构造函数形式 tuple(iterable)
t3 = tuple(["a", "b"]) # ("a", "b")

# 3. 切片操作
t4 = t3[0:1]
```

### 元组的操作

因为元组的不可变性，所以自身操作方式较少。

| 操作分类   | 常用方法/语法 | 作用说明                 | 是否会改变原列表 |
| :--------- | :------------ | :----------------------- | ---------------- |
| 查 (Query) | `t[i]`        | 返回位置 i 上的元素      | 否               |
|            | `index(x)`    | 查找元素第一次出现的位置 | 否               |
|            | `count(x)`    | 统计元素x出现的次数      | 否               |
|            | `x in list`   | 判断元素是否中列表中     | 否               |

但是同列表一样，内置函数、切片、解包操作，对元组都可用。

```python
t1 = ("a", 1, False)

print(t1[0]) # a
print(t1.index("a")) # 0
print(t1.count(False)) # 1
print("a" in t1) # True

t2 = t1[:-1] # ("a", 1)
a, b = t2
print(a) # "a"
print(b) # 1
```

## 集合 Set

集合的特点是**无序、不重复、可变**

### 集合的创建方式

- 字面量形式 `{}`
- 构造函数形式 `set`
- 集合推导式 `{expression for item in iterable if condition}`

```python
even_numbers = {0,2,4}

s1 = set([1,2])
s2 = set(('a', 'b'))

# 当将字典作为参数传入set()时，只有键会被使用。
s3 = set({"a": 1, "b": 2}) # {"a", "b"}
```

### 集合的操作方式

因为集合是可变的，所以对应的操作方式基本同列表一样。

## 不可变集合 frozenset

如果想创建一个不变、又没有重复元素的集合，可以使用 `frozenset` 构造函数。

```python
fs = frozenset([3, 2, 1])
fs.add(4)

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: 'frozenset' object has no attribute 'add'
```

## 字典 Dict

### 字典的创建方式

- 字面量形式 `{k: v}`
- 构造函数 `dict`
- 字典推导式 `{key_expression : value_expression for item in iterable if condition}`

```python
# 1. 字面量形式
d1 = {"a": 1, "b": "123"}

# 2. 构造函数 dict
d2 = dict(a=1, b="123")

d1 == d2 # True

# 3. 构造函数作为类型转换函数
# 双项列表的列表可以作为键值对映射成字典
lol = [ ['a', 'b'], ['c', 'd'], ['e', 'f'] ]
dict(lol) # {'a': 'b', 'c': 'd', 'e': 'f'}

# 双项元组列表映射成字典
lot = [ ('a', 'b'), ('c', 'd'), ('e', 'f') ]
dict(lot) # {'a': 'b', 'c': 'd', 'e': 'f'}

# 双项列表元组映射成字典
tol = ( ['a', 'b'], ['c', 'd'], ['e', 'f'] )
dict(tol) # {'a': 'b', 'c': 'd', 'e': 'f'}

# 双字符串列表映射成字典
los = [ 'ab', 'cd', 'ef' ]
dict(los) # {'a': 'b', 'c': 'd', 'e': 'f'}

# 双字符元组映射成字典
tos = ( 'ab', 'cd', 'ef' )
dict(tos) # {'a': 'b', 'c': 'd', 'e': 'f'}

# 4. 字典推导式
word = "letters"
letter_counts = { letter: word.count(letter) for letter in set(word)}
# {'t': 2, 'l': 1, 'e': 2, 'r': 1, 's': 1}
```

### 字典的操作方法

| 方法名     | 语法示例                     | 功能描述       | 返回值/备注                                                |
| :--------- | :--------------------------- | :------------- | :--------------------------------------------------------- |
| get        | `d.get(key, default)`        | 获取指定键的值 | 若键不存在，返回 `default` (默认None)，不会报错。          |
| keys       | `d.keys()`                   | 获取所有键     | 返回一个视图对象，可动态反映字典变化。                     |
| values     | `d.values()`                 | 获取所有值     | 返回一个视图对象，可动态反映字典值的变化。                 |
| items      | `d.items()`                  | 获取所有键值对 | 返回 `(key, value)` 元组的视图对象，可动态反映字典的变化。 |
| update     | `d.update(other_dict)`       | 批量更新字典   | 将 `other_dict` 的键值对更新进来，重复键会被覆盖。         |
| pop        | `d.pop(key, default)`        | 删除指定键     | 返回被删除的值。若键不存在且未设默认值，报错。             |
| popitem    | `d.popitem()`                | 删除最后一对   | 返回 `(key, value)` 元组。Python 3.7+ 删除最后插入的项。   |
| clear      | `d.clear()`                  | 清空字典       | 移除所有元素，字典变为空 `{}`。                            |
| setdefault | `d.setdefault(key, default)` | 设置默认值     | 若键存在，返回原值；若不存在，插入并返回 `default`。       |
| fromkeys   | `dict.fromkeys(seq, val)`    | 创建新字典     | 这是一个类方法。用序列 `seq` 做键，初始值都为 `val`。      |
| copy       | `d.copy()`                   | 浅拷贝         | 复制一个字典对象。                                         |

其中特别注意 `keys / values / items` 方法在 python3 之后的版本，都是返回一个视图对象，并且会实时反映原始对象键值对变化的情况。如果需要得到对应的列表，需要使用 `list()` 函数转换。

```python
d1 = {"a":1, "b": "123"}
ret_keys = d1.keys()
ret_values = d1.values()
ret_items = d1.items()

print(ret_keys) # dict_keys(['a', 'b'])
print(ret_values) # dict_values([1, '123'])
print(ret_items) # dict_items([('a', 1), ('b', '123')])

d1.setdefault("c", False)

print(ret_keys) # dict_keys(['a', 'b', 'c'])
print(ret_values) # dict_values([1, '123', False])
print(ret_items) # dict_items([('a', 1), ('b', '123'), ('c', False)])

keys = list(ret_keys) # ['a', 'b', 'c']
values = list(ret_values) # [1, '123', False]
items = list(ret_items) # [('a', 1), ('b', '123'), ('c', False)]
```

### 合并多个字典值的方式

类似 JavaScript 语言中的 `{...obj1, ...obj2}`

python 的操作符号是 `{**obj1, **obj2}`

```python
obj1 = {"a": 1, "b": 2}
obj2 = {"b": 3, "c": 4}

ret = {**obj1, **obj2} # {"a": 1, "b": 3, "c": 4}
```

另一种不产生新对象的合并方式，python 也提供 `obj.update(other)` 方法

```python
obj1 = {"a": 1, "b": 2}
obj2 = {"b": 3, "c": 4}

obj1.update(obj2) # obj1 = {"a": 1, "b": 3, "c": 4}
```
