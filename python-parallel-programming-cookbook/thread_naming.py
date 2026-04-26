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
def third_func():
    print(threading.current_thread().name + " is starting")
    time.sleep(2)
    print(threading.current_thread().name + ' is Exiting ')

if __name__ == "__main__":
    t1 = threading.Thread(target=first_func, name="first_func")
    t2 = threading.Thread(target=second_func, name="second_func")
    t3 = threading.Thread(target=third_func, name="third_func")
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()