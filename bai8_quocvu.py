import ttkbootstrap as tk
import random as r
root = tk.Window(
    title="The First Application",
    size=(800,400),
    themename="yeti"
)
def hello():
    text =  entry.get()
    
    if len(text)<1 :
        print("you typed nothing")
        buton.config(text = "NOTHING HERE CHUCKLENUTS")  
    elif text == "im gay":
        print("me too bro")
        buton.config(text= "me too bro")
    elif text == "nothing" or text == "NOTHING HERE CHUCKLENUTS":
        print("bro aint slick")
        buton.config(text = "bro aint slick")  
    elif text == "10.5":
        print("nubububububububububububububububiggubububububububububububububububa")
        buton.config(text = "nubububububububububububububububiggububububububububububububububub")  
    else:
        print("you typed","'", text, "'")
        buton.config(text = entry.get())
    entry.delete(0,'end')
    cor = colorroll()
    label.config(background = cor)
style = tk.Style
def colorroll():
    cha = "0123456789ABCDEF"
    color = "#"
    for i in range(6):
        color += r.choice(cha)
    style.configure("Color.TFrame")
    return color

def colorrandom():
    red = r.randint(0,255)
    blue = r.randint(0,255)
    green = r.randint(0,255)
    colour = f"({red},{blue},{green})"
    return colour

#def copy_color():
#    text = text1.cget("text")
#    root.clipboard_clear()
#    root.clipboard_append(text)

def changetheme():
    current = root.style.theme.name
    print(current)
    if current == "solar":
        root.style.theme_use("darkly")
    elif current == "darkly":
        root.style.theme_use("cyborg")
    elif current == "cyborg":
        root.style.theme_use("vapor")
    else:
        root.style.theme_use("solar")
    current = root.style.theme.name
    label.config(text=current)
frame = tk.Frame(root, width=50,height=50, style = "secondary")
label = tk.Label(text = "ai hoi", font = ("Arial", 15, "bold italic underline"), background = colorroll())
label.grid(row=500,column=150)
buton = tk.Button(root,text="hello vro",bootstyle='danger',command=changetheme)
buton.grid(row=200,column=150)
entry = tk.Entry(root)
entry.grid(row=40,column=100,sticky='nsew')
root.columnconfigure(0,weight=3)
root.columnconfigure(1,weight=1)
root.mainloop()
