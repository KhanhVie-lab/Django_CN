import tkinter as tk
import ttkbootstrap as ttk

window = ttk.Window(themename="flatly")
window.title("Ứng dụng quản lý và mua bán động vật trong sở thú")
window.geometry("500x600")

zoo = []
Money = 100

def update_listbox():
    listbox.delete(0, "end")
    for animal in zoo:
        text = f"{animal['TEN']} | {animal['MOI TRUONG SONG']} | {animal['CAN NANG']} | {animal['GIA TIEN']}"
        listbox.insert("end", text)

def insert():
    global Money
    name = entry_name.get()
    habitat = entry_habitat.get()
    weight = entry_weight.get()
    price = entry_price.get()

    if name and price.isdigit():
        price_val = int(price)
        if Money >= price_val:
            zoo.append({
                "TEN": name,
                "MOI TRUONG SONG": habitat,
                "CAN NANG": weight,
                "GIA TIEN": price
            })

            entry_name.delete(0, "end")
            entry_habitat.delete(0, "end")
            entry_weight.delete(0, "end")
            entry_price.delete(0, "end")

            Money -= price_val
            label_money.config(text=f"Money = {Money}")
            update_listbox()

def edit():
    selected1 = listbox.curselection()
    if selected1:
        index = selected1[0]
        name2 = entry_name.get()
        habitat2 = entry_habitat.get()
        weight2 = entry_weight.get()
        price2 = entry_price.get()
        
        if name2:
            zoo[index] = {
                "TEN": name2,
                "MOI TRUONG SONG": habitat2,
                "CAN NANG": weight2,
                "GIA TIEN": price2 if price2 else zoo[index]["GIA TIEN"]
            }
            entry_name.delete(0, "end")
            entry_habitat.delete(0, "end")
            entry_weight.delete(0, "end")
            entry_price.delete(0, "end")

            update_listbox()

def delete():
    selected = listbox.curselection()
    if selected:
        global Money
        index = selected[0]
        
        animal_to_delete = zoo[index]
        price = animal_to_delete["GIA TIEN"] 
        
        if price.isdigit():
            Money += int(price)

        del zoo[index]
        
        update_listbox()
        label_money.config(text=f"Money = {Money}")

def showinfo(event):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        animal = zoo[index]
        
        entry_name.delete(0, "end")
        entry_habitat.delete(0, "end")
        entry_weight.delete(0, "end")
        entry_price.delete(0, "end")
        
        entry_name.insert(0, animal["TEN"])
        entry_habitat.insert(0, animal["MOI TRUONG SONG"])
        entry_weight.insert(0, animal["CAN NANG"])
        entry_price.insert(0, animal["GIA TIEN"])

ttk.Label(window, text="TEN").pack()
entry_name = ttk.Entry(window)
entry_name.pack()

ttk.Label(window, text="MOI TRUONG SONG").pack()
entry_habitat = ttk.Entry(window)
entry_habitat.pack()

ttk.Label(window, text="CAN NANG").pack()
entry_weight = ttk.Entry(window)
entry_weight.pack()

ttk.Label(window, text="GIA TIEN").pack()
entry_price = ttk.Entry(window)
entry_price.pack()

label_money = ttk.Label(window, text=f"Money = {Money}", font=("Arial", 14))
label_money.pack(pady=10)

ttk.Button(window, text="Buy Animal", command=insert).pack(pady=5)
ttk.Button(window, text="Edit Animal", command=edit).pack(pady=5)
ttk.Button(window, text="Sell Animal", command=delete).pack(pady=5)

listbox = tk.Listbox(window, width=50)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", showinfo)

window.mainloop()