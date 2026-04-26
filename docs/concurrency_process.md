# 进程 Process

python 中使用 `multiprocessing` 模块创建和管理子进程。

> 具体示例参考 [Python 并发编程-基于进程的并行](https://python-parallel-programmning-cookbook.readthedocs.io/zh-cn/latest/chapter3/index.html)

## 创建和执行

在 python 语言中使用 `multiprocessing` 创建子进程的方式有三种方法

1. 通过 `multiprocessing.Process` 创建进程实例对象
2. 继承 `multiprocessing.Process` 创建进程子类，并重写 `run` 方法。当实例化这个类并调用 `start()` 时，会自动执行 `run()` 方法中的逻辑。
3. 使用进程池创建进程，当需要创建大量子进程时，手动管理非常繁琐。Pool 可以创建一个进程池，限制同时运行的进程数量，自动调度任务。

进程创建完成后，启动进程通过调用实例对象的 `.start()` 方法，操作系统会正式分配资源并启动子进程。

另外，如果调用 `.join([timeout])` 方法会让主进程（或调用者）进入阻塞状态，等待所有子进程执行完毕再继续向下执行。如果不调用 `join()`，主程序可能会在子进程结束前退出，导致子进程被强制终止。

创建进程实例对象，示例代码。

```python
import multiprocessing
import time

def worker(args):
    name = multiprocessing.current_process().name
    print(f"子进程 {name} 正在运行，参数 {args}")
    time.sleep(1)

if __name__ == '__main__':
    p = multiprocessing.Process(target=worker, args=("A",))
    p.start()  # 启动子进程
    p.join()   # 等待子进程结束
    print("主进程结束")
```

创建进程子类，示例代码。

```python
from multiprocessing import Process

class MyProcess(Process):
    def run(self):
        print("called run method in MyProcess: %s" % self.name)

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = MyProcess()
        jobs.append(p)
        p.start()
        p.join()
```

创建进程池，示例代码。

```python
import multiprocessing as mp

def function_square(data):
    result = data * data
    return result

if __name__ == '__main__':
    inputs = list(range(100))
    pool = mp.Pool(processes=4)
    pool_outputs = pool.map(function_square, inputs)
    pool.close()
    pool.join()
    print("Pool   : ", pool_outputs)
```

## 进程实例化参数

`Process` 类的调用签名：

```python
Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)

# group: 一般设置为 None ，这是为以后的一些特性预留的
# target: 当进程启动的时候要执行的程序（函数）
# name: 进程名称，默认会分配一个唯一名字 Process-N
# args: 传递给 target 的参数，要使用tuple类型
# kwargs: 同上，使用字典类型dict
# daemon: 默认为 False，进程是否在后台执行，此时的进程并不是Unix的守护进程或服务（daemons or services），所以当主进程退出，它们也会自动结束。
# 另外强调 daemon=True 的进程不允许创建子进程。否则，当后台进程跟随父进程退出的时候，新建的子进程会变成孤儿进程。
```

代码示例

```python
import multiprocessing as mp
import time

def foo():
    name = mp.current_process().name
    print("Starting %s \n" % name)
    time.sleep(3)
    print("Exiting %s \n" % name)

if __name__ == "__main__":
    background_process = mp.Process(name="background_process", target=foo)
    # 通过将 daemon = True，使该子进程在后台运行，所以控制台不会有输出
    background_process.daemon = True
    no_background_process = mp.Process(name= "NO_background_process" , target=foo)
    no_background_process.daemon = False
    background_process.start()
    no_background_process.start()
```

## 进程实例对象的方法

`Process` 类对象提供了以下方法：

1. `p.start()` 启动进程
2. `p.join([timeout])` 等待进程结束
3. `p.terminate()` 杀死进程
4. `p.is_alive()` 查看进程是否存活
5. `p.close()` 关闭进程
6. `p.exitcode` 进程退出码

```python
import multiprocessing as mp
import time

def foo():
    print("Starting foo")
    time.sleep(1)
    print("Exiting foo")

if __name__ == "__main__":
    p = mp.Process(target=foo)
    print("Process before execution", p, p.is_alive())
    p.start()
    print("Process running: ", p, p.is_alive())
    p.terminate()
    print("Process terminated: ", p, p.is_alive())
    p.join()
    print("Process joined: ", p, p.is_alive())
    print("Process exiting: ", p.exitcode)
    # 通过读进程的 ExitCode 状态码（status code）验证进程已经结束， ExitCode 可能的值如下：
    # == 0: 没有错误正常退出
    # > 0: 进程有错误，并以此状态码退出
    # < 0: 进程被 -1 * 的信号杀死并以此作为 ExitCode 退出
    # 在我们的例子中，输出的 ExitCode 是 -15 。负数表示子进程被数字为15的信号杀死。
```

## 进程间交换数据

并行应用常常需要在进程之间交换数据。Multiprocessing 库有两个沟通渠道（Communication Channel）可以交换对象：队列(queue)和管道（pipe）。

- Queue 返回一个进程共享的队列，是线程安全的，也是进程安全的。任何可序列化的对象（Python通过 pickable 模块序列化对象）都可以通过它进行交换。
- Pipe 返回一个进程间通信的管道，调用后返回一对被管道连接的连接对象，连接对象有 send / receive 方法可以在进程之间通信

Queue 示例代码

```python
import multiprocessing as mp
import random
import time

class Producer(mp.Process):
    def __init__(self, queue):
        mp.Process.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print("Process Producer: item %d appended to queue %s" % (item, self.name))
            time.sleep(1)
            print("The size of queue is %s" % self.queue.qsize())

class Consumer(mp.Process):
    def __init__(self, queue):
        mp.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                print("The queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                print("Process Consumer: item %d popped from by %s \n" % (item, self.name))
                time.sleep(1)

if __name__ == "__main__":
    queue = mp.Queue()
    process_producer = Producer(queue)
    process_consumer = Consumer(queue)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
```

Pipe 示例代码

```python
import multiprocessing as mp

def create_items(pipe):
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    output_pipe.close()

def multiply_items(pipe_1, pipe_2):
    close, input_pipe = pipe_1
    close.close()
    output_pipe, _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()
            output_pipe.send(item * item)
    except EOFError:
        output_pipe.close()

if __name__ == '__main__':
    # 第一进程管道发出数据
    pipe_1 = mp.Pipe(True)
    process_pipe_1 = mp.Process(target=create_items, args=(pipe_1,))
    process_pipe_1.start()
    # 第二个进程管道接收数据并计算
    pipe_2 = mp.Pipe(True)
    process_pipe_2 = mp.Process(target=multiply_items, args=(pipe_1,pipe_2,))
    process_pipe_2.start()
    pipe_1[0].close()
    pipe_2[0].close()
    try:
        while True:
            print(pipe_2[1].recv())
    except EOFError:
        print("End of program")
```

## 进程间同步数据

多个进程可以协同工作来完成一项任务。通常需要共享数据。所以在多进程之间保持数据的一致性就很重要了。需要共享数据协同的进程必须以适当的策略来读写数据。相关的同步原语和线程的库很类似。

进程的同步原语如下：

- Lock: 这个对象可以有两种状态：锁住的（locked）和没锁住的（unlocked）。一个Lock对象有两个方法， acquire() 和 release() ，来控制共享数据的读写权限。
- Event: 实现了进程间的简单通讯，一个进程发事件的信号，另一个进程等待事件的信号。 Event 对象有两个方法， set() 和 clear() ，来管理自己内部的变量。
- Condition: 此对象用来同步部分工作流程，在并行的进程中，有两个基本的方法： wait() 用来等待进程， notify_all() 用来通知所有等待此条件的进程。
- Semaphore: 用来共享资源，例如，支持固定数量的共享连接。
- Rlock: 递归锁对象。其用途和方法同 Threading 模块一样。
- Barrier: 将程序分成几个阶段，适用于有些进程必须在某些特定进程之后执行。处于障碍（Barrier）之后的代码不能同处于障碍之前的代码并行。

下面的代码展示了如何使用 barrier() 函数来同步两个进程。我们有4个进程，进程1和进程2由barrier语句管理，进程3和进程4没有同步策略。

```python
import multiprocessing as mp
from multiprocessing import Process, Barrier, Lock
from time import time
from datetime import datetime

def test_with_barrier(synchronizer, serializer):
    name = mp.current_process().name
    synchronizer.wait()
    now = time()
    with serializer:
        print("process %s ----> %s" % (name, datetime.fromtimestamp(now)))

def test_without_barrier():
    name = mp.current_process().name
    now = time()
    print("process %s ----> %s" % (name, datetime.fromtimestamp(now)))

if __name__ == '__main__':
    synchronizer = Barrier(2)
    serializer = Lock()
    Process(name='p1 - test_with_barrier', target=test_with_barrier, args=(synchronizer,serializer)).start()
    Process(name='p2 - test_with_barrier', target=test_with_barrier, args=(synchronizer,serializer)).start()
    Process(name='p3 - test_without_barrier', target=test_without_barrier).start()
    Process(name='p4 - test_without_barrier', target=test_without_barrier).start()
```

## 进程间管理数据状态

Python的多进程模块提供了在所有的进程间管理共享数据的管理者(Manager)。一个管理者对象控制着持有共享对象的服务进程，并允许其它进程操作共享对象。

管理者有以下特性：

- 它控制着管理共享对象的服务进程
- 它确保当某一进程修改了共享对象之后，所有的进程拿到额共享对象都得到了更新

```python
import multiprocessing as mp

def worker(dictionary, key, item):
    dictionary[key] = item
    print("key = %d, value = %s" % (key, item))

if __name__ == '__main__':
    mgr = mp.Manager()
    # 共享字典
    dictionary = mgr.dict()

    jobs = [mp.Process(target=worker, args=(dictionary, i, i*2)) for i in range(10)]

    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print("Result: ",dictionary)
```
