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


# daemon = True 的进程并不是Unix的守护进程或服务（daemons or services），所以当主进程退出，它们也会自动结束。
# daemon = True 的进程不允许创建子进程。否则，当后台进程跟随父进程退出的时候，新建的子进程会变成孤儿进程。