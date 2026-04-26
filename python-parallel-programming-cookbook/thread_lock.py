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