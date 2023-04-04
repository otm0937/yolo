# from multiprocessing import Process, Queue, set_start_method, Manager
# import time
# import numpy as np
#
#
# def send_to_queue(q, mylist):
#     # function to put elements into Queue
#     for num in mylist:
#         q.put(np.random.random((416, 416, 3)))
#
#
# def pick_from_queue(q, mylist):
#     # function to print queue elements
#     print("Queue elements:")
#     t1 = time.time()
#     # print(q.qsize())
#     # for num in mylist:
#     #     result = q.get()
#     #     # print(q.)
#     print("Queue is now empty!", time.time() - t1)
#
#
# if __name__ == "__main__":
#     set_start_method('fork')
#     # input list
#     mylist = [i for i in range(100)]
#
#     m = Manager()
#
#     # creating multiprocessing Queue
#     q = m.Queue()
#
#     # creating new processes
#     p1 = Process(target=send_to_queue, args=(q, mylist))
#     p2 = Process(target=pick_from_queue, args=(q, mylist))
#
#     # running process p1 and p2
#     p1.start()
#     p2.start()
#
#     # if we need waiting p1 and p2 process to finish their job
#     # p1.join()
#     # p2.join()

import multiprocessing
import time


def worker(x, que):
    que.put(x ** 2)
    # print(que.qsize())


if __name__ == '__main__':
    inputs = list(range(1000))

    pool = multiprocessing.Pool(processes=5)
    m = multiprocessing.Manager()
    q = m.Queue()
    for i in inputs:
        p = multiprocessing.Process(target=worker, args=(i, q))
        p.start()
        print(q.qsize())
    # workers = [pool.apply_async(worker, (i, q)) for i in inputs]
    # while q.qsize() < len(inputs):
    #     time.sleep(1)
    #
    # results = [q.get() for _ in range(q.qsize())]
    # assert len(results) == len(inputs)
