# 命名进程
import multiprocessing as mp
import time

def foo():
    # 获取当前进程的名称
    name = mp.current_process().name
    print("Starting %s \n" % name)
    time.sleep(3)
    print("Exiting %s \n" % name)

if __name__ == "__main__":
    process_with_name = mp.Process(name="foo_process", target=foo)
    process_with_default_name = mp.Process(target=foo)
    process_with_name.start()
    process_with_default_name.start()