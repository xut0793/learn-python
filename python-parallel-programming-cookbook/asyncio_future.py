'''
Date         : 2026-04-26 21:17:02 星期0
Author       : xut
Description  : 
'''
import asyncio

async def fist_coroutine(future, n):
  """"前N个数之和"""
  sum = 0
  for i in range(1, n + 1):
    sum += i
  await asyncio.sleep(3)
  future.set_result("first coroutine (sum of N integers) result = " + str(sum))

async def second_coroutine(future, n):
  """"前N个数乘积"""
  product = 1
  for i in range(1, n + 1):
    product *= i
  await asyncio.sleep(3)
  future.set_result("second coroutine (product of N integers) result = " + str(product))

def get_result(future):
  print(future.result())


future_1 = asyncio.Future()
future_2 = asyncio.Future()
tasks = [
  fist_coroutine(future_1, 10),
  second_coroutine(future_2, 10)
]
future_1.add_done_callback(get_result)
future_2.add_done_callback(get_result)

asyncio.run(asyncio.wait(tasks))