# 数据库

在 [web章节](./network_web_cgi_wsgi_asgi.md)中，提到一条计算机格言：

“All problems in computer science can be solved by another level of indirection（计算机科学中的所有问题都可以通过增加一个间接层来解决）” -- David Wheeler（剑桥大学计算机科学教授）

在 python 语言中使用数据库进行数据持久化编程开发中，这条格言同样适用。

## DB-API：地基与标准

> Why：为了解决“各自为战”的混乱

在 Python 早期，如果你想连接 MySQL，你得学一套指令；想连接 SQLite，又得学另一套完全不同的指令。这就像每个国家的插座标准都不一样，你每去一个国家都得带个新转接头，非常麻烦。

DB-API (Python Database API Specification v2.0) 是 Python 官方给所有数据库驱动制定的统一接口规范。它规定了所有数据库驱动必须实现的方法（如 connect() 连接、cursor() 游标、execute() 执行、fetchone() / fetchall() 查找、 commit() 提交、rollback() 回滚等）。

作用：

- 统一标准： 它让 Python 代码与数据库驱动之间的交互有了统一的标准。
- 解耦： 开发者只需要写符合 DB-API 的代码，理论上换个数据库（比如从 MySQL 换到 PostgreSQL），只需要换一下驱动包，核心代码逻辑不用大改。

局限：虽然统一了接口，但你依然需要手写 SQL 语句（字符串拼接）。这不仅繁琐，还容易出现 SQL 注入漏洞，且代码中充斥着数据库特有的方言（比如分页查询，MySQL 和 Oracle 的写法就不一样）。

## ORM：思想与进化

> Why：为了解决“手写 SQL 的痛苦”与“对象-关系阻抗失配”）

有了 DB-API，我们虽然能连数据库了，但还是得像个“SQL 搬运工”一样，把 Python 的数据手动拼成 SQL 字符串。

比如，你要存一个用户，你得写 `INSERT INTO users (name, age) VALUES ('Alice', 18)`。

这就产生了一个矛盾：Python 是面向对象的（操作的是类/对象），而数据库是关系型的（操作的是表/行）。 这两者之间存在“阻抗失配”。

另外，不同的数据库方言的 SQL 语法也不一样。比如 MySQL 的 INSERT 语句是 `INSERT INTO`，而 Oracle 的 INSERT 语句是 `INSERT ALL` 等等问题。

ORM (Object-Relational Mapping，对象关系映射) 是一种编程思想。它的核心目标是：让你像操作 Python 对象一样操作数据库，彻底告别手写 SQL。

作用：

- 映射： 它建立了一座桥梁，把“数据库的表”映射为“Python 的类”，把“表中的行”映射为“类的实例”。
- 自动化： 当你执行 `user.save()` 时，ORM 会在后台自动帮你生成并执行 `INSERT` 语句，并且抹平不同数据库方言的 SQL 差异，自动处理参数转义，杜绝 SQL 注入。

ORM 是一种编程理论，一个抽象的概念，你可以用 Python 实现 ORM，也可以用 Java 实现（如 Hibernate）。它不是特指某一个库。

## SQLAlchemy：集大成者

> Why：为了在 Python 中完美落地 ORM 思想并提供更多可能）

既然有了 ORM 这个好思想，我们需要一个强大的工具来实现它。虽然 Python 有很多 ORM 库（如 Django ORM, Peewee），但 SQLAlchemy 是公认的“王者”。

SQLAlchemy 是 Python 生态中最著名、功能最强大、最主流、工业级标准 ORM 框架，同时也是一个 SQL 工具包。
作用与联系：

- 它是 ORM 的实现者： SQLAlchemy 完美地实现了 ORM 思想。你定义 Python 类，它帮你管理数据库表结构。
- 它是 DB-API 的管理者： SQLAlchemy 并不直接连接数据库，它底层依赖不同类型数据库的 DB-API 驱动（如 pymysql 或 psycopg2）。它通过 DB-API 发送 SQL，并接收结果。

SQLAlchemy 的主要功能分为两层：

- Core：SQL 工具包（写更优雅的 SQL）
- ORM：完整实现 ORM 功能

```
+---------------------------------+
|        你的 Python 应用代码        |
|  (操作 User 对象: user.name = "Bob") |
+------------------+--------------+
                   |
+------------------v--------------+
|      SQLAlchemy ORM 层           |
| (将 User 对象翻译成 SQL 表达式)     |
+------------------+--------------+
                   |
+------------------v--------------+
|      SQLAlchemy Core 层          |
| (构建最终的 SQL 语句: UPDATE ...) |
+------------------+--------------+
                   |
+------------------v--------------+
|        DB-API 驱动层             |
| (如: psycopg2, PyMySQL)          |
+------------------+--------------+
                   |
+------------------v--------------+
|        关系型数据库              |
| (如: PostgreSQL, MySQL)          |
+---------------------------------+
```

## 示例

以 MySQL 为例，创建一个 User 类，并使用 SQLAlchemy ORM 层操作数据库，实现 CURD 功能。

1. 安装依赖

```bash
uv add sqlalchemy pymysql
```

然后确保 MySQL 已经启动，并创建一个数据库：

```sql
CREATE DATABASE IF NOT EXISTS test_db DEFAULT CHARSET utf8mb4;
```

2. 连接数据库，并创建数据表 user

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# --- 1. 数据库连接配置 ---
# 格式: mysql+pymysql://用户名:密码@主机地址:端口/数据库名?charset=编码
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/testdb?charset=utf8mb4"

# 创建数据库引擎 (Engine)
# echo=True 会在控制台打印生成的 SQL 语句，方便调试
engine = create_engine(DATABASE_URL, echo=True)

# 创建 Session 类
# Session 是我们与数据库交互的句柄，所有的操作都通过它完成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建模型基类
# 所有自定义的模型类都需要继承这个 Base
Base = declarative_base()

# --- 2. 定义 User 模型类 ---
class User(Base):
    # 指定映射的数据库表名
    __tablename__ = 'users'

    # 定义表的列，这些类属性将映射为表的字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="用户ID")
    name = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, comment="用户邮箱")
    age = Column(Integer, nullable=True, comment="用户年龄")

    # 为了方便打印，可以重写 __repr__ 方法
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', age={self.age})>"

# --- 3. 操作数据库的函数 ---

def create_table():
    """在数据库中创建表（如果不存在）"""
    # Base.metadata.create_all 会根据模型类的定义，自动生成并创建所有表
    print(">>> 正在检查并创建数据表...")
    Base.metadata.create_all(bind=engine)
    print(">>> 数据表检查/创建完成。")

def create_user(db, name, email, age):
    """创建并添加一个新用户"""
    # 1. 实例化 User 对象
    new_user = User(name=name, email=email, age=age)
    # 2. 添加对象 (此时还未提交到数据库)
    db.add(new_user)
    # 3. 提交会话，执行 INSERT 语句
    db.commit()
    # 刷新对象，获取数据库自动生成的 id 和 create_time
    db.refresh(new_user)
    print(f">>> 成功创建用户: {new_user}")
    return new_user

def read_users(db):
    """查询所有用户"""
    # 1. 查询所有用户
    all_users = db.query(User).all()
    print("所有用户:", all_users)

    # 2. 查询单个用户（按主键）
    user = db.query(User).get(1)  # get 按主键查询，无数据返回 None
    print("主键为1的用户:", user)

    # 3. 条件查询（filter）
    # 等于
    user_by_name = db.query(User).filter(User.name == "张三").first()
    print("姓名为张三的用户:", user_by_name)

    # 大于/小于
    users_age_gt_25 = db.query(User).filter(User.age > 25).all()
    print("年龄大于25的用户:", users_age_gt_25)

    # 模糊查询（like）
    users_like_li = db.query(User).filter(User.name.like("%李%")).all()
    print("姓名含李的用户:", users_like_li)

    # 4. 排序（order_by）
    users_order_by_age = db.query(User).order_by(User.age.desc()).all()
    print("按年龄降序排列:", users_order_by_age)

    # 5. 分页（offset 偏移，limit 条数）
    page_users = db.query(User).offset(0).limit(2).all()
    print("第1页（2条）:", page_users)

def update_user(db, user_id, new_age):
    """根据ID更新用户年龄"""
    print(f">>> 正在更新ID为 {user_id} 的用户年龄为 {new_age}...")
    # 使用 .get() 方法通过主键查询，非常高效
    user = db.get(User, user_id)
    if user:
        user.age = new_age
        db.commit()
        db.refresh(user)
        print(f">>> 更新成功: {user}")
    else:
        print("- 未找到该用户")

def delete_user(db, user_id):
    """根据ID删除用户"""
    print(f">>> 正在删除ID为 {user_id} 的用户...")
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
        print(f">>> 删除成功: {user}")
    else:
        print("- 未找到该用户")

# --- 4. 主程序入口 ---
if __name__ == "__main__":
    # 首先创建表
    create_table()

    # 创建一个会话实例，所有的数据库操作都在这个会话中进行
    # 使用 with 语句可以确保会话在使用后自动关闭，即使发生异常
    with SessionLocal() as db:
        try:
            # 1. 创建 (Create)
            user1 = create_user(db, "Alice", "alice@example.com", 25)
            user2 = create_user(db, "Bob", "bob@example.com", 30)

            # 2. 读取 (Read)
            read_users(db)

            # 3. 更新 (Update)
            update_user(db, user1.id, 26)

            # 4. 删除 (Delete)
            delete_user(db, user2.id)

            # 再次读取，确认操作结果
            read_users(db)

        except Exception as e:
            # 如果发生任何错误，回滚事务，保证数据一致性
            db.rollback()
            print(f"发生错误，事务已回滚: {e}")
```
