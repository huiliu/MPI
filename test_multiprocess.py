#!/export/home/liuhui/opt/bin/python3

from multiprocessing import Process, JoinableQueue
from time import sleep
#q是任务队列
#NUM是并发线程总数
#JOBS是有多少任务
q = JoinableQueue()
NUM = 12
JOBS = 100
#具体的处理函数，负责处理单个任务
def do_somthing_using(arguments):
    i=0
    while i < 100000:
        i += 1
    print(arguments)
#这个是工作进程，负责不断从队列取数据并处理
def working():
    while True:
        arguments = q.get()
        do_somthing_using(arguments)
#       sleep(1)
        q.task_done()
#fork NUM个线程等待队列
for i in range(NUM):
    t = Process(target=working)
    t.Daemon=True
    t.start()
#把JOBS排入队列
for i in range(JOBS):
    q.put(i)
#等待所有JOBS完成
q.join()
