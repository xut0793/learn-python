import asyncio

async def my_coroutine():
    print("开始执行协程")
    await asyncio.sleep(1)  # 模拟非阻塞的 I/O 等待
    print("协程执行完毕")
    return "成功"

# 异步协程的入口函数，
async def main():
    task = asyncio.create_task(my_coroutine())
    print("任务已创建")
    result = await task
    print(f"任务结果：{result}")

# 启动事件循环的标准方式（Python 3.7+ 推荐）
asyncio.run(main())