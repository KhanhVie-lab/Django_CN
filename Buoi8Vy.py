import ttkbootstrap as ttk
import random as rd

app = ttk.Window(themename="vapor")
app.title("Demo")
app.geometry("800x400") 

def click():
    color = random()
    text.config(text=color)
    style.configure("Color.TFrame", background = color)
    frame.config(style = "Color.TFrame") 

def copy_color():
    textcolor = text.cget("text")
    app.clipboard_clear()
    app.clipboard_append(textcolor)

def random():
    r = rd.randint(0, 255)
    g = rd.randint(0, 255)
    b = rd.randint(0, 255)
    color = f"#{r:02x}{g:02x}{b:02x}"
    return color

style = ttk.Style()
text1 = ttk.Label(app, text="Hi")
text1.pack()
text = ttk.Label(app, text="abc")
text.pack()
frame = ttk.Frame(app, width = 200, height = 200, style = "secondary")
frame.pack_propagate(False)
frame.pack()
button = ttk.Button(frame, text = "Click here!", command = click)
button.pack()
button1 = ttk.Button(app, text="Copy here!", bootstyle="primary", command=copy_color)
button1.pack()

app.mainloop()