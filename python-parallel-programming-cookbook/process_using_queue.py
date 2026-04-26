import multiprocessing as mp
import random
import time

class Producer(mp.Process):
    def __init__(self, queue):
        mp.Process.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print("Process Producer: item %d appended to queue %s" % (item, self.name))
            time.sleep(1)
            print("The size of queue is %s" % self.queue.qsize())

class Consumer(mp.Process):
    def __init__(self, queue):
        mp.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                print("The queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                print("Process Consumer: item %d popped from by %s \n" % (item, self.name))
                time.sleep(1)

if __name__ == "__main__":
    queue = mp.Queue()
    process_producer = Producer(queue)
    process_consumer = Consumer(queue)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()