from string import ascii_lowercase
from hashlib import sha256
from itertools import product, islice
from multiprocessing import Process
import time

hashes = []
with open("hash.txt", "r") as hashFile:
	for i in hashFile.readlines():
		hashes.append(i.rstrip())


combs = product(ascii_lowercase, repeat = 5)

menu = ""
for index, hsh in enumerate(hashes):
	menu += f"{index+1}. {hsh}\n"
menu += "Выберите хэш: "

hashNum = int(input(menu)) - 1
hsh = hashes[hashNum]

processNum = int(input("Введите количество потоков: "))
processArr = []
pswd = ""

def calculate(combs, offsetL, offsetR, hash):
	for password in islice(combs, offsetL, offsetR):
		if sha256("".join(password).encode("utf-8")).hexdigest() == hash:
			pswd = "".join(password)
			print(f"пароль: {pswd}")

			end_time = time.time()
			print(f"Затрачено: {end_time-start_time}")

			for proc in processArr:
				proc.terminate()
			return

offsets = []
offsetL = 0
offsetR = 26**5 // processNum
offset = offsetR

for i in range(processNum):
	if (i == processNum - 1):
		offsetR = None
		offsets.append([offsetL, offsetR])
	else:
		offsets.append([offsetL, offsetR])
		offsetL = offsetR + 1
		offsetR += offset

print(offsets)
exit()

start_time = time.time()
for i in range(processNum):
	p = Process(target = calculate, args = (combs, offsets[i][0], offsets[i][1], hsh,))
	p.start()
	processArr.append(p)