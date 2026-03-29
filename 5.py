import tkinter as tk
import random
def random_color():
    
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    root.config(bg=color)
root = tk.Tk()
root.title("Random Color Generator")
root.geometry("300x200")
button = tk.Button(
    root,
    text="Generate",
    font=("Arial", 12, "bold"),
    command=random_color
)
button.pack(expand=True)

root.mainloop()