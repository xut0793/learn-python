# Learn Python

学习 Python 的总结

2025 年 7 月 12 日

## 目录

- [x] 导论：如何学习编程语言
- [x] Python 语言简介
- **数据的表达**
  - [x] 数据类型: None,bool, int, float, str, bytes
  - [x] 数据引用: 标识符，变量，常量
  - [x] 数据运算：算术运算、关系运算、逻辑运算、位运算、成员运算、身份运算、运算符优先级、赋值运算符和复合赋值
  - [x] 数据转换：类型查看、类型转换、编码转换
  - [x] 数据抽象（数据结构）: list, tuple(namedtuple), dict(defaultdict, OrderedDict), set(frozenset)
  - [ ] 理解数据的不可变性和可变性，以及 Python 中一切皆对象
- **流程的表达**
  - [x] 顺序: 从上到下逐行执行
  - [x] 分支：if, elif, else
  - [x] 循环：for, while
  - [x] 结构模式匹配 match
- **代码复用和抽象的封装**
  - [x] 函数
    - [x] 函数声明
    - [x] 函数调用
    - [x] 函数形参：无参、位置参数、关键字参数、仅位置参数/、仅关键字参数*、不定长位置参数*args、不字长关键字参数\*\*kwargs
    - [x] 函数实参：可变参数和不可变参数
    - [x] 函数返回值
    - [x] 文档字符串
    - [x] 嵌套函数
    - [x] 作用域 LEGB: Local、Enclosing、Global、BuiltIn
    - [x] 闭包
    - [x] 递归
    - [x] 函数内部属性
    - [x] lambda 函数
    - [x] 生成器函数
    - [x] 装饰器函数
    - [x] 异步函数
  - [x] 面向对象编程
    - [x] 类 class
    - [x] 对象：类的实例
    - [x] 构建函数和初始函数 `__init__`
    - [x] 属性
      - [x] 实例属性
      - [x] 类属性
    - [x] 方法
      - [x] 实例方法
      - [x] 类方法
      - [x] 静态方法
      - [x] 属性方法
    - [x] 封装: `@property` 属性装饰器
    - [x] 继承：单继承、多继承、MRO
    - [x] 多态：Duck Typing
    - [x] 抽象类: ABC
    - [x] 魔术方法
    - [x] 数据类
    - [x] 枚举类
  - [x] 模块
    - [x] 导入机制
    - [x] 模块搜索路径
    - [x] 缓存机制
  - [x] 包
    - [x] `__init__.py`：包的元数据、公共API、导入行为控制、初始化逻辑
    - [x] 绝对导入与相对导入
- **异常**
  - [x] 产生错误（报错）: raise
  - [x] 捕获错误: try, except, finally
  - [x] 排查错误（调试）: pdb, logging
  - [x] 预防错误（测试）: pytest, doctest
- **高并发的实现**
  - [ ] 多进程: multiprocessing
  - [ ] 多线程: threading
  - [ ] 并发： concurrent
  - [ ] 异步: asyncio
- **标准库**
  - [x] 内置常量
  - [x] 内置函数
  - [ ] 文本操作
  - [ ] 数学
  - [ ] 数据类型
  - [ ] 数据压缩和存档
  - [ ] 函数式编程
  - [x] 系统和文件
    - [x] 系统 os
    - [x] io 流
    - [x] 文件路径 pathlib
    - [x] 文件操作 open
  - [ ] 命令行
  - [ ] 网络
    - [x] urllib
    - [ ] socket
    - [ ] socketserver
    - [ ] http
    - [ ] http.client 和 urllib.request
  - [ ] 数据库
- **项目工程化**
  - [ ] 项目环境隔离: .venv uv
  - [ ] 项目结构
  - [ ] 项目配置: pyproject.toml
  - [ ] 项目部署
- **项目练习**
  - [ ] web 开发: fastapi, django
  - [ ] 自动化测试
  - [ ] 网络爬虫
  - [ ] 系统运维
  - [ ] 数据分析: pandas, numpy, matplotlib, seaborn
  - [ ] 人工智能: pytorch

## python 学习路线

python 应用方向：web 开发、网络爬虫、系统运维、数据分析、人工智能

- [ ] 第一步：工具安装，环境搭建；
- [ ] 第二步：基础语法，磨炼功底；
- [ ] 第三步：高级编程，雷打基础；
- [ ] 第四步：python 常用库
- [ ] 第五步：web框架，样样精通；Django / Flask / FastAPI
- [ ] 第六步：网络爬虫，神奇有趣；Requests、BeautifulSoup、Scrapy、Selenium、PyQuery、Lxml、Pandas、Pyppeteer、aiohttp、Faker和ProxyPool。
- [ ] 第七步：自动化测试 pytest allure
- [ ] 第八步：自动化运维，轻松而自在；Linux、Nginx、Shell
- [ ] 第九步：python数据分析，抓数据走向；numpy / pandas
- [ ] 第十步：机器学习，Python中的高端；
- [ ] 第十一步：深度学习，建大模型；
- [ ] 第十二步：开源项目，高手上位；
- [ ] 第十三步：求职面试，非我莫属；
