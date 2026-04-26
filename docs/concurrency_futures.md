# concurrent.futures

## What 是什么

Python3.2带来了 concurrent.futures 模块，它实现了一个高并发的接口，它在python的多线程`threading`、多进程 `multiprocesssing` 的基础上进一步封装，通过“池化”（线程池、进程池）的方式，极大的简化了线程和进程的使用。

`concurrent.futures`的功能，简单来说就是开辟一个固定大小为n的进程池/线程池。进程池中最多执行n个进程/线程，当任务完成后，从任务队列中取新任务。若池满，则排队等待。

池由两部分组成:

- 一部分是内部的队列，存放着待执行的任务；
- 另一部分是一系列的进程或线程，用于执行这些任务。

池的概念主要目的是为了重用：让线程或进程在生命周期内可以多次使用。它减少了创建创建线程和进程的开销，提高了程序性能。

## Why 为什么需要它

python 语言已经有内置模块 threading、multiprocess了，为什么还要整出一个concurrent.futures呢？

python 的 `threading` 模块没有提供线程池的功能，需要手动封装，另外，`multiprocessing` 模块提供了线程池（Pool）的功能，便是相比 `concurrent.futures` 模块实现的都是**异步**操作，池化技术带来的好处：

- `futures` 实现的 API 极其优雅：相比于手动创建一堆 `Thread` 或 `Process` 对象并逐一 `start()` 和 `join()`，`concurrent.futures` 的池化技术（Pool）能自动管理线程/进程的创建、复用和销毁。
- 结果获取方便：底层的 `threading` 获取线程返回值非常麻烦（通常需要借助 Queue），而 `concurrent.futures` 通过 `Future` 对象直接 `.result()` 就能拿到返回值或异常，代码逻辑非常清晰。
- 切换成本低：如果你发现原本用 `ThreadPoolExecutor` 写的 I/O 任务变成了计算瓶颈，只需把类名替换为 `ProcessPoolExecutor`，其余代码几乎不用改动。

## How 如何使用

`concurrent.futures` 模块由以下部分组成：

### 核心组件：两大执行器（Executor）

基于 `concurrent.futures.Executor` 虚拟基类，了两个子类：`concurrent.futures.ThreadPoolExecutor(max_workers)` 和 `concurrent.futures.ProcessPoolExecutor(max_workers)`，分别对应线程池和进程池：

- `ThreadPoolExecutor`：底层基于 `threading` 模块。适用于 I/O 密集型任务（如网络请求、文件读写、数据库操作）。
- `ProcessPoolExecutor`：底层基于 `multiprocessing` 模块。适用于 CPU 密集型任务（如大量数值计算、图像处理），能绕过 GIL（全局解释器锁）利用多核 CPU。

`Executor` 实例对象的方法：

- `executor.submit(fn, *args, **kwargs)`：提交一个任务，返回一个 `Future` 对象。
- `executor.map(func, *iterables)`：批量提交任务，返回一个获取 `Future` 的迭代器。
- `executor.shutdown(wait=True)`：关闭执行器，释放线程资源。

I/O 密集型（使用线程池并发抓取网页）适用于多线程并发

```python
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(url):
    time.sleep(1)  # 模拟网络请求的 I/O 等待
    return f"成功获取: {url}"

urls = [f"网址{i}" for i in range(5)]

start = time.time()
# 使用线程池，最大 3 个工作线程
with ThreadPoolExecutor(max_workers=3) as executor:
    # 批量提交任务
    futures = [executor.submit(fetch_data, url) for url in urls]

    # 哪个任务先完成就先打印哪个
    for future in as_completed(futures):
        print(future.result())

print(f"线程池总耗时: {time.time() - start:.2f}秒")
# 串行需要5秒，并发后大约只需2秒左右
```

CPU 密集型（使用进程池并行计算）适用于多进程并发

```python
import time
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):
    # 模拟繁重的 CPU 计算
    return sum(i * i for i in range(n))

numbers = [10**6] * 4

start = time.time()
# 使用进程池，最大 4 个工作进程
with ProcessPoolExecutor(max_workers=4) as executor:
    # map 会按输入顺序返回结果
    results = list(executor.map(cpu_task, numbers))

print(f"进程池总耗时: {time.time() - start:.2f}秒")
```

### 核心对象：Future

`Executor` 执行后，返回 `Future` 对象，用于保存异步任务的结果。`Future` 可以理解为“未来的结果”。当你`executor.submit()`提交一个任务，或者批量提交任务`executor.map()`后，会立刻拿到一个或迭代多个 `Future` 对象，它充当了异步任务的凭证。

- `f.done()`：判断任务是否已完成。
- `f.result(timeout=None)`：阻塞并获取任务的返回值（可设置超时时间）。
- `f.exception(timeout=None)`：判断任务是否抛出异常（可设置超时）。)`：获取任务执行时抛出的异常。
- `f.cancel()`：尝试取消任务（仅在任务未开始运行时有效）。
- `f.add_done_callback(fn)`：为任务绑定一个完成后的回调函数。

为什么叫future？可以理解为还未完成的任务，future封装了待完成的任务，实现了主进程和子进程之前的通信，比如查询完成状态，得到结果。

### 执行结果的获取

`Future` 结果获取有多种方式：

- 单个任务执行后，可以通过 `f.result()` 获取结果。
- 使用 `executor.map()` 批量执行任务，可以通过 `for f in executor.map(func, *iterables)` 迭代单个 `Future` 对象，然后通过 `f.result()` 获取结果。
- 使用 `concurrent.futures.as_completed()` 批量获取多个 `Future` 对象迭代器，然后通过 `f.result()` 获取结果。
- 使用 `concurrent.futures.wait(futures, return_when)` 通过返回值 `(done, not_done) `获取结果。

以下示例均以 ThreadPoolExecutor（线程池）为例，ProcessPoolExecutor（进程池）的用法完全一致。

#### 1. 单个任务提交（不使用 with 语句）

不使用 `with` 语句时，需要手动调用 `shutdown()` 方法来释放资源。

```python
import concurrent.futures
import time

def single_task(seconds):
    time.sleep(seconds)
    return f"休眠 {seconds} 秒的单个任务完成"

# 创建线程池执行器（不使用 with 语句）
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# 1. submit(fn, *args)：提交单个任务，立刻返回一个 Future 对象
future = executor.submit(single_task, 2)

print(f"任务是否刚提交就完成？ {future.done()}")  # 2. done()：检查任务是否完成，刚提交时为 False

# 3. result(timeout=None)：阻塞直到任务完成并获取返回值
# 如果任务执行超过 timeout 设定的秒数，会抛出 TimeoutError
try:
    result = future.result(timeout=3)
    print(f"任务结果：{result}")
except concurrent.futures.TimeoutError:
    print("任务执行超时！")

print(f"任务现在是否完成？ {future.done()}")  # 获取结果后，任务状态变为 True

# 4. 手动关闭执行器，释放线程资源
# wait=True 表示等待池中所有任务执行完毕后再关闭
executor.shutdown(wait=True)
```

#### 2. 单个任务提交（使用 with 语句 & 异常处理）

`with` 语句是官方推荐的最佳实践，它会在代码块执行完毕后自动调用 `shutdown()`，即使任务报错也能保证资源被安全释放。

```python
import concurrent.futures

def risky_task(divisor):
    # 模拟一个可能出错的计算
    return 100 / divisor

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future = executor.submit(risky_task, 0)  # 除数为0，必定报错

    # 调用 result() 或 exception() 都会阻塞直到任务完成
    # 调用 exception()：获取任务执行时抛出的异常，如果没有异常则返回 None
    exc = future.exception()
    if exc:
        print(f"任务捕获到异常：{type(exc).__name__} - {exc}")
    else:
        print(f"任务正常结果：{future.result()}")
```

#### 3. 多个任务并发 map

`executor.map(func, *iterables)` 方法用于批量提交任务，返回一个迭代器，迭代器中的元素是 `Future` 对象，按任务输入顺序返回。

比如说你有一堆数据，想用同样的函数去处理，并且只关心最终结果且希望顺序一致，直接用 map。它底层帮你完成了 submit 和结果收集的工作，代码最简洁。

```python
import concurrent.futures
import time
import random

def batch_task(task_id):
    sleep_time = random.uniform(0.5, 1.5)
    time.sleep(sleep_time)  # 模拟耗时不一致的任务
    return f"任务 {task_id} 耗时 {sleep_time:.2f}秒"

task_ids = [1, 2, 3, 4, 5]

print("--- 方式A：使用 executor.map() ---")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # map(func, *iterables)：批量提交，返回结果的迭代器（严格保持输入顺序）
    # 如果任务中抛出异常，迭代到该任务时会抛出异常
    results = executor.map(batch_task, task_ids)
    for res in results:
        print(f"按顺序拿到结果：{res}")
```

#### 4. 多个任务并发 as_completed

`concurrent.futures.as_completed()` 方法结果是一个生成器（迭代器）。它不会一次性返回结果，而是哪个任务先完成，它就立刻 yield 出那个任务的 Future 对象。

比如说比如你并发了100个爬虫任务，你希望爬完一个就立刻解析一个，而不是等100个全爬完再一起解析（那样内存可能会爆，且等待时间过长）。

```python
import concurrent.futures
import time
import random

def batch_task(task_id):
    sleep_time = random.uniform(0.5, 1.5)
    time.sleep(sleep_time)  # 模拟耗时不一致的任务
    return f"任务 {task_id} 耗时 {sleep_time:.2f}秒"

task_ids = [1, 2, 3, 4, 5]

print("\n--- 方式B：使用 as_completed() ---")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # 先提交所有任务，得到一组 Future 对象
    futures = [executor.submit(batch_task, i) for i in task_ids]

    # concurrent.futures.as_completed(fs)：哪个任务先做完，就先产出哪个 Future
    for future in concurrent.futures.as_completed(futures):
        try:
            print(f"抢先拿到结果：{future.result()}")
        except Exception as e:
            print(f"任务出错：{e}")
```

#### 5. 多个任务并发 wait

`concurrent.futures.wait(futures, return_when)` 方法的核心逻辑是“阻塞直到满足某个条件，然后返回一次结果”。当你调用它时，主线程会卡住，直到你设定的 return_when 条件被触发。一旦触发，它会立刻返回两个集合：done（已完成的任务）和 not_done（未完成的任务）。

- FIRST_COMPLETED：只要任意一个任务完成，wait 立刻返回。此时 done 里至少有一个任务，not_done 里是剩下的任务。
- ALL_COMPLETED（默认值）：死等所有任务全部跑完，才返回。此时 done 里是所有任务，not_done 是空集。
- FIRST_EXCEPTION：只要任意一个任务报错，就立刻返回；如果所有任务都正常跑完没报错，效果等同于 ALL_COMPLETED。

常用场景：

- 快速失败（Fail-Fast）：比如你提交了10个健康检查任务，只要有一个报错（FIRST_EXCEPTION），你就想立刻停止等待并报警，而不想等剩下9个跑完。
- 阶段性处理：比如只要有一个任务先完成（FIRST_COMPLETED），你就想先拿它的结果去触发下一步操作，剩下的任务让它们继续在后台跑。

```python
import concurrent.futures
import time
from concurrent.futures import wait, FIRST_COMPLETED

def demo_task(n):
    time.sleep(n)
    return n

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(demo_task, i) for i in [1, 2, 3]]

    # 10. wait(fs, return_when=...)：阻塞直到满足特定条件
    # return_when 可选：FIRST_COMPLETED (第一个完成), ALL_COMPLETED (全部完成)， FIRST_EXCEPTION (第一个异常)
    done, not_done = wait(futures, return_when=FIRST_COMPLETED)

    print(f"已完成的任务数：{len(done)}")
    print(f"未完成的任务数：{len(not_done)}")

    # 此时可以获取那个最快完成的任务结果
    print(f"最快完成的任务结果是：{done.pop().result()}")
```

差异对比：

| 维度     | executor.map()                         | concurrent.futures.as_completed()         | concurrent.futures.wait()                |
| :------- | :------------------------------------- | :---------------------------------------- | :--------------------------------------- |
| 交互模式 | 批量映射（最省心）                     | 流式处理（最实时）                        | 条件触发（最灵活）                       |
| 返回形式 | 结果的迭代器（直接是返回值）           | Future 对象的迭代器（需调用 `.result()`） | 一次性返回 `(done, not_done)` 两个集合   |
| 结果顺序 | 严格保持输入顺序                       | 谁先完成谁先出                            | 集合无序，需自行遍历处理                 |
| 典型场景 | 简单的数据并行计算（如批量计算、下载） | 实时获取结果（如爬虫解析、微服务调用）    | 需要打断等待或控制剩余任务（如快速失败） |

## `shutdown` 和 `cancel_futures` 区别

Python 3.9+ 新增 `concurrent.futures.cancel_futures(executor)` 取消指定执行器（Executor）中所有尚未开始运行的任务。

比如说当你的程序遇到致命错误，或者用户主动点击了“取消”按钮，你希望立刻停止线程池/进程池中还在排队等待的任务，以节省系统资源。

对比 `executor.shutdown(cancel_futures=True)`：

- `shutdown` 会直接关掉整个池子，之后不能再提交新任务。
- `cancel_futures` 只是清空排队区，池子本身还活着，你依然可以继续往里面提交新的任务。

```python
import concurrent.futures
import time

def task(n):
    time.sleep(1)
    return n

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # 提交 5 个任务，由于 max_workers=2，会有 3 个在排队
    futures = [executor.submit(task, i) for i in range(5)]

    time.sleep(1.5) # 等前两个任务开始跑，后面的还在排队

    # 取消所有还在排队的任务
    cancelled_count = concurrent.futures.cancel_futures(executor)
    print(f"成功取消了 {cancelled_count} 个排队任务")

    # 此时依然可以提交新任务，因为池子没被 shutdown
    new_future = executor.submit(task, 100)
    print(f"新任务的结果: {new_future.result()}")
```

## 进阶使用

### 进程池专属优化：chunksize 分块处理

在使用 `ProcessPoolExecutor` 的 map 方法时，有一个专为多进程设计的参数 `chunksize`。
当你需要处理海量的可迭代对象时，将任务分块打包发送给子进程，能显著减少进程间通信（IPC）的开销，从而大幅提升性能。

> chunksize 参数对 ThreadPoolExecutor 没有任何效果。

```python
import concurrent.futures

def cpu_intensive_task(n):
    return sum(i * i for i in range(n))

data = [10**5] * 1000  # 假设有1000个繁重的计算任务

# 使用 ProcessPoolExecutor 时，适当调大 chunksize 能提升效率
with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    # 默认 chunksize=1，意味着每个任务单独发送一次
    # 设置 chunksize=50，意味着每50个任务打包成一块发送给子进程
    results = list(executor.map(cpu_intensive_task, data, chunksize=50))
```

### 线程/进程池的初始化器：initializer 与 initargs

如果你的每个工作线程或进程在执行具体任务前，都需要进行一些统一的“准备工作”（比如建立数据库连接池、加载大型模型文件、配置日志等），可以使用 initializer 参数。它会在每个工作者启动时自动执行一次。

```python
import concurrent.futures
import threading

# 模拟为每个线程准备一个独立的数据库连接或资源
def worker_initializer(db_name):
    # 这里可以使用 threading.local() 或全局变量来存储线程专属资源
    thread_data = threading.local()
    thread_data.connection = f"为 {threading.current_thread().name} 建立的 {db_name} 连接"
    print(f"{threading.current_thread().name} 初始化完毕")

def process_task(task_id):
    # 在实际生产中，可以从 threading.local() 中取出连接使用
    return f"任务 {task_id} 正在使用已初始化的资源处理"

with concurrent.futures.ThreadPoolExecutor(
    max_workers=3,
    initializer=worker_initializer,
    initargs=("MyDatabase",)  # 传递给 initializer 的参数元组
) as executor:
    results = list(executor.map(process_task, [1, 2, 3]))
```

### 优雅处理执行器崩溃：捕获 BrokenExecutor

在生产环境中，底层的线程池或进程池可能会因为系统资源耗尽、子进程被外部强行杀死等原因意外崩溃。concurrent.futures 提供了专门的异常类来处理这种情况，避免程序直接崩溃。

- BrokenThreadPool：当线程池的工作线程初始化失败时引发。
- BrokenProcessPool：当进程池的某个工作进程被意外终止（例如内存溢出被系统 OOM Killer 杀掉）时引发。

```python
import concurrent.futures
from concurrent.futures.process import BrokenProcessPool

def heavy_computation(n):
    return n ** 1000

try:
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        future = executor.submit(heavy_computation, 10)
        print(future.result())
except BrokenProcessPool as e:
    print(f"警告：进程池已损坏，可能需要重启服务或检查系统资源。错误信息: {e}")
```

### 动态控制并发度：结合 Semaphore（信号量）

虽然 max_workers 限制了线程/进程池的大小，但如果你想在代码逻辑层面更精细地控制同时访问某个特定资源（如第三方API、本地数据库）的并发数量，可以结合 threading.Semaphore 使用。

```python
import concurrent.futures
import threading
import time

# 假设第三方接口限制每秒只能处理2个请求
api_semaphore = threading.Semaphore(2)

def call_external_api(url):
    with api_semaphore:  # 最多只允许2个线程同时进入这个代码块
        print(f"开始请求 {url}")
        time.sleep(1)  # 模拟网络请求耗时
        return f"{url} 请求完成"

urls = [f"api/data/{i}" for i in range(5)]

# 即使线程池开了5个线程，由于信号量的限制，同一时刻只会有2个请求在真正执行
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(call_external_api, urls))
```
