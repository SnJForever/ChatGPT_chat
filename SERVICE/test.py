""" import threading
import time
from tqdm import tqdm 

import datetime

#现在执行的线程
threads=[]

#设置总线程个数
total_thread_num=50


list = []
def ThFun(frame_idx):
    time.sleep(0.1)
    list.append((frame_idx,"aa"))

for frame_idx in tqdm(range(1000), 'Face Renderer:'):
    print(frame_idx)
    while(True):
        current_thread_num = 0
        for thread in threads:
            if thread.isAlive():
                current_thread_num += 1
            
        if (current_thread_num >= total_thread_num ):
            time.sleep(0.1)
            continue
        else:
            break
    
    current_thread = threading.Thread(target = ThFun, args = (frame_idx,))
    current_thread.start()
    threads.append(current_thread)
    

while(True):
    current_thread_num = 0
    for thread in threads:
        if thread.isAlive():
            current_thread_num += 1

    if (current_thread_num == 0 ):
        break
    else:
        continue

def take_first(elem):
    return elem[0]

print('start time:',datetime.datetime.now())
print(list)
list.sort(key=take_first)
print(list)

# result = []
# for i in list:
#     result.append(i[1])

result = [i[1] for i in list]
print('end time:',datetime.datetime.now())
print(result) """


""" import threading
import tqdm
import time
import datetime

#现在执行的线程
threads=[]

#设置总线程个数
total_thread_num=5
start_time = datetime.datetime.now()
print('start time:',start_time)
list = []
def ThFun(start, stop):
    for item in range(start, stop):
        time.sleep(0.1)
        list.append((item,'a'))
step = int(1000/total_thread_num)
for n in range(0, 1000, step):
    stop = n + step if n + step <= 1000 else 1000
    print(n,stop)
    current_thread = threading.Thread(target = ThFun, args =  (n, stop))
    current_thread.start()
    threads.append(current_thread)

while(True):
    current_thread_num = 0
    for thread in threads:
        if thread.isAlive():
            current_thread_num += 1
    if (current_thread_num == 0 ):
        break
    else:
        time.sleep(0.1)
        continue
end_time = datetime.datetime.now()    
print('end_time time:',end_time)
print('total use time:',end_time - start_time)
print("list=",list) """

""" import time

words = ["apple", "bananan", "cake", "dumpling"] * 50



def clock(func):
    def clocked(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("执行时间：", end - start)
        return result
    return clocked


from multiprocessing.dummy import Pool as ThreadPool

class process_data():

    def process(self, item,a):
        for i in item:
            print(i,a, "正在并行for循环")
            time.sleep(0.1)

    @clock
    def test(self):
        for i in words:
            time.sleep(0.1)

    @clock
    def make_it(self):
        pool = ThreadPool(processes=10)
        pool.apply(self.process, (words,'aa'))
        pool.close()
        pool.join()


process_data().make_it()

# process_data().test() """

import time
from multiprocessing.dummy import Pool as ThreadPool
import datetime
start = datetime.datetime.now()

def process(item,a):
    print(item,a, "正在并行for循环")
    time.sleep(0.1)
    return a

pool = ThreadPool(processes=5)

result_list = [pool.apply_async(process, (frame_idx,'b')) for frame_idx in range(60)]

pool.close()
pool.join()
result_list_1 = [i._value for i in result_list]  

print(result_list_1)

end = datetime.datetime.now()
print("执行时间：", end - start)

start = datetime.datetime.now()


for frame_idx in range(60):
    time.sleep(0.1)

end = datetime.datetime.now()
print("执行时间：", end - start)