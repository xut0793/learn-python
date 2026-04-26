'''
Date         : 2026-04-26 21:25:49 星期0
Author       : xut
Description  : 
'''
import asyncio
import time


async def fetch_data(task_id, delay):
    print(f"任务 {task_id}: 开始发起 I/O 请求...")
    #  await 暂停当前协程，交出控制权给事件循环
    await asyncio.sleep(delay)
    print(f"任务 {task_id}: I/O 请求完成，拿到结果！")
    return f"任务 {task_id} 的结果"


async def main():
    start_time = time.time()
    # 将协程函数包装成任务，并提交给事件循环，此时 fetch_data 并没有立刻执行完，而是被事件循环接管了
    task1 = asyncio.create_task(fetch_data(1, 2))
    task2 = asyncio.create_task(fetch_data(2, 1))
    task3 = asyncio.create_task(fetch_data(3, 3))

    # 等待所有任务完成（Future 占位符被填入结果）
    # asyncio.gather 会收集所有 Task (Future) 的最终结果
    results = await asyncio.gather(task1, task2, task3)

    print(f"所有任务完成，总耗时: {time.time() - start_time:.2f} 秒")
    print(f"最终结果: {results}")


# 启动事件循环
if __name__ == "__main__":
    asyncio.run(main())
