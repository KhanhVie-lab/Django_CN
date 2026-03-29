import tkinter as tk
from tkinter import messagebox

products = []

def add_product():
    name = name_var.get().strip()
    price = price_var.get().strip()

    if name == "" or price == "":
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ!")
        return

    if not price.isdigit():
        messagebox.showerror("Lỗi", "Giá phải là số!")
        return

    product = f"{name} - {price}đ"
    products.append(product)
    listbox.insert(tk.END, product)

    name_var.set("")
    price_var.set("")

def delete_product():
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
        products.pop(selected_index)
    except:
        messagebox.showerror("Lỗi", "Chọn sản phẩm để xoá!")

root = tk.Tk()
root.title("Quản lý sản phẩm")
root.geometry("350x400")
name_var = tk.StringVar()
price_var = tk.StringVar()

tk.Label(root, text="Tên sản phẩm").pack()
tk.Entry(root, textvariable=name_var).pack(pady=5)

tk.Label(root, text="Giá").pack()
tk.Entry(root, textvariable=price_var).pack(pady=5)

tk.Button(root, text="Thêm", command=add_product).pack(pady=5)
tk.Button(root, text="Xoá", command=delete_product).pack(pady=5)

listbox = tk.Listbox(root, width=40)
listbox.pack(pady=15)

root.mainloop()