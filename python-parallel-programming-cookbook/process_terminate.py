# 使用 terminate 杀死进程
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
    # 我们通过读进程的 ExitCode 状态码（status code）验证进程已经结束， ExitCode 可能的值如下：
    # == 0: 没有错误正常退出
    # > 0: 进程有错误，并以此状态码退出
    # < 0: 进程被 -1 * 的信号杀死并以此作为 ExitCode 退出
    # 在我们的例子中，输出的 ExitCode 是 -15 。负数表示子进程被数字为15的信号杀死。