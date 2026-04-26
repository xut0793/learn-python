'''
Date         : 2026-04-26 13:31:17 星期0
Author       : xut
Description  : 
'''
import concurrent.futures
import time

number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def count(x):
  for i in range(0, 10000000):
    i += 1
  return i * x
def evaluate_item(x):
  # 计算总和，这里只是为了消耗时间
  result_item = count(x)
  return result_item

if __name__ == '__main__':
  # 顺序执行
  start_time = time.time()
  for item in number_list:
    result_sum = evaluate_item(item)
    print("item: %s, result: %s" % (item, result_sum))
  print("Sequential execution in " + str(time.time() - start_time), "seconds")

  # 线程池进行
  start_time_thread = time.time()
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(evaluate_item, item) for item in number_list]
    for future in concurrent.futures.as_completed(futures):
      result_sum = future.result()
      print("item: %s, result: %s" % (item, result_sum))

    print ("Thread pool execution in " + str(time.time() - start_time_thread), "seconds")

  # 进程池进行
  start_time_process = time.time()
  with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(evaluate_item, item) for item in number_list]
    for future in concurrent.futures.as_completed(futures):
      result_sum = future.result()
      print("item: %s, result: %s" % (item, result_sum))
    print ("Process pool execution in " + str(time.time() - start_time_process), "seconds")
  
# 输出结果
# item: 1, result: 10000000
# item: 2, result: 20000000
# item: 3, result: 30000000
# item: 4, result: 40000000
# item: 5, result: 50000000
# item: 6, result: 60000000
# item: 7, result: 70000000
# item: 8, result: 80000000
# item: 9, result: 90000000
# item: 10, result: 100000000
# Sequential execution in 2.701934576034546 seconds
# item: 10, result: 10000000
# item: 10, result: 30000000
# item: 10, result: 20000000
# item: 10, result: 40000000
# item: 10, result: 50000000
# item: 10, result: 60000000
# item: 10, result: 70000000
# item: 10, result: 90000000
# item: 10, result: 80000000
# item: 10, result: 100000000
# Thread pool execution in 2.6747519969940186 seconds
# item: 10, result: 10000000
# item: 10, result: 30000000
# item: 10, result: 40000000
# item: 10, result: 20000000
# item: 10, result: 50000000
# item: 10, result: 60000000
# item: 10, result: 80000000
# item: 10, result: 70000000
# item: 10, result: 100000000
# item: 10, result: 90000000
# Process pool execution in 1.4101128578186035 seconds