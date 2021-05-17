import os
import psutil
import json
import xml.etree.ElementTree as xml

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def rmfile():
	fName = input("Название файла: ")
	if os.path.exists(fName):
		remove = int(input("Точно удалить? (1/0)"))
		if remove in range(2) and remove == 1:
			os.remove(fName)

def getDriveInfo():
	disks = psutil.disk_partitions()
	for i in range(len(disks)):
		curDisk = disks[i]
		print(f"""Диск {i+1} | путь: {curDisk.device}""")
		print(f"""Точка монтирования: {curDisk.mountpoint}""")
		print(f"""Файловая система: {curDisk.fstype}""")
		DU = psutil.disk_usage(curDisk.mountpoint)
		print(f"\tПамять")
		print(f"\t\tВсего: {sizeof_fmt(DU.total)}")
		print(f"\t\tСвободно: {sizeof_fmt(DU.free)}")
		print(15*"*")

def createObject():
	fName = input("Название файла: ")
	if os.path.exists(fName):
		"Файл уже существует."
	else:
		open(fName, "w")

def askMenu():
	secMenu = """
	1. Создать файл
	2. Записать новые данные
	3. Вывести данные
	4. Удалить файл
	Выбор: """

	while True:
		try:
			choice = int(input(secMenu))
		except KeyboardInterrupt:
			exit()
		except:
			choice = 0

		if choice in range(1,5):
			return choice
		else:
			print("Введите число от 1 до 5")

def files():
	choice = askMenu()
	if choice == 1:
		createObject()
	if choice == 2:
		fName = input("Название файла: ")
		addStr = input("Введите новую строку: ")
		if os.path.exists("fName"):
			with open(fName, "a") as file:
				file.write(addStr)
		else:
			with open(fName, "w") as file:
				file.write(addStr)
	if choice == 3:
		fName = input("Название файла: ")
		if os.path.exists(fName):
			with open(fName, "r") as file:
				print(file.read())
		else:
			print("Файл с таким названием не существует")
	if choice == 4:
		rmfile()




def jsons():
	choice = askMenu()
	if choice == 1:
		createObject()
	if choice == 2:
		fName = input("Название файла: ")
		array = {}
		print("Оставьте оба ввода пустыми, чтобы закончить цикл")
		while True:
			key = ""; value = ""
			key = input("Введите ключ: ")
			value = input("Введите элемент: ")

			if len(key) != 0 and len(value) != 0:
				array.update({f"{key}": f"{value}"})
				print(array)
			else:
				break

		if os.path.exists("fName"):
			rewrite = int(input("Файл уже существует, перезаписать? (1/0)"))
			if rewrite in range(2) and rewrite == 1:
				json.dump(array, open(fName, "w"))
		else:
			json.dump(array, open(fName, "w"))

	if choice == 3:
		fName = input("Название файла: ")
		if os.path.exists(fName):
			print(json.load(open(fName, "r")))
		else:
			print("Файл с таким названием не существует")

	if choice == 4:
		rmfile()

def xmls():
	choice = askMenu()
	if choice == 1:
		createObject()
	if choice == 2:
		editor = int(input("""
					Добавить элементы:
					1. С помощью встроенного редактора текста
					2. Ввести новые элементы
					Выбор: """))
		fName = input("Название файла: ")
		root = xml.Element("main")


		if editor == 1:
			import click
			click.edit(filename = fName)
		if editor == 2:
			flag = 0
			while True:
				if flag == 1:
					break
				newElText = input("Введите название нового элемента (оставить пустым для завершения цикла): ")
				if len(newElText) == 0:
					break
				newEl = xml.Element(newElText)
				root.append(newEl)

				while True:
					newSubElText = input("Введите название вложенного элемента (оставить пустым для завершения): ")
					if len(newSubElText) == 0:
						flag = 1
						break
					newSubEl = xml.SubElement(newEl, newSubElText)

					newSubEl.text = input("Введите текст для вложенного элемента: ")
			tree = xml.ElementTree(root)
			xml.indent(tree)
			with open(fName, "wb") as file:
				tree.write(file, encoding = "utf-8")

	if choice == 3:
		fName = input("Название файла: ")
		with open(fName, "r") as xml:
			print(xml.read())
	
	if choice == 4:
		rmfile()

from zipfile import ZipFile as ZIP

def zips():
	choice = askMenu()
	if choice == 1:
		with ZIP(input("Название архива: "), "w") as z:
			z.close()

	if choice == 2:
		with ZIP(input("Название архива: "), "a") as z:
			while True:
				fName = input("Название добавляемого файла (оставьте пустым для завершения): ")
				if len(fName) == 0:
					break
				z.write(fName)
			z.close()

	if choice == 3:
		with ZIP(input("Название архива: "), "r") as z:
			z.printdir()
			z.close()

	if choice == 4:
		rmAsk = int(input("""
					1. Удалить файл в архиве
					2. Удалить архив
					Выбор: """))
		if rmAsk == 1:
			fName = input("Название архива: ")
			fNameDel = input("Название файла для удаления: ")
			zin = ZIP(fName, 'r')
			zout = ZIP(f"{fName}_new", 'w')
			for item in zin.infolist():
				buff = zin.read(item.filename)
				if (item.filename != fNameDel):
					zout.writestr(item, buff)
			zin.close()
			zout.close()

			os.rename(f"{fName}_new", f"{fName}")
		if rmAsk == 2:
			rmfile()

def main():
	mainMenu = """
1. Вывести информацию о дисках
2. Работа с файлами
3. Работа с JSON
4. Работа с XML
5. Работа с ZIP архивами
Выбор: """

	while True:
		try:
			choice = int(input(mainMenu))
		except KeyboardInterrupt:
			exit()
		except:
			choice = 0

		if choice in range(1,6):
			if choice == 1:
				getDriveInfo()
			if choice == 2:
				files()
			if choice == 3:
				jsons()
			if choice == 4:
				xmls()
			if choice == 5:
				zips()
			break
		else:
			print("Введите число от 1 до 5")

if __name__ == '__main__':
	main()