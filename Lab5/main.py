menu = f"""
--------
1. Выделить память
2. Освободить память
3. Показать состояние памяти
4. Выход
--------
"""
class memory(object):
	procList = {}
	procNum = 0

	def allocate(self):
		procName = input("Название процесса: ")
		procMem = int(input("Память процесса: "))

		if procMem > self.free() or procMem < 0:
			print("Невозможно выделить память под процесс"); return

		self.procList.update({self.procNum:[procName, procMem]})
		self.procNum+=1

	def delete(self):
		procId = int(input("Введите идентификатор процесса для освобождения: "))
		if procId in self.procList:
			del self.procList[procId]
		else:
			print("Процесс с таким идентификатором не найден")

	def showMem(self):
		print(8*"-")
		print(f"Свободно {self.free()} / {64*1024} ({round(self.free() / (64*1024) * 100, 2)} %)")

		for i in self.procList:
			print(f"{i} | {self.procList[i][0][:12]} | {self.procList[i][1]} Байт ({round(self.procList[i][1] / (64*1024) * 100, 2)} %)")
		print(8*"-")

	def free(self):
		return 64*1024 - sum([self.procList[i][1] for i in self.procList])

mem = memory()

while True:
	try:
		while True:
			inp = int(input(menu))
			break
	except:
		pass

	if inp == 1:
		mem.allocate()
	if inp == 2:
		mem.delete()
	if inp == 3:
		mem.showMem()
	if inp == 4:
		break