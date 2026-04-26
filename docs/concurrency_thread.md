# 线程 Process

python 中使用 `threading` 模块创建和管理子线程。

> 具体示例参考 [Python 并发编程-基于线程的并行](https://python-parallel-programmning-cookbook.readthedocs.io/zh-cn/latest/chapter2/index.html)

## 创建和执行

在 python 语言中使用 `threading` 创建子线程的方式有三种方法

1. 通过 `threading.Thread` 创建线程实例对象
2. 继承 `threading.Thread` 创建线程子类，并重写 `run` 方法。当实例化这个类并调用 `start()` 时，会自动执行 `run()` 方法中的逻辑。
3. 使用线程池创建线程，当需要创建大量子线程时，手动管理非常繁琐。threading 模块没有类似 multiprocessing 模块提供 Pool 类，需要使用 `concurrent.futures`，这个单开一章讲解。

线程创建完成后，启动线程通过调用实例对象的 `.start()` 方法，操作系统会正式分配资源并启动子线程。

另外，如果调用 `.join([timeout])` 方法会让主线程（或调用者）进入阻塞状态，等待所有子线程执行完毕再继续向下执行。如果不调用 `join()`，主程序可能会在子线程结束前退出，导致子线程被强制终止。

创建线程实例对象，示例代码。

```python
import threading

def function(i):
    print("function called by thread %i \n" % i)
    return


if __name__ == "__main__":
    threads = []

    for i in range(5):
        t = threading.Thread(target=function, args=(i,))
        threads.append(t)
        t.start()
        t.join()

```

创建线程子类，

1. 定义一个 Thread 类的子类
1. 重写 `__init__(self [,args])` 方法，可以添加额外的参数
1. 最后，需要重写 `run(self, [,args])` 方法来实现线程要做的事情

示例代码。

```python
import _thread
import threading
import time

exitFlag = 0

class myThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.delay, 5)
        print("Exiting " + self.name)

def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            _thread.exit()
        time.sleep(delay)
        print("%s : %s " % (thread_name, time.ctime(time.time())))
        counter -= 1

t1 = myThread(1, "Thread-1", 1)
t2 = myThread(2, "Thread-2", 2)

t1.start()
t2.start()
t1.join()
t2.join()
print("Exiting Main Thread")
```

创建线程池，示例代码。

```python
import concurrent.futures
import time

# 定义一个简单的任务函数
def task(n):
    print(f"Task {n} started")
    time.sleep(1)  # 模拟耗时操作
    print(f"Task {n} finished")
    return n * 2

# 创建一个线程池，指定最大线程数为 3
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # 提交任务到线程池
    futures = [executor.submit(task, i) for i in range(5)]

    # 获取任务的结果
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        print(f"Task result: {result}")
```

## 线程实例化参数

`Thread` 类的调用签名：

```python
Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None, context=None)

# group: 一般设置为 None ，这是为以后的一些特性预留的
# target: 当线程启动的时候要执行的程序（函数）
# name: 线程名称，默认会分配一个唯一名字 Thread-N
# args: 传递给 target 的参数，要使用tuple类型
# kwargs: 同上，使用字典类型dict
# daemon: 默认为 False，线程是否在后台执行。
```

代码示例

```python
import threading
import time

def first_func():
    print(threading.current_thread().name + " is starting")
    time.sleep(2)
    print (threading.current_thread().name + ' is Exiting ')
    return
def second_func():
    print(threading.current_thread().name + " is starting")
    time.sleep(2)
    print (threading.current_thread().name + ' is Exiting ')
    return

if __name__ == "__main__":
    t1 = threading.Thread(target=first_func, name="first_func")
    t2 = threading.Thread(target=second_func, name="second_func")
    t1.start()
    t2.start()
    t1.join()
    t2.join()
```

## 线程实例对象的方法

`Thread` 类对象提供了以下方法：

1. `t.start()` 启动线程
2. `t.join([timeout])` 等待线程结束
3. `t.is_alive()` 查看线程是否存活

```python
import _thread
import threading
import time

exitFlag = 0

class myThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.delay, 5)
        print("Exiting " + self.name)

def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            _thread.exit()
        time.sleep(delay)
        print("%s : %s " % (thread_name, time.ctime(time.time())))
        counter -= 1

t1 = myThread(1, "Thread-1", 1)
t2 = myThread(2, "Thread-2", 2)

t1.start()
t2.start()
t1.join()
t2.join()
print("Exiting Main Thread")
```

## 线程间交换数据

并行应用常常需要在线程之间交换数据。threading模块中使用 Queue 返回一个线程共享的队列，是线程安全的，也是线程安全的。任何可序列化的对象（Python通过 pickable 模块序列化对象）都可以通过它进行交换。

Queue 示例代码

```python
"""
Queue常用的方法有以下四个：

put(): 往queue中放一个item
get(): 从queue删除一个item，并返回删除的这个item
task_done(): 每次item被处理的时候需要调用这个方法
join(): 所有item都被处理之前一直阻塞
"""

from threading import Thread
from queue import Queue
import time
import random
class producer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) :
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print('Producer notify: item N° %d appended to queue by %s' % (item, self.name))
            time.sleep(1)

class consumer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            print('Consumer notify : %d popped from queue by %s' % (item, self.name))
            self.queue.task_done() # 关键方法，相当于释放锁

if __name__ == '__main__':
    queue = Queue()
    t1 = producer(queue)
    t2 = consumer(queue)
    t3 = consumer(queue)
    t4 = consumer(queue)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
```

生产者使用 `Queue.put(item [,block[, timeout]])` 来往queue中插入数据。Queue是同步的，在插入数据之前内部有一个内置的锁机制。所以可能发生两种情况：

- 如果 block 为 True ， timeout 为 None （这也是默认的选项，本例中使用默认选项），那么可能会阻塞掉，直到出现可用的位置。如果 timeout 是正整数，那么阻塞直到这个时间，就会抛出一个异常。
- 如果 block 为 False ，如果队列有闲置那么会立即插入，否则就立即抛出异常（ timeout 将会被忽略）。本例中， put() 检查队列是否已满，然后调用 wait() 开始等待。

消费者从队列中取出整数然后用 `task_done()` 方法将其标为任务已处理。消费者使用 `Queue.get([block[, timeout]])` 从队列中取回数据，queue内部也会经过锁的处理。如果队列为空，消费者阻塞。

## 线程间同步数据

当两个或以上对共享内存的操作发生在并发线程中，并且至少有一个可以改变数据，又没有同步机制的条件下，就会产生竞争条件，可能会导致执行无效代码、bug、或异常行为。

竞争条件最简单的解决方法是使用锁。锁的操作非常简单，当一个线程需要访问部分共享内存时，它必须先获得锁才能访问。此线程对这部分共享资源使用完成之后，该线程必须释放锁，然后其他线程就可以拿到这个锁并访问这部分资源了。很显然，避免竞争条件出现是非常重要的，所以我们要保证，在同一时刻只有一个线程允许访问共享内存。

共享数据协同的线程必须以适当的策略来读写数据，线程的同步原语如下：

- Lock: 这个对象可以有两种装填：锁住的（locked）和没锁住的（unlocked）。一个Lock对象有两个方法， `acquire()` 和 `release()` ，来控制共享数据的读写权限。
- Event: 实现了线程间的简单通讯，一个线程发事件的信号，另一个线程等待事件的信号。 Event 对象有两个方法， `set()` 和 `clear()` ，来管理自己内部的变量。
- Condition: 此对象用来同步部分工作流程，在并行的线程中，有两个基本的方法： `wait()` 用来等待线程，`notify_all()` 用来通知所有等待此条件的线程。
- Semaphore: 用来共享资源，例如，支持固定数量的共享连接。
- Rlock: 递归锁对象。
- Barrier: 将程序分成几个阶段，适用于有些线程必须在某些特定线程之后执行。处于障碍（Barrier）之后的代码不能同处于障碍之前的代码并行。

### Lock 进行线程同步

```python
import threading

shared_resource_with_lock = 0
shared_resource_without_lock = 0
COUNT = 100000
shared_resource_lock = threading.Lock()

# 有锁的情况
def increment_with_lock():
    global shared_resource_with_lock
    for i in range(COUNT):
        shared_resource_lock.acquire()
        shared_resource_with_lock += 1
        shared_resource_lock.release()

def decrement_with_lock():
    global shared_resource_with_lock
    for i in range(COUNT):
        shared_resource_lock.acquire()
        shared_resource_with_lock -= 1
        shared_resource_lock.release()

# 没有锁的情况
def increment_without_lock():
    global shared_resource_without_lock
    for i in range(COUNT):
        shared_resource_without_lock += 1

def decrement_without_lock():
    global shared_resource_without_lock
    for i in range(COUNT):
        shared_resource_without_lock -= 1


if __name__ == '__main__':
    t1 = threading.Thread(target=increment_with_lock)
    t2 = threading.Thread(target=decrement_with_lock)
    t3 = threading.Thread(target=increment_with_lock)
    t4 = threading.Thread(target=decrement_with_lock)

    tt1 = threading.Thread(target=increment_without_lock)
    tt2 = threading.Thread(target=decrement_without_lock)
    tt3 = threading.Thread(target=increment_without_lock)
    tt4 = threading.Thread(target=decrement_without_lock)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    tt1.start()
    tt2.start()
    tt3.start()
    tt4.start()
    tt1.join()
    tt2.join()
    tt3.join()
    tt4.join()

    print ("the value of shared variable with lock management is %s" % shared_resource_with_lock)
    print ("the value of shared variable with race condition is %s" % shared_resource_without_lock)
```

### RLock 进行线程同步

RLock其实叫做“Reentrant Lock”，就是可以重复进入的锁，也叫做“递归锁”。

这种锁对比Lock有是三个特点：

1. 谁拿到谁释放。如果线程A拿到锁，线程B无法释放这个锁，只有A可以释放；
2. 同一线程可以多次拿到该锁，即可以acquire多次；
3. acquire多少次就必须release多少次，只有最后一次release才能改变RLock的状态为unlocked

```python
import threading
import time

class Box(object):
    lock = threading.RLock()

    def __init__(self):
        self.total_items = 0

    def execute(self, n):
        Box.lock.acquire()
        self.total_items += n
        Box.lock.release()

    def add(self):
        Box.lock.acquire()
        self.execute(1)
        Box.lock.release()

    def remove(self):
        Box.lock.acquire()
        self.execute(-1)
        Box.lock.release()

## These two functions run n in separate
## threads and call the Box's methods
def adder(box, items):
    while items > 0:
        print("adding 1 item in the box")
        box.add()
        time.sleep(1)
        items -= 1

def remover(box, items):
    while items > 0:
        print("removing 1 item in the box")
        box.remove()
        time.sleep(1)
        items -= 1

## the main program build some
## threads and make sure it works
if __name__ == "__main__":
    items = 5
    print("putting %s items in the box " % items)
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, items))
    t2 = threading.Thread(target=remover, args=(box, items))
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("%s items still remain in the box " % box.total_items)
```

### Semaphore 进行线程同步

信号量由E.Dijkstra发明并第一次应用在操作系统中，信号量是由操作系统管理的一种抽象数据类型，用于在多线程中同步对共享资源的使用。

- 每当线程想要读取关联了信号量的共享资源时，必须调用 acquire() ，此操作减少信号量的内部变量, 如果此变量的值非负，那么分配该资源的权限。如果是负值，那么线程被挂起，直到有其他的线程释放资源。
- 当线程不再需要该共享资源，必须通过 release() 释放。这样，信号量的内部变量增加，在信号量等待队列中排在最前面的线程会拿到共享资源的权限。

```python
# -*- coding: utf-8 -*-

"""Using a Semaphore to synchronize threads"""
import threading
import time
import random

# The optional argument gives the initial value for the internal
# counter;
# it defaults to 1.
# If the value given is less than 0, ValueError is raised.
semaphore = threading.Semaphore(0)

def consumer():
        print("consumer is waiting.")
        # Acquire a semaphore
        semaphore.acquire()
        # The consumer have access to the shared resource
        print("Consumer notify : consumed item number %s " % item)

def producer():
        global item
        time.sleep(10)
        # create a random item
        item = random.randint(0, 1000)
        print("producer notify : produced item number %s" % item)
         # Release a semaphore, incrementing the internal counter by one.
        # When it is zero on entry and another thread is waiting for it
        # to become larger than zero again, wake up that thread.
        semaphore.release()

if __name__ == '__main__':
        for i in range (0,5) :
                t1 = threading.Thread(target=producer)
                t2 = threading.Thread(target=consumer)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
        print("program terminated")
```

### Condition 进行线程同步

条件指的是应用程序状态的改变。这是另一种同步机制，其中某些线程在等待某一条件发生，其他的线程会在该条件发生的时候进行通知。一旦条件发生，线程会拿到共享资源的唯一权限。

释条件机制最好的例子还是生产者-消费者问题。在本例中，只要缓存不满，生产者一直向缓存生产；只要缓存不空，消费者一直从缓存取出（之后销毁）。当缓冲队列不为空的时候，生产者将通知消费者；当缓冲队列不满的时候，消费者将通知生产者。

```python
from threading import Thread, Condition
import time

items = []
condition = Condition()

class consumer(Thread):

    def __init__(self):
        Thread.__init__(self)

    def consume(self):
        global condition
        global items
        condition.acquire()
        if len(items) == 0:
            condition.wait()
            print("Consumer notify : no item to consume")
        items.pop()
        print("Consumer notify : consumed 1 item")
        print("Consumer notify : items to consume are " + str(len(items)))

        condition.notify()
        condition.release()

    def run(self):
        for i in range(0, 20):
            time.sleep(2)
            self.consume()

class producer(Thread):

    def __init__(self):
        Thread.__init__(self)

    def produce(self):
        global condition
        global items
        condition.acquire()
        if len(items) == 10:
            condition.wait()
            print("Producer notify : items producted are " + str(len(items)))
            print("Producer notify : stop the production!!")
        items.append(1)
        print("Producer notify : total items producted " + str(len(items)))
        condition.notify()
        condition.release()

    def run(self):
        for i in range(0, 20):
            time.sleep(1)
            self.produce()

if __name__ == "__main__":
    producer = producer()
    consumer = consumer()
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
```

### Event 进行线程同步

事件是线程之间用于通讯的对象。有的线程等待信号，有的线程发出信号。基本上事件对象都会维护一个内部变量，可以通过 set() 方法设置为 true ，也可以通过 clear() 方法设置为 false 。 wait() 方法将会阻塞线程，直到内部变量为 true 。

```python
import time
from threading import Thread, Event
import random
items = []
event = Event()

class consumer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        while True:
            time.sleep(2)
            self.event.wait()
            item = self.items.pop()
            print('Consumer notify : %d popped from list by %s' % (item, self.name))

class producer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        global item
        for i in range(100):
            time.sleep(2)
            item = random.randint(0, 256)
            self.items.append(item)
            print('Producer notify : item N° %d appended to list by %s' % (item, self.name))
            print('Producer notify : event set by %s' % self.name)
            self.event.set()
            print('Produce notify : event cleared by %s '% self.name)
            self.event.clear()

if __name__ == '__main__':
    t1 = producer(items, event)
    t2 = consumer(items, event)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
```

## with 语句

Python从2.5版本开始引入了 with 语法。此语法非常实用，在有两个相关的操作需要在一部分代码块前后分别执行的时候，可以使用 with 语法自动完成。同事，使用 with 语法可以在特定的地方分配和释放资源，因此， with 语法也叫做“上下文管理器”。在threading模块中，所有带有 acquire() 方法和 release() 方法的对象都可以使用上下文管理器。

```python
import threading
import logging
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

def threading_with(statement):
    with statement:
        logging.debug('%s acquired via with' % statement)

def threading_not_with(statement):
    statement.acquire()
    try:
        logging.debug('%s acquired directly' % statement )
    finally:
        statement.release()

if __name__ == '__main__':
    # let's create a test battery
    lock = threading.Lock()
    rlock = threading.RLock()
    condition = threading.Condition()
    mutex = threading.Semaphore(1)
    threading_synchronization_list = [lock, rlock, condition, mutex]
    # in the for cycle we call the threading_with e threading_no_with function
    for statement in threading_synchronization_list :
       t1 = threading.Thread(target=threading_with, args=(statement,))
       t2 = threading.Thread(target=threading_not_with, args=(statement,))
       t1.start()
       t2.start()
       t1.join()
       t2.join()
```
