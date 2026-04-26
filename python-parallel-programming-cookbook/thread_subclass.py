import _thread
import threading
import time

exitFlag = 0

class myThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.delay, 5)
        print("Exiting " + self.name)

def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            _thread.exit()
        time.sleep(delay)
        print("%s : %s " % (thread_name, time.ctime(time.time())))
        counter -= 1

t1 = myThread(1, "Thread-1", 1)
t2 = myThread(2, "Thread-2", 2)

t1.start()
t2.start()
t1.join()
t2.join()
print("Exiting Main Thread")