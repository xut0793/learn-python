# asyncio

asyncio 是 Python 3.4 引入的一个标准库，它通过在单进程单线程中，结合协程的方式实现并发。

asyncio 模块提供了四个主要组件：

- EventLoop：事件循环
- Task：任务
- Coroutine：协程
- Future：异步操作结果

## EventLoop

事件循环是 asyncio 的中央处理器和调度中心。它在一个单线程中永不停止地运行，通过操作系统的底层机制（如 Linux 的 epoll 或 Windows 的 select）来同时监控成百上千个网络连接和 I/O 资源。它的作用是管理所有的任务，在整个程序运行过程中不断循环执行，追踪任务发生的顺序将它们放到队列中，当主线程空闲的时候，调用相应的任务处理器，将结果返回给调用方。

不同语言对事件循环的实现和使用方式不同，比如 JavaScript 语言的运行时（浏览器和Nodejs）内部就实现了事件循环，在应用层不需要显式处理，但是 Python 语言通过标准库实现事件循环，并且要求在应用代码显式调用。

它的核心工作流程是一个“运行-暂停-切换-恢复”的循环：

1. 管理任务：维护一个“待办事项”列表（就绪队列）。
2. 监控 I/O：不断询问操作系统：“这些连接里，有哪个可以读数据了吗？有哪个可以写数据了吗？”
3. 调度执行：从队列中取出一个任务运行。当任务遇到 await（通常是 I/O 操作）时，会主动暂停并交出控制权，告诉事件循环：“等这个 I/O 准备好了再叫我”。事件循环随即去处理其他任务，等 I/O 就绪后，再把暂停的任务放回队列等待恢复。

```python
# 伪代码来理解事件循环
while True:
    events = getEvents();
    for e in events
        processEvent(e);
```

asyncio 中关于事件循环相关的 api 如下：

- 获取与创建事件循环：这些方法主要用于拿到事件循环的实例对象（遥控器）
  - `asyncio.get_running_loop()`：获取当前线程中正在运行的事件循环。如果你在协程内部需要访问事件循环，首选这个方法。
  - `asyncio.new_event_loop()`：手动创建一个全新的事件循环对象。通常在需要自定义或多线程管理事件循环时使用。
  - `asyncio.get_event_loop()`：获取当前的事件循环。如果当前没有，它会尝试创建一个。（注：在 Python 3.14+ 中，如果没有正在运行的循环，它会直接报错，官方更推荐使用 `get_running_loop()`）。
  - `asyncio.set_event_loop(loop)`：复用事件循环，将指定的事件循环对象设置为当前线程的当前事件循环。
- 运行与控制生命周期：这些方法决定了事件循环什么时候开始跑、什么时候停下来。
  - `loop.run_until_complete(future)`：运行事件循环，直到传入的 future（或协程）执行完毕并返回结果。这是最经典的运行方式。
  - `loop.run_forever()`：让事件循环一直运行下去，直到被手动调用 `stop()` 停止。常用于需要长期驻留的后台服务。
  - `loop.stop()`：发出停止事件循环的指令。
  - `loop.close()`：关闭事件循环，清理资源。关闭后的循环不能再被使用。
  - `loop.is_running()` / `loop.is_closed()`：分别用来检查事件循环当前是否正在运行，以及是否已经被关闭。
- 调度任务与回调（Callback）：这些方法用于向事件循环“派发活儿”，告诉它什么时候该执行什么函数。
  - `loop.create_task(coro)`：将一个协程包装成 Task 对象并提交到事件循环中准备执行。这是并发执行多个协程的基础。
  - `loop.call_soon(callback, *args)`：尽快（在事件循环的下一次迭代中）调用一个普通的回调函数。
  - `loop.call_later(delay, callback, *args)`：延迟指定的秒数（delay）后，再调用回调函数。
  - `loop.call_at(when, callback, *args)`：在指定的绝对时间点（when，通常通过 loop.time() 获取）调用回调函数。
  - `loop.call_soon_threadsafe(callback, *args)`：call_soon 的线程安全版本。当你需要从其他普通线程向事件循环所在的线程提交任务时，必须使用它。
- 网络 I/O 与底层交互：这些是事件循环最强大的底层能力，用于处理真实的网络连接和文件。
  - `loop.create_connection()` / `loop.create_server()`：分别用于创建 TCP 客户端连接和搭建 TCP 服务器。
  - `loop.create_datagram_endpoint()`：用于处理 UDP 协议的网络通信。
  - `loop.run_in_executor(executor, func, *args)`：极其重要。它可以将一个耗时的同步阻塞函数（如传统的文件读写或 CPU 密集型计算）放到线程池或进程池中运行，从而避免阻塞住整个事件循环。
  - `loop.add_reader(fd, callback, *args)` / `loop.remove_reader(fd)`：直接监听文件描述符（fd）的可读状态，常用于底层的网络库开发。

asyncio 生命周期代码示例

```python
import asyncio

async def main():
    print("手动挡，需要自己掌控一切！")

# 1. 手动创建循环
loop = asyncio.new_event_loop()
try:
    # 2. 手动设置为当前线程的循环（在某些场景下需要）
    asyncio.set_event_loop(loop)
    # 3. 手动运行协程
    loop.run_until_complete(main())
finally:
    # 4. 手动关闭循环，防止资源泄露
    loop.close()
```

上述直接操作 `event_loop` 的方式都是偏底层的函数，创建事件循环对象后，需要手动调用 `loop.run_until_complete()` 来跑任务，手动管理生命周期，你可以创建后让它一直运行（比如调用 `loop.run_forever()`），也可以在不同的时间段多次复用同一个循环对象`asyncio.set_event_loop(loop)` 。最后必须记得调用 `loop.close()` 来释放资源。

这样适用于需要深度定制的高级场景，或者精细控制事件循环启停时。例如，在多线程编程中，你需要在非主线程里手动创建一个独立的事件循环；或者你需要实现一个长期驻留、不能随便关闭的后台服务。在 99% 的日常业务开发中，上述过程只需要调用 `asyncio.run(main())` 即可。

`asyncio.run(coro)`：这是 Python 官方推荐的异步程序唯一入口。它是一个高层级的封装函数，设计目标是“开箱即用、用完即弃”。它会自动帮你完成一整套流程：创建一个新的事件循环、将其设置为当前线程的默认循环、运行传入的协程、在协程结束后自动关闭循环并清理资源。

`asyncio.run()` 和 `asyncio.new_event_loop()` 的核心区别在于：前者是开箱即用的“全自动驾驶”，而后者是需要手动操作底层细节的“手动挡”。

```python
import asyncio

async def main():
    print("全自动运行，省心！")

# 一行代码搞定创建、运行和销毁
asyncio.run(main())
```

## Future

Future 是也是一个底层的对象，代表一个“尚未完成但未来会有结果”的异步操作结果。事件循环可以通过监视一个future对象的状态来指示它已经完成。future对象有几个状态：

- Pending
- Running
- Done
- Cancelled

刚创建的 future 为pending，事件循环调用执行的时候当然就是running，调用完毕自然就是done，如果需要停止事件循环，就需要先把 future 取消，状态为cancel。

future 的核心作用是连接底层的回调代码和高层的 async/await 语法。

Future 对象的 API ：

- 设置结果与异常（填充容器）：这些方法通常由生产异步结果的代码（数据生产者）调用，用来把最终的值放进 Future 里。
  - `future.set_result(result)`: 将 Future 标记为“已完成”，并设置其结果。一旦调用，Future 的状态就会从 Pending 变为 Done。类似JavaScript中 Promise 的 resolve方法。
  - `future.set_exception(exception)`: 将 Future 标记为“已完成”，并设置一个异常。这表示异步操作失败了。类似JavaScript中 Promise 的 reject方法。
  - 注意：`set_result` 和 `set_exception` 对同一个 Future 只能调用一次，重复调用会抛出 InvalidStateError。
- 获取结果与状态（提取与检查）：这些方法由消费结果的协程调用（数据消费者），用来检查进度或拿走最终的值。
  - `future.done()`: 返回一个布尔值，表示 future 是否已经完成。如果 Future 已经被取消，或者已经通过 set_result / set_exception 设置了结果/异常，都会返回 True。
  - `future.cancel()`: 取消 future，返回一个布尔值，表示是否成功取消。
  - `future.exception()`: 返回 Future 内部设置的异常对象。如果操作正常结束没有报错，则返回 None。
  - `future.result()`: 返回 future 的最终结果。
    - 如果结果已设置，返回该值；
    - 如果设置了异常，调用此方法会重新引发该异常；
    - 如果任务被取消，会引发 CancelledError；
    - 如果 Future 还没完成就调用，会引发 InvalidStateError。
- 生命周期控制与回调
  - `future.add_done_callback(callback)`: 为 Future 添加一个回调函数。当 Future 完成（无论是成功、失败还是被取消）时，事件循环会自动调用这个回调，并将 Future 对象本身作为参数传给它。
  - `future.remove_done_callback(callback)`: 删除一个回调函数。

```python
import asyncio

# 负责“生产”结果的协程
async def producer(future: asyncio.Future):
    print("生产者: 开始执行耗时操作...")
    await asyncio.sleep(2)  # 模拟耗时的 I/O 操作

    # 操作完成，将结果填入 Future 容器
    future.set_result("生产者产出的数据")
    print("生产者: 结果已填入 Future")

# 负责“消费”结果的协程
async def consumer(future: asyncio.Future):
    print("消费者: 正在等待 Future 的结果...")

    # 使用 await 等待 Future 被填入结果（期间会暂停并交出控制权）
    result = await future
    print(f"消费者: 拿到结果了！-> {result}")

async def main():
    # 1. 手动创建一个空的 Future 对象（初始状态为 Pending）
    my_future = asyncio.Future()
    print(f"Future 初始状态: done={my_future.done()}, cancelled={my_future.cancelled()}")

    # 2. 并发运行生产者和消费者
    # 消费者会在这里等待，直到生产者调用 set_result
    await asyncio.gather(
        producer(my_future),
        consumer(my_future)
    )

    # 3. 再次检查状态
    print(f"Future 最终状态: done={my_future.done()}")

if __name__ == "__main__":
    asyncio.run(main())
```

同 `event_loop` 一样，日常开发极少手动创建 `asyncio.Future()`，在大多数业务代码中，调用 `asyncio.create_task(coro)` 返回的 Task 对象本身就是 Future 的子类，它已经自动帮你处理了协程执行完毕后的 `set_result` 或 `set_exception` 逻辑。

特别需要注意一点，如果你手动创建了 Future，一定要确保在代码的某个分支里调用了 `set_result` 或 `set_exception`。如果忘了，任何 await 这个 Future 的协程都会无限期地卡死等待下去。这跟 JavaScript 中的 `new Promise` 中要记得调用 `resolve` 或 `reject` 方法类似。

## Task

`Task` 是事件循环里驱动协程运行的核心对象。作为 Future 的子类，它不仅负责调度协程的执行，还提供了丰富的方法来获取结果、监控状态以及控制任务的生命周期。

协程对象本身无法直接在事件循环中运行，必须被包装成 Task 对象。当我们调用 `asyncio.run(coro)` 或 `asyncio.create_task(coro)` 时，就是把协程包装成了一个 Task 并提交给事件循环调度。

- 任务创建与调度
  - `asyncio.create_task(coro)`：这是创建 Task 最常用、最推荐的方法。它会将传入的协程对象包装成一个 Task，并立即将其提交给当前的事件循环进行调度。
- 任务执行结果获取与状态监控
  - `task.done()`：返回一个布尔值。如果 Task 已经执行完成（无论是正常返回、抛出异常还是被取消），都会返回 True。
  - `task.result()`：返回 Task 的最终结果。如果协程正常返回，则返回该值；如果协程内部引发了异常，调用此方法会重新引发该异常；如果任务被取消，会引发 CancelledError。如果任务尚未完成就调用，会引发 InvalidStateError。
  - `task.exception()`：返回 Task 内部引发的异常。如果协程正常结束，返回 None；如果任务被取消，会引发 CancelledError。同样，如果任务未完成就调用，会引发 InvalidStateError。
  - `task.get_coro()`：返回被 Task 包装的原始协程对象。
- 任务取消（生命周期控制）：任务取消是一种“请求式”的协作机制，而不是强制中断：
  - `task.cancel(msg=None)`：向任务发出取消请求。这会在事件循环的下一轮调度中，向被包装的协程内部抛出一个 asyncio.CancelledError 异常。
  - `task.uncancel()`：递减任务的取消请求计数。这在某些复杂的取消逻辑中非常有用。
  - `task.cancelling()`：返回当前对该任务挂起的取消请求次数（即调用 `cancel()` 减去 `uncancel()` 的次数）。
  - `task.cancelled()`：如果任务已经被成功取消，返回 True。
- 回调与调试
- `task.add_done_callback(callback)`：为任务添加一个回调函数。当任务完成时（无论成功、失败或被取消），事件循环会自动调用这个回调函数。这在低层级的异步框架开发中非常常用。
- `task.get_name()` / `task.set_name(value)`：获取或设置任务的名称，方便在日志和调试时识别具体的任务。
- `task.print_stack()` / `task.get_stack()`：打印或获取当前任务的调用栈信息。当协程因为 I/O 阻塞而暂停时，这些方法能帮你定位代码具体挂起在哪个位置。

```python
import asyncio

# 模拟一个长时间运行的异步任务
async def long_running_task(name):
    print(f"任务 {name}: 开始执行...")
    try:
        # 模拟耗时 I/O 操作
        await asyncio.sleep(5)
        print(f"任务 {name}: 执行完毕！")
        return f"{name} 的成功结果"
    except asyncio.CancelledError:
        # 捕获取消请求，进行必要的清理工作
        print(f"任务 {name}: 收到了取消请求，正在清理资源...")
        raise  # 必须重新抛出 CancelledError，否则任务状态不会变为已取消

async def main():
    # 1. 创建并调度任务
    task = asyncio.create_task(long_running_task("A"))

    # 2. 监控任务状态
    print(f"任务刚创建时是否完成: {task.done()}")  # 输出: False
    print(f"任务名称: {task.get_name()}")          # 输出: Task-A (默认名称)

    # 等待 2 秒后尝试取消任务
    await asyncio.sleep(2)

    if not task.done():
        print("主程序决定取消该任务...")
        task.cancel()  # 发出取消请求

    # 3. 等待任务结束并获取结果/异常
    try:
        result = await task
        print(f"任务最终结果: {result}")
    except asyncio.CancelledError:
        print(f"主程序: 任务 {task.get_name()} 已被成功取消")
        print(f"任务最终状态 (done): {task.done()}")      # 输出: True
        print(f"任务最终状态 (cancelled): {task.cancelled()}") # 输出: True

if __name__ == "__main__":
    asyncio.run(main())
```

Task 作为看作是协程函数和 Future 之间的桥梁，当协程执行结束时，Task 会调用 Future 的 set_result 方法将结果存入。我们在代码中写 `result = await future` 或 `result = await task`，本质上就是在等待这个占位符被填入最终的结果。

## asyncio

asyncio 模块自身提供了许多高层级的全局函数，它们就像是为开发者准备的便捷工具箱，让我们无需直接操作底层的事件循环对象 event_loop、Future、Task，就能轻松驾驭异步编程。日常开发中，绝大多数都是直接调用这些全局函数即可完成异步任务。

- 启动与管理事件循环
  - `asyncio.run(coro, *, debug=None)`：这是 Python 异步程序的绝对入口。它的作用是创建一个新的事件循环，运行传入的顶层协程（coro），并在协程完成后自动关闭事件循环。在一个程序中，`asyncio.run()` 通常只会在最外层被调用一次。
- 创建任务与可等待对象
  - `asyncio.create_task(coro)`：将协程包装成一个 Task 对象，并立即提交给当前的事件循环调度执行。这是在日常开发中启动后台并发任务最常用的方法。
  - `asyncio.ensure_future(obj)`：这是一个更底层的函数。如果传入的是协程，它会自动调用 create_task；如果传入的已经是 Future 或 Task，则直接原样返回。通常用于框架内部或不确定传入对象类型时。
- 并发执行任务与任务聚合
  - `asyncio.gather(*aws, return_exceptions=False)`：并发执行多个可等待对象（如协程、任务），并按传入顺序收集所有结果。非常适合需要同时发起多个独立任务（如批量网络请求）并统一拿结果的场景。如果设置 `return_exceptions=True`，即使某个任务报错，也不会中断整体，而是将异常作为结果返回。
  - `asyncio.wait(aws, *, timeout=None, return_when=ALL_COMPLETED)`：比 gather 更灵活。它返回两个集合：已完成的任务（done）和未完成的任务（pending）。你可以通过 return_when 参数控制何时返回，例如 `FIRST_COMPLETED`（任意一个任务完成就返回）或 `FIRST_EXCEPTION`（任意一个任务抛出异常就返回）。
  - `asyncio.as_completed(aws, *, timeout=None)`：返回一个迭代器，按任务实际完成的先后顺序依次产出结果。如果你希望哪个任务先跑完就先处理哪个，用这个最合适。
- 时间与休眠控制
  - `asyncio.sleep(delay, result=None)`：异步版的“睡一会儿”。它会阻塞当前协程 delay 秒，但不会阻塞整个事件循环，期间其他协程可以正常运行。常用于模拟耗时的 I/O 操作或简单的延时。
  - `asyncio.wait_for(aw, timeout)`：为某个可等待对象设置超时时间。如果 aw 在 timeout 秒内没有完成，会抛出 `asyncio.TimeoutError` 异常，非常适合给网络请求等不确定的操作加上时间保险。
  - `asyncio.timeout(delay)`：Python 3.11 引入的上下文管理器（`async with asyncio.timeout(5)`），比 `wait_for` 的写法更优雅，同样用于限制代码块的执行时间。
- 并发数量限制（流控）
  - `asyncio.Semaphore(value)`：信号量，用于限制同时并发执行的任务数量。比如在写爬虫时，为了防止把对方服务器打挂或被封 IP，可以用它限制同时只能有 10 个请求在跑。
- 线程安全与底层交互
  `asyncio.to_thread(func, /, *args, **kwargs)`：Python 3.9+ 引入的神器。它可以在一个独立的线程池中异步地运行普通的同步函数（如传统的文件读写、耗时的 CPU 计算），完美解决同步代码阻塞事件循环的问题。
  `asyncio.get_running_loop()`：在协程内部获取当前正在运行的事件循环对象。如果你需要在协程里调用事件循环的底层方法（比如添加定时器），就用它。

## Coroutine

协程是异步编程的基本执行单元。通过`async def` 定义的函数就是协程函数，有时也可以简称协程。

通过 `async def` 定义一个协程。但是要注意，直接调用协程函数（如 `coro = my_coroutine()`）并不会立即执行，而是返回一个协程对象。

在协程函数内部，使用 `await` 表示协程向事件循环发出的“暂停并让出控制权”的信号。这是一种合作式多任务（Cooperative Multitasking），任务必须主动放弃 CPU，其他任务才有机会运行。`await` 后面通常跟着另一个协程或异步操作（如 asyncio.sleep() 或网络请求）。

### 启动一个协程

协程函数本身并不会启动协程，而是返回一个协程对象。要启动协程，通常有两种方式：

- `asyncio.run(coro, *, debug=None)`：这是 Python 异步程序的绝对入口。它的作用是创建一个新的事件循环，运行传入的顶层协程（coro），并在协程完成后自动关闭事件循环。在一个程序中，`asyncio.run()` 通常只会在最外层被调用一次。
- `asyncio.create_task(coro)`：将协程包装成一个 Task 对象，并立即提交给当前的事件循环调度执行。这是在日常开发中启动后台并发任务最常用的方法。

```python
import asyncio

async def my_coroutine():
    print("开始执行协程")
    await asyncio.sleep(1)  # 模拟非阻塞的 I/O 等待
    print("协程执行完毕")
    return "成功"

# 异步协程的入口函数，只会调用一次
async def main():
    task = asyncio.create_task(my_coroutine())
    print("任务已创建")
    result = await task
    print(f"任务结果：{result}")

# 启动事件循环的标准方式（Python 3.7+ 推荐）
asyncio.run(main())
```

### 从协程中获取返回值

协程函数直接调用并不会返回值，而是返回一个生成器对象。需要通过 `await` 获取协程的返回值。

```python
import asyncio

async def get_user_info(user_id):
    await asyncio.sleep(1)
    return f"用户 {user_id} 的详细信息"

async def main():
    # 使用 await 等待协程执行完毕，并接收返回值
    result = await get_user_info(1001)
    print(result)  # 输出: 用户 1001 的详细信息

asyncio.run(main())
```

### 协程中调用协程

一个协程可以启动另一个协程，从而可以任务根据工作内容，封装到不同的协程中。我们可以在协程中使用await关键字，链式的调度协程，来形成一个协程任务流。这是构建复杂异步逻辑的基础，代码会按照顺序依次执行。

```python
import asyncio

async def fetch_data(api_name):
    print(f"正在请求 {api_name} 接口...")
    await asyncio.sleep(1)
    print(f"{api_name} 接口请求完成")
    return f"{api_name} 的数据"

async def main():
    # 在协程中串行调用其他协程
    data1 = await fetch_data("用户信息")
    data2 = await fetch_data("订单列表")

    print("所有数据请求完毕")

asyncio.run(main())
```

### 协程中调用同步函数

在 asyncio 的协程中调用同步函数（比如普通的文件读写、耗时的 CPU 计算或使用了 time.sleep 的函数）是异步编程中最容易踩的坑。

如果直接在协程里调用同步函数，它会阻塞整个事件循环，导致其他并发的协程任务全部卡死，完全丧失异步编程的优势。

为了解决这个问题，asyncio 提供了将同步代码“丢”到线程池中执行的方案。以下是详细的示例代码和对比：

错误示范：直接调用同步函数（会阻塞事件循环），在这个例子中，同步函数里的 `time.sleep(2)`会像一堵墙，卡住整个单线程的事件循环，导致原本应该并发执行的 other_task 被迫等待。

```python
import asyncio
import time

# 一个普通的同步阻塞函数
def blocking_sync_function():
    print("同步函数: 开始执行耗时操作 (阻塞中)...")
    time.sleep(2)  # 模拟耗时的同步 I/O 或 CPU 计算
    print("同步函数: 执行完毕")
    return "同步函数的结果"

async def other_task():
    print("其他任务: 开始运行")
    for i in range(3):
        print(f"其他任务: 正在运行中... {i+1}")
        await asyncio.sleep(1)
    print("其他任务: 运行结束")

async def main():
    # 将两个任务并发执行
    await asyncio.gather(
        blocking_sync_function(),  # 错误！这会直接卡死整个事件循环 2 秒
        other_task()
    )

asyncio.run(main())
# 运行结果你会发现：other_task 必须等 blocking_sync_function 彻底跑完才能开始，并没有实现并发。
```

正确示范 1：使用 `loop.run_in_executor`（兼容旧版本 Python），这是 Python 3.8 及之前版本使用的方法。

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def blocking_sync_function(arg1, arg2):
    print(f"同步函数: 开始处理参数 {arg1}, {arg2}...")
    time.sleep(2)
    return f"处理结果: {arg1 + arg2}"

async def main():
    loop = asyncio.get_running_loop()

    # 使用默认的线程池执行器（第一个参数传 None）
    # 后面的参数会依次传递给 blocking_sync_function
    result = await loop.run_in_executor(
        None,
        blocking_sync_function,
        10, 20
    )

    print(f"主协程拿到了结果: {result}")

asyncio.run(main())
```

正确示范 2：使用 `asyncio.to_thread`（Python 3.9+ 推荐），这是最简洁的方法。它会自动把同步函数放到一个独立的线程池中去运行，并返回一个可等待对象（awaitable），这样就不会阻塞主事件循环了。

```python
import asyncio
import time

def blocking_sync_function():
    print("同步函数: 开始在线程池中执行...")
    time.sleep(2)
    print("同步函数: 执行完毕")
    return "同步函数的结果"

async def other_task():
    print("其他任务: 开始并发运行")
    for i in range(3):
        print(f"其他任务: 正在运行中... {i+1}")
        await asyncio.sleep(1)
    print("其他任务: 运行结束")

async def main():
    await asyncio.gather(
        asyncio.to_thread(blocking_sync_function),  # 正确！丢到线程池异步执行
        other_task()
    )

asyncio.run(main())
# 运行结果：你会发现 "其他任务" 和 "同步函数" 是同时打印日志的，实现了真正的并发。
```

## 并发协程

当有多个并发任务时，asyncio 提供了三种强大的工具来收集和处理结果，它们的侧重点各不相同：

- `asyncio.gather()`：最常用。一次性并发执行多个协程，按传入顺序返回所有结果。
- `asyncio.wait()`：更灵活。可以控制返回条件（比如“任意一个完成就返回”），返回已完成和未完成的任务集合。
- `asyncio.as_completed()`：实时处理。按任务实际完成的先后顺序逐个产出结果，哪个先跑完就先处理哪个。

```python
import asyncio
import random

async def fetch_data(task_id):
    delay = random.uniform(0.5, 2.0) # 随机模拟不同的网络延迟
    await asyncio.sleep(delay)
    print(f"任务 {task_id} 完成 (耗时 {delay:.2f}秒)")
    return f"任务 {task_id} 的结果"

async def main():
    tasks = [fetch_data(i) for i in range(3)]

    print("\n--- 1. asyncio.gather (按输入顺序收集所有结果) ---")
    # 注意：这里重新生成了 tasks，因为上面的 tasks 已经被 consume 过了
    results = await asyncio.gather(fetch_data(0), fetch_data(1), fetch_data(2))
    print(f"最终结果列表: {results}")

    print("\n--- 2. asyncio.wait (灵活控制，比如第一个完成就返回) ---")
    tasks = [fetch_data(i) for i in range(3)]
    # return_when=asyncio.FIRST_COMPLETED 表示任意一个任务完成就立刻返回
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"第一个完成的任务结果: {done.pop().result()}")
    # (注：实际生产中，pending 里的任务通常需要手动取消或继续等待)

    print("\n--- 3. asyncio.as_completed (按实际完成顺序实时处理) ---")
    tasks = [fetch_data(i) for i in range(3)]
    # 返回一个迭代器，哪个任务先跑完，就先 yield 哪个
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"实时拿到结果 -> {result}")

asyncio.run(main())
```

在使用 `asyncio.gather()` 时，如果其中一个协程报错了，默认会直接抛出异常中断所有任务。如果你希望忽略报错、让其他任务继续执行，可以将报错信息也作为结果返回，只需加上 `r`eturn_exceptions=True` 参数即可。

```python
# 即使某个任务报错，也不会中断，报错会以 Exception 对象的形式出现在结果列表中
results = await asyncio.gather(task1, task2, task3, return_exceptions=True)
```

### 并发协程处理数据同步

很多人有一个误区：“异步 = 单线程 = 不需要锁”。这是完全错误的。因为协程会在 await 处主动让出控制权，如果多个协程同时操作共享资源，就可能发生交错执行，导致数据不一致（例如经典的 counter += 1 在跨越 await 时会导致更新丢失）。

为了支持安全的并发执行，asyncio包含了 threading 和 multiprocessing 模块中的并发场景中数据同步的原语，当多个协程需要同时访问或修改共享资源（如全局变量、数据库连接等）时，必须使用 asyncio 提供的同步原语来保护“临界区”。

- Lock 互斥锁: 确保同一时间只有一个协程能访问临界区，解决竞态条件。推荐使用 async with lock: 语法，它会自动处理锁的获取与释放，即使在发生异常时也能保证锁被正确释放。asyncio.Lock 是不可重入的（同一个协程不能多次获取同一个锁），且不能与 threading 模块的锁混用。
- Semaphore 信号量: 允许有限数量的协程同时访问某个资源。常用于限制并发量，例如控制同时访问数据库的连接数或 API 的并发请求数。创建时指定最大并发数（如 sem = asyncio.Semaphore(5)），在协程中使用 async with sem: 包裹需要限制并发的代码块。
- Event 事件: 种简单的信号机制。一个或多个协程可以通过 await event.wait() 等待某个条件发生，另一个协程通过 event.set() 来唤醒所有等待者。非常适合用于“一次性”的就绪通知，比如等待某个初始化任务完成后，再启动后续的业务协程。
- Condition 条件变量: 结合了锁和事件的功能。允许一个或多个协程等待某个条件的变化，通常与共享状态结合使用。

#### 互斥锁 (Lock) - 保护共享变量

如果不加锁，两个协程同时执行 counter += 1 且中间有 await 挂起，最终的 counter 结果会小于预期。

```python
import asyncio

counter = 0
lock = asyncio.Lock()

async def increment_with_lock():
    global counter
    for _ in range(1000):
        # 使用 async with 自动获取和释放锁，防止竞态条件
        async with lock:
            temp = counter
            await asyncio.sleep(0)  # 模拟在临界区内发生协程切换
            counter = temp + 1

async def main():
    # 启动两个协程同时修改 counter
    await asyncio.gather(increment_with_lock(), increment_with_lock())
    print(f"加锁后的最终结果: {counter}")  # 预期输出: 2000

asyncio.run(main())
```

#### 信号量 (Semaphore) - 限制并发量

假设我们有一个只能同时处理 2 个请求的资源（如数据库连接池），信号量可以完美控制并发数量。

```python
import asyncio

# 限制最多 2 个协程同时进入临界区
semaphore = asyncio.Semaphore(2)

async def limited_task(task_id):
    async with semaphore:
        print(f"任务 {task_id} 开始执行 (当前并发数: 2)")
        await asyncio.sleep(1)  # 模拟耗时操作
        print(f"任务 {task_id} 执行完毕")

async def main():
    # 创建 5 个任务，但同一时间只有 2 个能真正运行
    tasks = [limited_task(i) for i in range(5)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

#### 事件 (Event) - 协程间的信号通知

模拟一个场景：消费者协程必须等待初始化任务（setter）完成后，才能开始工作。

```python
import asyncio

event = asyncio.Event()

async def waiter(name):
    print(f"{name} 正在等待初始化完成...")
    await event.wait()  # 阻塞，直到事件被设置
    print(f"{name} 收到信号，开始工作！")

async def initializer():
    print("初始化任务开始，预计耗时 2 秒...")
    await asyncio.sleep(2)
    print("初始化完成，发送信号！")
    event.set()  # 唤醒所有等待该事件的协程

async def main():
    await asyncio.gather(waiter("消费者A"), waiter("消费者B"), initializer())

asyncio.run(main())
```

#### 条件变量 (Condition) - 复杂的生产者消费者协作

```python
import asyncio

# 创建一个全局的条件变量
condition = asyncio.Condition()
queue = []

async def consumer(name):
    """消费者：等待队列中有数据后再消费"""
    while True:
        # 使用 async with 获取条件变量内部的锁
        async with condition:
            # 1. 检查条件：如果队列为空，则等待生产者的通知
            while not queue:
                print(f"消费者 {name} 发现队列为空，正在等待生产...")
                await condition.wait()  # 释放锁并挂起，等待被 notify 唤醒

            # 2. 被唤醒后，重新获取了锁，并且队列中已有数据
            item = queue.pop(0)
            print(f"消费者 {name} 成功消费了数据: {item}")

            # 如果遇到结束信号 None，则退出循环
            if item is None:
                break

async def producer():
    """生产者：生产数据并通知等待的消费者"""
    for i in range(5):
        await asyncio.sleep(1)  # 模拟生产数据的耗时

        # 获取条件变量的锁，准备修改共享队列
        async with condition:
            queue.append(i)
            print(f"生产者生产了数据: {i}，正在通知消费者...")
            # 通知所有因为 condition.wait() 而挂起的消费者协程
            condition.notify_all()

    # 生产结束后，放入一个 None 作为结束信号，并再次通知消费者退出
    async with condition:
        queue.append(None)
        condition.notify_all()
        print("生产者工作结束，已发送退出信号。")

async def main():
    # 启动 1 个生产者和 2 个消费者
    await asyncio.gather(
        producer(),
        consumer("A"),
        consumer("B")
    )

asyncio.run(main())
```

### 并发协程间数据交换

在异步编程中，最优雅的数据交换方式是使用队列 (Queue)，它完美实现了生产者-消费者模式。

- 协程安全：内部已经做好了异步同步处理，不需要手动加锁。
- 非阻塞：当队列满时，put 操作会挂起当前协程；当队列空时，get 操作会挂起，绝不会阻塞整个事件循环。
- 背压控制：可以通过设置 maxsize 参数限制队列容量，防止生产者过快导致内存溢出。

常用方法：

- `await queue.put(item)`：异步放入数据。
- `await queue.get()`：异步取出数据。
- `queue.task_done()`：标记一个取出的任务已处理完毕。
- `await queue.join()`：阻塞直到队列中所有任务都被处理完毕（常用于优雅退出）。

```python
import asyncio

async def producer(queue, num_items):
    """生产者：负责生产数据并放入队列"""
    for i in range(num_items):
        await queue.put(i)
        print(f"🏭 生产者生产了数据: {i}")
        await asyncio.sleep(0.5)  # 模拟生产耗时

    # 生产结束后，放入一个 None 作为结束信号
    await queue.put(None)
    print("🏭 生产者工作结束")

async def consumer(queue, name):
    """消费者：负责从队列取出数据并处理"""
    while True:
        item = await queue.get()  # 队列空时会自动挂起等待
        if item is None:  # 收到结束信号，退出循环
            queue.task_done()
            break
        print(f"📦 消费者 {name} 处理了数据: {item}")
        await asyncio.sleep(1)  # 模拟处理耗时（比生产慢）
        queue.task_done()  # 标记该任务已处理完毕
    print(f"📦 消费者 {name} 工作结束")

async def main():
    # 创建一个最大容量为 3 的队列，起到背压控制作用
    queue = asyncio.Queue(maxsize=3)

    # 启动 1 个生产者和 2 个消费者
    await asyncio.gather(
        producer(queue, 5),
        consumer(queue, "A"),
        consumer(queue, "B")
    )

asyncio.run(main())
```

这段代码和之前的 condition 示例对比着看。Queue 内部其实已经帮你封装好了这套“加锁-判断-等待-通知”的逻辑，而 Condition 则给了你更底层、更灵活的控制权。

### 注意事项

- 都使用了 `async with` 或标准的 `await queue.get()` 模式，这是最安全、最符合 Python 异步编程规范的写法。
- 严禁混用：绝对不要在 asyncio 中使用 threading 模块的锁或队列（如 threading.Lock, queue.Queue）。它们会阻塞当前线程，导致整个事件循环卡死，所有协程都会停止响应。
- 明确临界区：使用锁时，一定要先想清楚你要保护的“不变量”是什么。锁的范围（临界区）既不能太大（影响并发性能），也不能太小（保护不到位）。
- 善用上下文管理器：无论是 Lock、Semaphore 还是 Condition，都优先使用 async with 语法，这能极大降低因忘记释放锁或异常处理不当导致的死锁风险。
- 队列的优雅退出：在使用 Queue 时，通常通过放入一个特殊的终止信号（如 None）来通知消费者协程退出循环，或者配合 queue.join() 来确保所有任务处理完毕后再关闭程序。
