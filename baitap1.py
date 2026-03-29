#Bài 1
num = int(input("Nhập một số nguyên: "))
if num % 2 == 0:
    print("Số này là số chẵn")
else:
    print("Số này là số lẻ")
if num > 0:
    print("Số này là số dương")
elif num < 0:
    print("Số này là số âm")
else:
    print("Số này bằng 0")