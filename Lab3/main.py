from multiprocessing import Manager, Process, Value
from time import sleep
from random import randint
import os
import traceback
import sys

manager = Manager()
pipeline = manager.list()
flag = Value("i", 1)
flagSenders = Value("i", 1)

def getter():
	while True:
		try:
			if (len(pipeline) <= 80) and flag.value:
				pass
			else:
				pipeline.pop()
			sleep(0.5)

		except:
			pass

def sender():
	while flagSenders.value:
		try:
			if (len(pipeline) >= 100):
				while True:
					if (len(pipeline) <= 80):
						break
					pass
			else:
				pipeline.append(randint(1,100))
			sleep(0.2)

		except:
			pass

if __name__ == '__main__':
	mp = [Process(target = getter) for i in range(2)] + [Process(target = sender) for i in range(3)]
	for i in mp:
		i.daemon = True
		i.start()

	while True:
		try:
			print(len(pipeline))
			print(pipeline)

			sleep(0.2)
			os.system("clear")

			if len(pipeline) == 0:
				for i in mp[:2]:
					i.kill()
				sys.exit()

		except KeyboardInterrupt:
			for i in mp[2:]:
				i.kill()
			flagSenders = 0
			flag.value = 0