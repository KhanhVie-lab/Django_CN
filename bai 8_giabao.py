import ttkbootstrap as ttk
app = ttk.Window(themename="vapor",
                title="Demo",
                size=(800,400)) 
app.title("Demo") #Cách 2 của title 
app.geometry("800x400") #Cách 2 của size
def copy_color ():
    text = text1.cget ("text")
    app.clipboard_clear()
    app.clipboard_append (text)
text1 = ttk. Label(app,text="Xin chào!")
text1.pack()
button1 = ttk.Button(app, text="Copy here!", bootstyle="primary", command=copy_color)
button1. pack()
app.mainloop()