import tkinter as tk
from tkinter import messagebox


def submit():
    name = name_var.get().strip()
    age = age_var.get().strip()

    if name == "" or age == "":
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        return

    if not age.isdigit():
        messagebox.showerror("Lỗi", "Tuổi phải là số!")
        return

    age = int(age)

    if age <= 0:
        messagebox.showerror("Lỗi", "Tuổi phải lớn hơn 0!")
        return

    messagebox.showinfo("Thông tin", f"Tên: {name}\nTuổi: {age}")

root = tk.Tk()
root.title("Form nhập liệu")
root.geometry("300x220")

name_var = tk.StringVar()
age_var = tk.StringVar()

tk.Label(root, text="Tên").pack(pady=5)
tk.Entry(root, textvariable=name_var).pack()

tk.Label(root, text="Tuổi").pack(pady=5)
tk.Entry(root, textvariable=age_var).pack()

tk.Button(root, text="Submit", command=submit).pack(pady=15)
root.mainloop()