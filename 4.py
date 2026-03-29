import tkinter as tk

def hien_thi():
    ten = entry.get()
    ket_qua.config(text="Xin chào " + ten)
root = tk.Tk()
root.title("Ứng dụng chào hỏi")
root.geometry("300x200")
label = tk.Label(root, text="Nhập tên của bạn")
label.pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)
button = tk.Button(root, text="Hiển thị", command=hien_thi)
button.pack(pady=10)
ket_qua = tk.Label(root, text="")
ket_qua.pack(pady=10)
root.mainloop()