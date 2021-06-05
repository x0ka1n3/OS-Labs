from multiprocessing import Process, Value
import time
import os

quant = Value("i", 5)

def progress(curNum, allNum, barLen = 10):
	# return f"{curNum} {allNum} {barLen}"
	# return f'[{curNum/}]'
	return f"""[{(curNum*barLen//allNum)*"#"}{(barLen-(curNum*barLen//allNum))*"-"}] {curNum}s/{allNum}s"""

def func1(run, start_time):
	i = 0
	while True:
		if run.value == 1:
		 	os.system("cls")
		 	i-=1
		 	print(f"Поток 1 (числа до минус бесконечности) {progress(int(time.time()) - start_time.value, quant.value)} \n {i}")
		 	time.sleep(0.2)

def func2(run, start_time):
	i = 0
	while True:
	 	if run.value == 2:
		 	os.system("cls")
		 	i+=1
		 	print(f"Поток 2 (числа до плюс бесконечности) {progress(int(time.time()) - start_time.value, quant.value)} \n {i}")
		 	time.sleep(0.2)

def func3(run, start_time):
	i = 0
	while True:
	 	if run.value == 3:
		 	os.system("cls")
		 	i+=1
		 	print(f"Поток 3 ({i} нулей) {progress(int(time.time()) - start_time.value, quant.value)} \n {i*'0'}")
		 	time.sleep(0.2)

def worker():
	queue = [Process(target = func1, args = (run,start_time,)), Process(target = func2, args=(run,start_time,)), Process(target = func3, args=(run,start_time,))]
	[i.start() for i in queue]
	while True:
		for i in range(1, 4):
			run.value = i
			start_time.value = int(time.time())
			time.sleep(quant.value)

run = Value("i", 0)
start_time = Value("i", int(time.time()))
if __name__ == '__main__':
	worker()