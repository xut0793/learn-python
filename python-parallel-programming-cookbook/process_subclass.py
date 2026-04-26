# 自定义子类进程
import multiprocessing as mp

class MyProcess(mp.Process):
    def run(self):
        print("called run method in MyProcess: %s" % self.name)

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = MyProcess()
        jobs.append(p)
        p.start()
        p.join()