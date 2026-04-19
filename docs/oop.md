# 面向对象编程（OOP）

面向对象编程（Object-Oriented Programming，简称 OOP）是一种编程范式，它使用"类和对象"来组织代码。对象是类的实例，类是对象的模板。

Python 是一门完全支持面向对象编程的语言。

## 什么是面向对象编程

以下内容摘自 《Java 开发手册》 ch6.1

软件开发的过程就是人们使用各种计算机语言将自身关心的现实世界（问题域）映射到计算机世界（目标域）的过程。

```
现实世界问题域 +--> 建立模型    +-->  编程实现     +--->  计算机世界
               借助某种建模思想    借助某种编程语言         执行求解

```

### 对象

对象是现实世界中的事物，在人脑中的映像，这种映像通过对同一类事物的抽象，反应在人脑中的意识，并作为一种概念而存在。这个概念就是现实世界当中的事物在人们意识当中的抽象。只要这个对象存在于人们的思维意识当中，人们就可以借此判断同类的东西。

例如，当人们认识到一种新事物，它叫苹果，看到它是圆形的，可以吃，味道是甘甜的，于是人脑中就形成了苹果的概念，知道它的特征（苹果的颜色、形状、重量等）和行为（苹果可以吃、可以被人吃、可以用来榨汁等）。

### 面向对象

面向对象（Object-Oriented）是一种方法或者思想，它追求更客观，更自然的描述现实世界，使得分析、设计和实现软件系统跟认识客观世界的过程尽可能的一致。

客观世界是由许多不同种类的对象构成的，每一个对象都有自己的运动规律和内部状态，不同对象之间相互联系、相互作用。

面向对象技术从组成客观世界的对象着眼，通过抽象，将对象映射到计算机系统中，又通过模拟对象之间的相互作用、相互联系来模拟现实客观世界，描述客观世界的运动规律。

### 面向对象编程

面向对象编程（Object-Oriented Programming，OOP）是将面向对象技术在计算机中通过编程实现。

从编程开发的角度来看，所谓对象被定义为一个封装了状态（数据）和行为（操作方法）的实体。

程序员可以通过定义一个对象集合，以及它们之间的相互作用来创建一个面向对象的程序，让许多对象协同工作来完成一个用户需要的软件系统。

### 面向对象编辑的特征

在 OOP 中，程序被看作相互协作的对象集合，每个对象都是某个类的实例，所有类构成一个通过继承或者组合形成的相互联系的层次结构。

所以面向对象的语言通常具有以下实现：

- 类和遗传机制：类 class 声明、继承。
- 对象生成功能：实例。
- 消息沟通机制: 方法调用。

这些实现机制使得 OOP 具有以下特征：

- 封装 encapsulation：将数据和操作数据的方法封装在一起，形成一个对象，有限制的对外提供方法调用。
- 继承 inheritance：一个类可以派生出新的类，新的类可以继承父类的属性和方法，并且可以添加新的属性和方法。
- 多态 polymorphism：对象的方法可以有多种不同的实现。从消息传递的机制看，同样的消息接口（同一个方法）为不同对象接收时可以做出不同的行动。

## 类的声明与定义

在 Python 中，使用 `class` 关键字声明类：

```python
class Person:
    """人类"""
    pass
```

## 对象的创建

使用类名加括号创建对象：

```python
class Person:
    pass

# 创建对象
p1 = Person()
p2 = Person()

print(type(p1))  # <class '__main__.Person'>
print(p1 == p2)  # False，不同实例
```

## `__init__` 方法

`__init__` 在创建对象时自动调用，用于初始化对象的属性。`self` 代表类的实例，指向对象本身。

```python
class Person:
    def __init__(self, name, age):
        self.name = name  # 实例属性
        self.age = age

# 创建对象时传入参数
p = Person("张三", 25)
print(p.name)  # 张三
print(p.age)   # 25
```

> **注意**：`__init__` 不是构造函数，真正创建对象的是 `__new__`，从`__init__` 方法的入参 self 也可以知道，此时实例对象已经实现。具体见下文的魔法方法章节

## 2. 属性

### 2.1 实例属性

实例属性属于具体对象，每个对象拥有独立的副本。

```python
class Dog:
    def __init__(self, name):
        self.name = name  # 实例属性

dog1 = Dog("旺财")
dog2 = Dog("小黑")

print(dog1.name)  # 旺财
print(dog2.name)  # 小黑
```

### 2.2 类属性

类属性属于类本身，所有对象共享同一份数据。

```python
class Dog:
    species = "犬科动物"  # 类属性

    def __init__(self, name):
        self.name = name

dog1 = Dog("旺财")
dog2 = Dog("小黑")

print(dog1.species)  # 犬科动物
print(dog2.species)  # 犬科动物
print(Dog.species)   # 犬科动物，通过类名访问
```

### 2.3 实例属性与类属性的区别

| 特性     | 实例属性                       | 类属性                         |
| -------- | ------------------------------ | ------------------------------ |
| 归属     | 属于对象                       | 属于类                         |
| 数量     | 每个对象独立拥有               | 所有对象共享                   |
| 定义位置 | `__init__` 方法中              | 类体中，方法外                 |
| 访问方式 | `self.属性名` 或 `对象.属性名` | `类名.属性名` 或 `对象.属性名` |

### 2.4 属性的访问与修改

```python
class Dog:
    species = "犬科动物"

    def __init__(self, name):
        self.name = name

dog = Dog("旺财")

# 访问属性
print(dog.name)      # 旺财
print(dog.species)   # 犬科动物

# 修改实例属性
dog.name = "大黄"
print(dog.name)      # 大黄

# 修改类属性
Dog.species = "哺乳动物"
print(dog.species)   # 哺乳动物
```

### 2.5 动态添加属性

Python 允许在运行时动态给对象添加属性：

```python
class Dog:
    def __init__(self, name):
        self.name = name

dog = Dog("旺财")

# 动态添加实例属性
dog.age = 3
print(dog.age)  # 3

# 动态添加类属性
Dog.species = "犬科"
print(dog.species)  # 犬科
```

> **注意**：动态添加的属性只对当前对象有效，不会影响其他对象。

## 3. 方法

### 3.1 实例方法

实例方法是类中最常用的方法，第一个参数必须是 `self`。

```python
class Person:
    def __init__(self, name, age: int):
        self.name = name
        self.age = age

    def introduce(self):
        """实例方法"""
        print(f"我叫{self.name}，今年{self.age}岁")

p = Person("张三", 25)
p.introduce()  # 我叫张三，今年25岁
```

### 3.2 类方法（`@classmethod`）

类方法使用 `@classmethod` 装饰器，第一个参数是 `cls`，代表类本身。

```python
class Person:
    count = 0  # 类属性，记录人数

    def __init__(self, name):
        self.name = name
        Person.count += 1

    @classmethod
    def get_count(cls):
        """类方法"""
        return cls.count

p1 = Person("张三")
p2 = Person("李四")

print(Person.get_count())  # 2
print(p1.get_count())      # 2
```

### 3.3 静态方法（`@staticmethod`）

静态方法使用 `@staticmethod` 装饰器，是指不接收任何隐式的第一参数（既没有 `self` 也没有 `cls` 参数）的一类方法。

本质上就是一个普通的函数，只是被“静态”地放置在了类的命名空间中，以表明它在逻辑上属于这个类。

静态方法适用于与类相关但不依赖实例或类状态的工具函数。

```python
class MathUtils:
    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def is_even(n: int) -> bool:
        return n % 2 == 0

print(MathUtils.add(3, 5))       # 8
print(MathUtils.is_even(4))      # True
```

### 3.4 属性方法（`@property`）

使用 `@property` 装饰器可以将方法像属性一样访问。通常用于类属性的封装（对属性访问和设置进行验证）。

```python
class Person:
    def __init__(self, name, age: int):
        self.name = name
        self._age = age  # 使用下划线表示内部属性

    @property
    def age(self):
        """获取年龄"""
        return self._age

    @age.setter
    def age(self, value: int):
        """设置年龄"""
        if 0 <= value <= 150:
            self._age = value
        else:
            raise ValueError("年龄必须在 0-150 之间")

    # 你可以在使用 del 语句删除属性时执行一些清理操作，例如释放资源或重置状态。
    @age.deleter
    def age(self):
        """删除年龄"""
        print("正在清理数据...")
        self._age = None

p = Person("张三", 25)
print(p.age)      # 25，像属性一样访问
p.age = 30        # 通过 setter 设置
print(p.age)      # 30
del p.age         # 正在清理数据...
```

## 4. 封装

在Python中，对于相关封装的方式，更像一种君子协定，python世界中认为你是一个成年人，你仍然可以访问它，但你不应该这样做，或者做了后果自负。

> 不像 Java 、 JavaScript 语言中，程序编译器或解释器对越级访问会报错。

### 4.1 公有属性与方法

默认情况下，Python 中的属性和方法都是公有的，可以从类外部访问。

```python
class Person:
    def __init__(self, name):
        self.name = name  # 公有属性

    def say_hello(self):  # 公有方法
        print(f"Hello, I'm {self.name}")

p = Person("张三")
print(p.name)      # 张三
p.say_hello()      # Hello, I'm 张三
```

### 4.2 私有属性与方法（`__` 双下划线）

以双下划线开头的属性或方法是私有的，只能在类内部访问。

```python
class BankAccount:
    def __init__(self, owner, balance: float):
        self.owner = owner
        self.__balance = balance  # 私有属性

    def __get_balance(self):  # 私有方法
        return self.__balance

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
            print(f"存款 {amount}，余额: {self.__balance}")

    def withdraw(self, amount: float):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"取款 {amount}，余额: {self.__balance}")
        else:
            print("余额不足")

account = BankAccount("张三", 1000)
account.deposit(500)   # 存款 500，余额: 1500
account.withdraw(200)  # 取款 200，余额: 1300

# 无法直接访问私有属性
# print(account.__balance)  # AttributeError
print(account._BankAccount__get_balance()) # 可以访问
```

> **说明**：Python 的私有是通过**名称改写**实现的，`__balance` 实际变成了 `_BankAccount__balance`。

### 4.3 受保护的属性与方法（`_` 单下划线）

单下划线表示受保护的属性，是一种约定，表示"请勿随意访问"，但 Python 不会强制限制。

```python
class Person:
    def __init__(self, name):
        self._name = name  # 受保护的属性

    def _internal_method(self):  # 受保护的方法
        pass
```

> **约定**：受保护的属性应该只在类和子类中使用。

### 4.4 Getter 和 Setter 方法

传统的 getter/setter 模式：

```python
class Person:
    def __init__(self, name, age: int):
        self.name = name
        self._age = age

    def get_age(self):
        return self._age

    def set_age(self, age: int):
        if 0 <= age <= 150:
            self._age = age
        else:
            raise ValueError("年龄无效")

p = Person("张三", 25)
print(p.get_age())  # 25
p.set_age(30)
print(p.get_age())  # 30
```

### 4.5 使用 `@property` 属性装饰器

推荐使用 `@property` 属性装饰器实现属性访问控制

| 装饰器            | 功能              | 触发时机                            |
| :---------------- | :---------------- | :---------------------------------- |
| `@property`       | 定义 getter 方法  | 读取属性时，如 `obj.attr`           |
| `@属性名.setter`  | 定义 setter 方法  | 为属性赋值时，如 `obj.attr = value` |
| `@属性名.deleter` | 定义 deleter 方法 | 删除属性时，如 `del obj.attr`       |

```python
class Person:
    def __init__(self, name, age: int):
        self.name = name
        self._age = age  # 使用下划线表示内部属性

    @property
    def age(self):
        """获取年龄"""
        return self._age

    @age.setter
    def age(self, value: int):
        """设置年龄"""
        if 0 <= value <= 150:
            self._age = value
        else:
            raise ValueError("年龄必须在 0-150 之间")

    # 你可以在使用 del 语句删除属性时执行一些清理操作，例如释放资源或重置状态。
    @age.deleter
    def age(self):
        """删除年龄"""
        print("正在清理数据...")
        self._age = None

p = Person("张三", 25)
print(p.age)      # 25，像属性一样访问
p.age = 30        # 通过 setter 设置
print(p.age)      # 30
del p.age         # 正在清理数据...
```

## 5. 继承

### 5.1 单继承

子类可以继承父类的所有属性和方法。

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} 发出声音")

class Dog(Animal):  # Dog 继承 Animal
    def speak(self):
        print(f"{self.name} 汪汪叫")

dog = Dog("旺财")
dog.speak()  # 旺财 汪汪叫
```

### 5.2 继承中的 `__init__` 调用

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, student_id):
        super().__init__(name)  # 必须先调用父类 __init__
        self.student_id = student_id

s = Student("张三", "2024001")
print(s.name)        # 张三
print(s.student_id)  # 2024001
```

### 5.3 `super()` 函数的使用

使用 `super()` 调用父类的方法。

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类 __init__
        self.breed = breed

    def info(self):
        print(f"名字: {self.name}, 品种: {self.breed}")

dog = Dog("旺财", "金毛")
dog.info()  # 名字: 旺财, 品种: 金毛
```

### 5.4 方法重写（Override）

子类可以重写父类的方法。

```python
class Animal:
    def speak(self):
        print("动物发出声音")

class Cat(Animal):
    def speak(self):
        print("喵喵喵")

class Dog(Animal):
    def speak(self):
        print("汪汪汪")

cat = Cat()
cat.speak()  # 喵喵喵

dog = Dog()
dog.speak()  # 汪汪汪
```

### 5.5 多继承

Python 支持一个类继承多个父类。

```python
class Flyable:
    def fly(self):
        print("我会飞！")

class Swimmable:
    def swim(self):
        print("我会游泳！")

class Duck(Flyable, Swimmable):
    pass

duck = Duck()
duck.fly()  # 我会飞！
duck.swim()  # 我会游泳！
```

### 5.6 方法解析顺序（MRO）

在 Python 的类继承中，MRO 是 **Method Resolution Order**（方法解析顺序）的缩写。

简单来说，它是一条明确的规则，决定了当你在一个继承了多个父类的子类实例上调用一个方法时，Python 应该按照什么样的顺序去这些类中查找该方法。

#### MRO 的核心：C3 线性化算法

Python 使用一种名为 C3 线性化算法 的机制来计算 MRO。这个算法保证了方法查找顺序的确定性和一致性，主要遵循以下几个原则：

- 子类优先：在查找方法时，子类总是比它的父类优先被检查。
- 从左到右：在多重继承中，父类的声明顺序很重要。Python 会按照 class Child(Parent1, Parent2) 中 Parent1 在前，Parent2 在后的顺序进行查找。
- 单调性：一个类在其所有子类的 MRO 中，相对顺序是保持一致的，不会出现矛盾。
- 避免重复：在继承链中，同一个父类（尤其是共同的祖先类）只会被查找一次。

#### 查看 MRO

你可以通过以下两种方式来查看任何一个类的 MRO：

- 使用类的 `__mro__` 属性，它会返回一个元组。
- 调用类的 `mro()` 方法，它会返回一个列表。

```python
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")

class C(A):
    def method(self):
        print("C.method")

class D(B, C):
    pass

d = D()
d.method()  # B.method

# 查看 MRO
print(D.mro())  # [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]
print(D.__mro__) # (D, B, C, A, object)
```

#### 解决“菱形继承”问题

```
    A
   / \
  B   C
   \ /
    D
```

在这个结构中，B 和 C 都继承自 A，而 D 又同时继承 B 和 C。如果没有 MRO，当 D 的实例调用一个在 A 中定义的方法时，Python 将不知道应该通过 B 还是 C 去找 A，可能会导致 A 的方法被调用两次或产生歧义。MRO 通过 C3 算法，确保了 A 在查找顺序中只出现一次，并且位置在 B 和 C 之后。

#### 多重继承中 super 调用

```python
class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        print("Hello from B")
        super().greet()  # 根据 MRO，调用 A.greet

class C(A):
    def greet(self):
        print("Hello from C")
        super().greet()  # 根据 MRO，调用 A.greet

class D(B, C):
    def greet(self):
        print("Hello from D")
        super().greet()  # 根据 D 的 MRO (D->B->C->A)，调用 B.greet

d = D()
d.greet()
# 输出:
# Hello from D
# Hello from B
# Hello from C
# Hello from A
```

#### MRO 冲突

如果继承关系定义不当，导致 C3 算法无法找到一个满足所有规则（特别是单调性）的线性顺序，Python 就会抛出一个 TypeError，提示无法创建一致的 MRO。

```python
class X: pass
class Y: pass
class A(X, Y): pass # A 的 MRO 要求 X 在 Y 之前
class B(Y, X): pass # B 的 MRO 要求 Y 在 X 之前

# 下面这行代码会报错，因为无法调和 A 和 B 的矛盾顺序
class C(A, B): pass
# TypeError: Cannot create a consistent method resolution order (MRO) for bases A, B
```

## 6. 多态

Python 的多态是**隐式的**，不需要接口声明，只要对象有相应的方法即可调用（Duck Typing）。

### 6.1 多态的概念

多态是指不同对象对同一消息可以有不同的响应（多种形态）。

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪"

class Cat(Animal):
    def speak(self):
        return "喵喵"

def make_animal_speak(animal: Animal):
    print(animal.speak())

make_animal_speak(Dog())  # 汪汪
make_animal_speak(Cat())  # 喵喵
```

### 6.2 鸭子类型（Duck Typing）

Python 是动态类型语言，遵循"鸭子类型"原则：如果一个对象走起来像鸭子，叫起来像鸭子，那它就是鸭子。

```python
class Duck:
    def quack(self):
        print("嘎嘎")

class Person:
    def quack(self):
        print("我会学鸭子叫，嘎嘎")

def make_it_quack(thing):
    thing.quack()

make_it_quack(Duck())   # 嘎嘎
make_it_quack(Person()) # 我会学鸭子叫，嘎嘎
```

### 6.3 方法重写实现多态

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

shapes = [Rectangle(3, 4), Circle(5)]
for shape in shapes:
    print(f"面积: {shape.area()}")
```

## 抽象类

顾名思意，抽象类就是抽象的类。抽象是相对于具体而言的，一般来说，具体类的都有对应实例对象的具体实现，而抽象类则不能直接实例化。

从面向对象的角度来看，类是现实世界中事物分类在计算机世界的一种映射。现实世界中，对具体事物的分类之上也都会有一个抽象的类别，比如，狗是具体的对象，而动物是抽象的类别；苹果是具体的对象，而水果是抽象的类别。

抽象类是定义抽象方法的类。抽象类不能被实例化，只能被继承，抽象方法必须被子类实现。

### 为什么需要抽象类

类的继承的缺点之一，**继承破坏了封装性**，主要体现在：

- 对于子类而言，通过继承实现是没有安全保障的，因为父类修改内部实现细节，它的功能就可能会被破坏；
- 而对于基类而言，让子类能继承和随意重写方法，也是破坏了基类封装的目的，而且也让父类丧失了能自由修改内部实现的自由。

引入抽象方法和抽象类，用来约束了类的行为，引导使用者正确使用它们，减少误用。当类继承于某个抽象类时，子类就知道它必须要实现所有的抽象方法，而不可能忽略，如果被忽略程序会提示错误。

无论是编写程序，还是平时做其他事情，每个人都可能会犯错，减少错误不能只依赖人的优秀素质，还需要一些机制，使得一个普通人都容易把事情做对，而难以把事情做错。抽象类提供的这样一种机制，在语言层面提供这些约束机制，让开发者把事情做对，不容易做错。

```
Traceback (most recent call last):
  File "f:\xx\oop.py", line 12, in <module>
    dog = Dog()
TypeError: Can't instantiate abstract class Dog without an implementation for abstract method 'eat'
```

### 定义抽象类

在Python中创建抽象类，我们使用 abc 模块（抽象基类 abstract base class）实现。

- 导入必要的 abc 模块
- 通过继承ABC来创建你的抽象类
- 使用`@abstractmethod`装饰器定义抽象方法

```python
from abc import ABC, abstractmethod

class Shape(ABC):
  @abstractmethod
  def area(self):
    pass

  @abstractmethod
  def perimeter(self):
    pass

class Rectangle(Shape):
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def area(self):
    return self.width * self.height

  def perimeter(self):
    return 2 * (self.width + self.height)

class Circle(Shape):
  def __init__(self, radius):
  self.radius = radius

def area(self):
  return 3.14 * self.radius ** 2

def perimeter(self):
  return 2 * 3.14 * self.radius

# 使用这些类
rect = Rectangle(5, 3)
circle = Circle(4)

print(f"矩形面积：{rect.area()}")
print(f"圆形周长：{circle.perimeter()}")
```

## 7. 特殊方法（魔术方法）

在 Python 中，特殊方法（Special Methods），也被称为魔术方法（Magic Methods）或双下方法（Dunder Methods），是赋予自定义类“魔法”般能力的核心机制。

它们是以双下划线开头和结尾的特殊方法名（如 `__init__`, `__str__`），允许你的对象与 Python 的内置函数、运算符和语法结构无缝交互。

魔术方法最“魔术”的地方在于，它们通常不是由你直接调用的，而是由 Python 解释器在特定的场景下自动触发。

- 当你执行 len(my_object) 时，Python 会在后台自动调用 my_object.**len**()。
- 当你执行 obj_a + obj_b 时，Python 会尝试调用 obj_a.**add**(obj_b)。
- 当你执行 print(my_object) 时，Python 会调用 my_object.**str**()。

通过实现这些方法，你可以让你的自定义对象表现得像内置类型（如列表、字典、数字）一样自然和直观。

简单来说，**魔术方法让你可以“重载”Python 的内置行为，使其作用于你自己的类上**。

| 魔术方法                                    | 触发时机                                   | 功能说明                                                                               |
| :------------------------------------------ | :----------------------------------------- | :------------------------------------------------------------------------------------- |
| 对象的生命周期                              |                                            |                                                                                        |
| `__new__(cls, ...)`                         | 实例化对象时最先调用                       | 负责创建并返回实例对象，常用于控制对象的创建过程，如实现单例模式。                     |
| `__init__(self, ...)`                       | 对象创建后立即调用                         | 负责初始化对象，设置实例属性。这是最常用的魔术方法。                                   |
| `__del__(self)`                             | 对象被垃圾回收时调用                       | 负责清理资源（如关闭文件、断开连接）。由于调用时机不确定，不建议依赖它。               |
| 对象的字符串表示                            |                                            |                                                                                        |
| `__str__(self)`                             | `print(obj)` 或 `str(obj)`                 | 返回一个对用户友好的、可读性强的字符串表示。                                           |
| `__repr__(self)`                            | `repr(obj)` 或在交互式命令行中直接输入对象 | 返回一个对开发者友好的、明确的字符串表示，理想情况下，该字符串应能用于重新创建该对象。 |
| `__format__(self, format_spec)`             | `format(obj, spec)` 或 f-string            | 定义对象在格式化字符串时的行为。                                                       |
| 运算符重载                                  |                                            |                                                                                        |
| `__add__(self, other)`                      | `+`                                        | 定义加法行为。                                                                         |
| `__sub__(self, other)`                      | `-`                                        | 定义减法行为。                                                                         |
| `__mul__(self, other)`                      | `*`                                        | 定义乘法行为。                                                                         |
| `__eq__(self, other)`                       | `==`                                       | 定义相等比较行为。                                                                     |
| `__lt__(self, other)`                       | `<`                                        | 定义小于比较行为。                                                                     |
| `__le__(self, other)`                       | `<=`                                       | 定义小于等于比较行为。                                                                 |
| 模拟容器行为                                |                                            |                                                                                        |
| `__len__(self)`                             | `len(obj)`                                 | 返回容器的“长度”。                                                                     |
| `__getitem__(self, key)`                    | `obj[key]`                                 | 获取指定键/索引的值。                                                                  |
| `__setitem__(self, key, value)`             | `obj[key] = value`                         | 设置指定键/索引的值。                                                                  |
| `__contains__(self, item)`                  | `item in obj`                              | 判断对象中是否包含某个元素。                                                           |
| `__iter__(self)`                            | `for x in obj`                             | 返回一个迭代器，使对象可迭代。                                                         |
| 属性控制                                    |                                            |                                                                                        |
| `__getattr__(self, name)`                   | 访问一个不存在的属性时                     | 提供一个后备机制来动态获取属性。                                                       |
| `__setattr__(self, name, value)`            | 任何属性赋值时                             | 拦截所有属性赋值操作，可用于数据校验。                                                 |
| `__getattribute__(self, name)`              | 任何属性访问时                             | 拦截所有属性访问操作，功能强大但需谨慎使用，避免无限递归。                             |
| `__slots__`                                 | 任何属性访问时                             | 用于限制类实例可以拥有的属性，节省内存                                                 |
| 上下文管理器                                |                                            |                                                                                        |
| `__enter__(self)`                           | 进入 `with` 代码块时                       | 执行 setup 逻辑，其返回值会被赋给 `as` 后面的变量。                                    |
| `__exit__(self, exc_type, exc_val, exc_tb)` | 离开 `with` 代码块时                       | 执行 teardown 逻辑，如关闭文件、释放锁等。                                             |
| 让对象可调用                                |                                            |                                                                                        |
| `__call__(self, ...)`                       | `obj()`                                    | 让一个实例对象可以像函数一样被调用。                                                   |

### `__new__` 和 `__init__`区别

`__new__` 负责“出生”（创建实例），`__init__` 负责“成长”（初始化属性）。

当你调用 `MyClass()` 创建一个对象时，Python 内部实际执行了以下两个步骤：

1. 调用 `__new__`：Python 首先调用 `__new__` 方法，并传入类本身（cls）。`__new__` 的职责是在内存中分配空间，创建并返回一个全新的实例。
1. 调用 `__init__`：只有当 `__new__` 返回的是当前类（或其子类）的实例时，Python 才会自动调用 `__init__` 方法，并将`__new__` 返回的实例作为 self 参数传入，进行初始化操作。

一个关键点：`__new__` 决定了 `__init__` 是否有机会执行。如果`__new__` 没有返回当前类的实例，`__init__` 将不会被调用。

但是在 99% 的情况下，你只需要使用 `__init__` 来初始化属性。`__new__` 主要用于一些高级场景。

```python
# 实现单例模式 Singleton
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("创建新实例")
            cls._instance = super().__new__(cls)
        else:
            print("返回已有实例")
        return cls._instance

s1 = Singleton()  # 输出: 创建新实例
s2 = Singleton()  # 输出: 返回已有实例
print(s1 is s2)   # 输出: True

# 控制实例创建过程,__new__ 可以返回任何对象，甚至可以返回 None 来阻止实例的创建。这为对象池、缓存等模式提供了可能。
class Demo:
    def __new__(cls):
        print("__new__ 被调用")
        # 返回一个字符串而不是 Demo 的实例
        return "Not a Demo instance"

    def __init__(self):
        # 这行代码永远不会执行！
        print("__init__ 被调用")

obj = Demo()
print(obj)  # 输出: Not a Demo instance
print(type(obj))  # 输出: <class 'str'>


# 继承不可变类型
# 当你需要继承像 int、str、tuple 这样的不可变类型时，必须在 __new__ 中修改值。因为 __init__ 执行时，不可变对象已经创建完成，无法再被修改。
class MyInt(int):
    def __new__(cls, value):
        # 在对象创建前，强制将值变为偶数
        if value % 2 != 0:
            value += 1
        return super().__new__(cls, value)

num = MyInt(5)
print(num)  # 输出: 6
```

### 其它方法示例

```python
"""__str__ 与 __repr__"""
class Person:
    def __init__(self, name, age: int):
        self.name = name
        self.age = age

    def __str__(self):
        """面向用户的字符串表示"""
        return f"Person({self.name}, {self.age})"

    def __repr__(self):
        """面向开发者的字符串表示"""
        return f"Person(name='{self.name}', age={self.age})"

p = Person("张三", 25)
print(p)         # Person(张三, 25)
print(repr(p))   # Person(name='张三', age=25)

"""__len__ 与 __getitem__ 与 __setitem__"""
class MyList:
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def append(self, item):
        self.data.append(item)

ml = MyList()
ml.append(1)
ml.append(2)
ml.append(3)

print(len(ml))    # 3
print(ml[0])      # 1
ml[0] = 10
print(ml[0])      # 10

"""实现了 __call__ 方法的对象可以像函数一样调用。"""
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count

c = Counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3


"""__add__ 和 __sub__ 重载运算符 + 和 -"""
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)  # Vector(4, 6)
print(v1 - v2)  # Vector(-2, -2)


"""析构方法 __del__"""
class Resource:
    def __init__(self, name):
        self.name = name
        print(f"{self.name} 已创建")

    def __del__(self):
        """对象被销毁时调用"""
        print(f"{self.name} 已销毁")

r = Resource("数据库连接")
del r  # 数据库连接 已销毁
```

> **注意**：Python 有垃圾回收机制，通常不需要手动实现 `__del__`。

### `__slots__` 的作用

`__slots__` 用于限制类实例可以拥有的属性，节省内存。

- 使用 `__slots__` 后，不能再动态添加未声明的属性
- 子类不会继承父类的 `__slots__`，需要在子类中重新定义
- 使用 `__slots__` 的类不会有 `__dict__` 属性

```python
class Person:
    __slots__ = ['name', 'age']  # 只允许这两个属性

    def __init__(self, name, age: int):
        self.name = name
        self.age = age

p = Person("张三", 25)
p.name = "李四"  # OK
# p.address = "北京"  # AttributeError: 'Person' object has no attribute 'address'
```

## 11. 数据类（`@dataclass`）

在Python中，数据类（dataclass）是一种用于创建包含数据属性的类的结构，它通过使用装饰器简化了类的创建过程。数据类自动为你生成一些特殊方法，如`__init__()`、`__repr__()`和`__eq__()`，这些方法基于类中定义的字段。

数据类的主要目的是存储数据，而不是定义复杂的行为或方法。

### 基本用法

数据类最基础的作用就是自动生成常用的魔术方法。

- 自动生成方法：默认情况下，`@dataclass` 会自动生成 `__init__`（初始化）、`__repr__`（字符串表示）和 `__eq__`（相等比较）。
- 类型提示：定义数据类时，必须使用类型注解（Type Hinting）来声明字段类型。

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
print(p)        # 自动生成的 __repr__: Point(x=1.0, y=2.0)
print(p.x)      # 访问属性: 1.0
```

### `@dataclass` 装饰器参数

```python
@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False,
           match_args=True, kw_only=False, slots=False, weakref_slot=False)
class C:
  pass
```

| 参数           | 默认值  | 作用说明                                                                                         |
| :------------- | :------ | :----------------------------------------------------------------------------------------------- |
| `init`         | `True`  | 生成 `__init__` 方法。                                                                           |
| `repr`         | `True`  | 生成 `__repr__` 方法。                                                                           |
| `eq`           | `True`  | 生成 `__eq__` 方法（用于 `==` 比较）。                                                           |
| `order`        | `False` | 生成比较方法（`__lt__`, `__le__`, `__gt__`, `__ge__`），用于 `<`, `>` 等比较。                   |
| `frozen`       | `False` | 设为 `True` 时，实例变为不可变（类似元组），修改属性会报错，实现只读属性。                       |
| `slots`        | `False` | 设为 `True` 时，生成 `__slots__`，节省内存并提升属性访问速度。                                   |
| `unsafe_hash`  | `False` | 设为 `True` 时，则生成`__hash__` 方法                                                            |
| `match_args`   | `True`  | 根据传给生成的 `__init__` 方法的非关键字形参列表来创建 `__match_args__` 元组                     |
| `kw_only`      | `False` | 设为 `True` 时，所有字段都将被标记为仅限关键字的，仅限关键字字段不会被包括在 `__match_args__` 中 |
| `weakref_slot` | `False` | 设为 `True` 时，则添加一个名为 `__weakref__` 的槽位，这是使得一个实例 可以弱引用 所必需的。      |

### 字段的高级配置

数据类提供了灵活的方式来处理字段的默认值和特殊行为。

- 默认值：可以直接赋值，但必须遵循“无默认值的字段在前，有默认值的字段在后”的规则（类似于函数参数）。
- `field()` 函数：用于更精细的控制。特别是处理可变默认值（如列表、字典）时，不能直接赋值（否则所有实例共享同一个列表），必须使用 default_factory。

```python
dataclasses.field(*, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None, kw_only=MISSING, doc=None)
```

> MISSING 值是一个哨兵对象，用于检测一些形参是否由用户提供。使用它是因为 None 对于一些形参来说是有效的用户值。任何代码都不应该直接使用 MISSING 值。

| 参数              | 默认值     | 作用说明                                                                                                                                                |
| :---------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `default`         | `MMISSING` | 如果提供，这将为该字段的默认值                                                                                                                          |
| `default_factory` | `MMISSING` | 如果提供，它必须是一个零参数的可调用对象，它将在该字段需要一个默认值时被调用                                                                            |
| `init`            | `True`     | 该字段将作为一个形参被包括在生成的 `__init__` 方法中                                                                                                    |
| `repr`            | `True`     | 该字段将被包括在生成的 `__repr__` 方法所返回的字符串中                                                                                                  |
| `hash`            | `None`     | 如为真值，则此字段将被包括在所生成的 `__hash__` 方法中。 如为假值，则此字段将被排除在所生成的 `__hash__` 之外。 如为 None (默认值)，则使用 compare 的值 |
| `compare`         | `True`     | 该字段将被包括在生成的相等和比较方法中 `__eq__`, `__gt__` 等                                                                                            |
| `kw_only`         | `MMISSING` | 如为真值，则该字段将被标记为仅限关键字的                                                                                                                |
| `doc`             | `None`     | 该字段的可选的文档字符串                                                                                                                                |
| `metadata`        | `None`     | 它完全不被数据类所使用，并且是作为第三方扩展机制提供的                                                                                                  |

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    name: str
    # 普通默认值
    active: bool = True
    # 可变默认值：每个实例都会创建一个新的空列表
    tags: List[str] = field(default_factory=list)
    # 排除在 repr 之外（例如密码）
    password: str = field(repr=False, default="secret")
```

### 后置处理钩子 `__post_init__`

数据类本身不强制数据验证，但你可以定义 `__post_init__` 方法。它会在自动生成的 `__init__` 执行完毕后立即运行，非常适合用来检查数据合法性。

```python
@dataclass
class Product:
    price: float
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("价格不能为负数")

@dataclass
class C:
    a: float
    b: float
    c: float = field(init=False)

    def __post_init__(self):
        self.c = self.a + self.b
```

### 使用场景

- 基于 `__post_init__` 实现数据验证。
- 不可变对象，使用 `@dataclass(frozen=True)` 可以创建不可变的数据结构。这在多线程环境或需要保证数据不被意外修改的场景下非常有用。
- 替代字典：相比于字典，数据类提供了更好的可读性、类型检查和 IDE 自动补全支持，非常适合用于 API 响应解析、配置项管理或数据库模型映射。并且可以使用 `dataclasses.asdict()` 将数据类实例轻松转换为字典，方便进行 JSON 序列化。

## 枚举类（`enum` 模块）

在 Python 中，枚举（Enum） 是一种用于定义一组固定的、相关的常量的类型。它从 Python 3.4 开始作为标准库 enum 提供。

使用枚举的核心目的是替代“魔法数字”或“魔法字符串”，将一组语义相关的常量封装成一个类，从而极大地提升代码的可读性、可维护性和类型安全性。

定义一个枚举非常简单，只需继承 Enum 类即可。每个成员都有两个核心属性：name（名称）和 value（值）。

```python
# ❌ 不推荐：魔法数字，可读性差
def process_order(status):
    if status == 1:
        print("处理待支付订单...")
    elif status == 2:
        print("处理已支付订单...")

# ✅ 推荐：使用枚举，语义清晰
from enum import Enum

class OrderStatus(Enum):
    PENDING = 1  # 待支付
    PAID = 2     # 已支付

def process_order(status: OrderStatus):
    if status == OrderStatus.PENDING:
        print("处理待支付订单...")
```

枚举类的作用：

- 类型安全：枚举成员不会与普通的数字或字符串混淆。Color.RED == 1 的结果是 False，这有效防止了意外的类型错误。
- 不可变性：枚举成员一旦定义，其值就不能被修改或重新赋值，保证了常量的稳定性。
- 可迭代：可以直接遍历一个枚举类，获取其所有成员。

### 检举项自动赋值 auto

当你不关心枚举成员的具体值时，可以使用 `auto() `让 Python 自动分配一个唯一值。

```python
from enum import Enum, auto

class Animal(Enum):
    DOG = auto()
    CAT = auto()
    MOUSE = auto()
```

### 强制值唯一 `@unique`

默认情况下，枚举允许不同名称的成员拥有相同的值（后者被视为前者的别名）。使用 `@unique` 装饰器可以强制要求所有成员的值必须唯一。

```python
from enum import Enum, unique

@unique
class Status(Enum):
    SUCCESS = 1
    # FAIL = 1  # 这会抛出错误，因为值重复了
    ERROR = 2
```

### 枚举添加方法

枚举类可以像普通类一样定义方法，实现更复杂的行为。

```python
class VIP(Enum):
    BRONZE = 1
    GOLD = 3

    def get_level_name(self):
        return {1: '初级', 3: '高级'}.get(self.value, '未知')

print(VIP.GOLD.get_level_name())  # 输出: '高级'
```

## 设计原则与实践

### SOLID 原则简介

SOLID 是五个面向对象设计原则的首字母缩写：

| 原则 | 全称                            | 名称         | 说明                                                                                                                     |
| ---- | ------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| S    | Single Responsibility Principle | 单一职责原则 | 一个类只负责一项职责，一个方法只负责一项功能。                                                                           |
| O    | Open Closed Principle           | 开闭原则     | 对扩展开放，对修改关闭。就是当别人要修改软件功能的时候，使得他不能修改我们原有代码，只能新增代码实现软件功能修改的目的。 |
| L    | Liskov Substitution Principle   | 里氏替换原则 | 所有父类能出现的地方，子类就可以出现，并且替换了也不会出现任何错误。                                                     |
| I    | Interface Segregation Principle | 接口隔离原则 | 类间的依赖关系应该建立在最小的接口上，接口的内容一定要尽可能地小，能有多小就多小。                                       |
| D    | Dependence Inversion Principle  | 依赖倒置原则 | 依赖抽象，而非具体实现。就是说我们应该面向接口编程。通过抽象成接口，使各个类的实现彼此独立，实现类之间的松耦合。         |

### 组合优于继承

组合是指在一个类中包含另一个类的实例，而非继承。

```python
class Engine:
    def start(self):
        print("引擎启动")

class Car:
    def __init__(self):
        self.engine = Engine()  # 组合

    def start(self):
        self.engine.start()
        print("汽车启动")

car = Car()
car.start()
```
