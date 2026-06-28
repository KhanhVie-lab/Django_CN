
import ttkbootstrap as tk
import tkinter as ttk
root = tk.Window(
    title="The First Application",
    size=(800,400),
    themename="yeti"
)
collection = [{"ten": "car", "wheels": 4}]
listbox = ttk.Listbox(root)
listbox.grid(column= 0, row = 0)

def update_listbox():
    listbox.delete(0,"end")
    if len(collection) > 0:
        for item in collection:
            listbox.insert("end",f"{item["ten"]} - {item["wheels"]}")
    else: 
        listbox.delete(0,"end")
update_listbox()
def appendor():
    ans = entry.get()
    answ = ans.split(" ")
    if ans != "" and len(answ) == 2 and type(answ[1]) == int and type(answ[0]) == str:
        collection.append({"ten": answ[0], "wheels": answ[1]})
    elif ans.strip() == "":
        label.config(text = "input something first! type again!")
    elif len(answ) != 2:
        label.config(text = "must be (format: <name> <wheel>)! type again!")
    elif type(answ[1]) != int or type(answ[0]) != str:
        label.config(text = "name must be a text, and wheels must be int! type again!")
    update_listbox()

def destroy():
    global collection
    collection = []
    update_listbox()

def delete():
    global collection
    a = listbox.curselection()
    
    a = a[0]
    print(a)
    print(collection)
    if a > 0:
        del collection[a]
    else:
        collection = []
    update_listbox()
    
def edit():
    global collection
    b = listbox.curselection()
    b = b[0]
    ans = entry.get()
    answ = ans.split(" ")
    collection[b] = {"ten": answ[0], "wheels": answ[1]}
    update_listbox()
    
def insert():
    global collection
    c = listbox.curselection()
    c = c[0]
    ans = entry.get()
    answ = ans.split(" ")
    collection.insert(c+1, {"ten": answ[0], "wheels": answ[1]})
    update_listbox()
    
label = tk.Label(
    root,
    text = "add vehicle: (format: <name> <wheel>)" 
)
label.grid(column = 0, row = 1)
entry = tk.Entry(
    root,
)
entry.grid(column = 0, row = 2)
button = tk.Button(
    root,
    text = "submit",
    command = appendor
)
delbutton = tk.Button(
    root,
    text = "del all",
    command = destroy
)
delselect = tk.Button(
    root,
    text = "delete",
    command = delete
)
editt = tk.Button(
    root,
    text = "edit",
    command = edit
)
innsert = tk.Button(
    root,
    text = "insert",
    command = insert
)

innsert.grid(column = 1, row = 3)
delselect.grid(column = 2, row = 3)
delbutton.grid(column = 3, row = 3)
button.grid(column = 4, row = 3)
editt.grid(column = 5, row = 3)
root.mainloop()



