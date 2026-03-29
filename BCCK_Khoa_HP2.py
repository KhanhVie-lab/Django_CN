import ttkbootstrap as tk
from tkinter import messagebox

app = tk.Window(title="The Quiz Game", themename="solar" \
"", size=(1920,1080))

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)

data = tk.StringVar()

answers = "ABCD"

def check():
    answer = data.get()

    if answer.strip().upper() not in answers:
        messagebox.showerror("Error", "Invalid")
    else: 
        if answer.strip().upper() == "A":
            messagebox.showinfo("Success", "Correct!")
        else:
            messagebox.showerror("Error", "Wrong")

def shutdown():
    shut = messagebox.askokcancel("Exit", "Do you want to exit the program?")
    if shut:
        app.destroy()

# Question
text = tk.Label(
    app,
    text="What is the purpose of pady and padx?",
    font=("Arial", 24),
    anchor="center",
    justify="center"
)

text.grid(row=0, column=0, columnspan=2, pady=20)

# Entry box
entry = tk.Entry(app, textvariable=data)
entry.grid(row=1, column=0, columnspan=2, pady=10)

# Button
button = tk.Button(app, text="Check", command=check)
button.grid(row=2, column=0, pady=10)

button2 = tk.Button(app, text="Shutdown", command=shutdown)
button2.grid(row=2, column=1, pady=10)

textA = tk.Label(app, text="A.To create padding around a widget ", font=("arial", 15))
textA.grid(row=3, column=0, columnspan=2, pady=5)

textB = tk.Label(app, text="B.To move the widget to a desired spot when commanded", font=("arial", 15))
textB.grid(row=4, column=0, columnspan=2, pady=5)

textC = tk.Label(app, text="C.To scale the widget using coordinates",font=("arial", 15))
textC.grid(row=5, column=0, columnspan=2, pady=5)

textD = tk.Label(app, text="D.To make the widget centered",font=("arial", 15))
textD.grid(row=6, column=0, columnspan=2, pady=5)

app.mainloop()