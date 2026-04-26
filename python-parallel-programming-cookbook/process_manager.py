import multiprocessing as mp

def worker(dictionary, key, item):
    dictionary[key] = item
    print("key = %d, value = %s" % (key, item))

if __name__ == '__main__':
    mgr = mp.Manager()
    dictionary = mgr.dict()
    jobs = [mp.Process(target=worker, args=(dictionary, i, i*2)) for i in range(10)]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print("Result: ",dictionary)

# 一个管理者对象控制着持有Python对象的服务进程，并允许其它进程操作共享对象。
# 管理者有以下特性：
#     它控制着管理共享对象的服务进程
#     它确保当某一进程修改了共享对象之后，所有的进程拿到共享对象都得到了更新