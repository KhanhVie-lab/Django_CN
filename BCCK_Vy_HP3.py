import ttkbootstrap as ttk
import tkinter as tk
from tkinter import *
from tkinter import messagebox

window = ttk.Window(themename="superhero")
window.title("Quản lí học sinh")
window.geometry("650x500")
for i in range(4):
    window.columnconfigure(i, weight=1)

label_title = ttk.Label(
    window,
    text="QUẢN LÍ HỌC SINH",
    font=("Arial",20,"bold"),
    bootstyle="info"
)
label_title.grid(
    row = 0,
    column = 1, 
    columnspan = 4, 
    pady = 20,
    sticky = "ew"
)

label_name = ttk.Label(
    window,
    text = "Tên học sinh"
)
label_name.grid(
    row=1,                       
    column=0,                           
    padx=(20,10),                          
    pady=10,
    sticky="e"                            
)

entry1 = ttk.Entry(
    window,
    width=30                  
)
entry1.grid(
    row=1,                          
    column=1,
    padx=(0,20),                          
    pady=10,
    sticky="w"                      
)

label_class = ttk.Label(
    window,
    text = "Lớp"
)
label_class.grid(
    row=2,                       
    column=0,                           
    padx=(20,10),                          
    pady=10,
    sticky="e"                            
)

entry2 = ttk.Entry(
    window,
    width=30                  
)
entry2.grid(
    row=2,                          
    column=1,
    padx=(0,20),                          
    pady=10,
    sticky="w"                      
)

ds_hs = [
     {'ten':'An', 'lop': '10'},
     {'ten':'Dũng', 'lop': '7'}
]

label_ds = ttk.Label(
    window,
    text="Danh sách học sinh",
    bootstyle="info"
)
label_ds.grid(
    row=3,
    column=1,
    columnspan=2,
    pady=(10,5)
)

listbox = tk.Listbox(
    window,
    width=30,
    height=10
)
listbox.grid(
    row=4,
    column=1,
    columnspan=2,
    pady=10
)

for item in ds_hs:
        listbox.insert("end",item["ten"])

def update_listbox():
    listbox.delete(0,"end")
    for item in ds_hs:
        listbox.insert("end",item["ten"])

def insert():
    ten = entry1.get().strip().title()
    lop = entry2.get().strip()
    if not ten:
        messagebox.showwarning(
             "Thông báo",
             "Vui lòng nhập tên học sinh"
        ) 
        return
    if not lop:
        messagebox.showwarning(
             "Thông báo",
             "Vui lòng nhập lớp"
        ) 
        return
    ds_hs.append({
        'ten' : ten,       
        'lop' : lop
    })
    update_listbox()
    refresh()

def delete():
    abc = listbox.curselection()
    if not abc:
        messagebox.showwarning(
             "Thông báo",
             "Vui lòng chọn học sinh cần xóa"
        )
        return
    del ds_hs[abc[0]]
    update_listbox()
    entry1.delete(0, END)
    entry2.delete(0, END)
    label_ten.config(
        text="Tên:"
    )
    label_lop.config(
        text="Lớp:"
    )

def refresh():
    entry1.delete(0, END)
    entry2.delete(0, END)
    label_ten.config(
        text="Tên:"
    )

    label_lop.config(
        text="Lớp:"
    )

def edit():
    abc = listbox.curselection()
    ten = entry1.get().strip().title()
    lop = entry2.get().strip()
    if not abc:
        messagebox.showwarning(
            "Thông báo",
            "Vui lòng chọn học sinh cần sửa"
        )
        return
    if not ten or not lop:
        messagebox.showwarning(
            "Thông báo",
            "Vui lòng nhập đầy đủ thông tin"
        )
        return
    ds_hs[abc[0]] = {
        'ten' : ten,
        'lop' : lop
    }
    update_listbox()

def show_detail(event):
    abc = listbox.curselection()
    if abc:
        item = ds_hs[abc[0]] 
        label_ten.config(
            text = f"Tên: {item['ten']}"
        )
        label_lop.config(
            text = f"Lớp: {item['lop']}"
        )
    entry1.delete(0, END)
    entry1.insert(0, item["ten"])
    entry2.delete(0, END)
    entry2.insert(0, item["lop"])

listbox.bind(
    "<<ListboxSelect>>",
    show_detail
)

label_ten = ttk.Label(
    window,
    text="Tên: "
)
label_ten.grid(
    row=3,
    column=3,
    sticky="w"
)

label_lop = ttk.Label(
    window,
    text="Lớp: "
)
label_lop.grid(
    row=4,
    column=3,
    sticky="w"
)

insert_button = ttk.Button(window, text="Insert", width=10, command = insert, bootstyle="success")
insert_button.grid(
    row=5,
    column=0,
    padx=10,
    pady=20,
    sticky="e"
)
delete_button = ttk.Button(window, text="Delete", width=10, command = delete, bootstyle="success")
delete_button.grid(
    row=5,
    column=1,
    padx=10,
    pady=20
)
refresh_button = ttk.Button(window, text="Refresh", width=10, command = refresh, bootstyle="success")
refresh_button.grid(
    row=5,
    column=2,
    padx=10,
    pady=20

)
edit_button = ttk.Button(window, text="Edit", width=10, command = edit, bootstyle="success")
edit_button.grid(
    row=5,
    column=3,
    padx=10,
    pady=20,
    sticky="w"
)

window.mainloop() 