text = input("Nhập một chuỗi: ")
length = len(text)
print("Số ký tự:", length)
print("Các ký tự trong chuỗi:")
for char in text:
    print(char)
reversed_text = text[::-1]
print("Chuỗi đảo ngược:", reversed_text)