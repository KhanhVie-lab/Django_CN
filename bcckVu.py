
import ttkbootstrap as tk
import random as r
from tkinter import messagebox
root = tk.Window(
    title="The First Application",
    size=(1800,400),
    themename="yeti"
)
costate = 0
question = 1
def hello():
    global question
    global correct
    global incorrect
    global costate
    global itq
    text =  entry.get()
    if (text == "2" or text.lower() == "two") and question == 1:
        label.config(text = "correct!")
        costate = 1
        buttoon.config(text = "next question")
        question += 1
        correct += 1
        itq = 0
    elif text.lower() == "length" and question == 2:
        label.config(text = "correct!")
        buttoon.config(text = "next question")
        costate = 1
        question += 1
        correct += 1
        itq = 0
    elif text.lower() == "donald trump" and question == 3:
        label.config(text = "correct!")
        buttoon.config(text = "next question")
        costate = 1
        question += 1
        correct += 1
        itq = 0
    elif text.lower() == "8th mar" and question == 4:
        label.config(text = "correct!")
        buttoon.config(text = "next question")
        costate = 1
        question += 1
        correct += 1
        itq = 0
    elif text.lower() == "true" and question == 5:
        label.config(text = "correct!")
        buttoon.config(text = "FINAL QUESTION?")
        costate = 1
        question += 1
        correct += 1
        itq = 0
    elif (text.lower() == "4" or text.lower() == "four") and question == 6:
        label.config(text = "YOU WIN!!")
        buttoon.config(text = "no more questions")
        costate = 1
        correct += 1
        itq = 0
        label2.config(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}")
    else: 
        if costate == 0 and itq < 5:
            label.config(text = "incorrect!")
            buttoon.config(text = "retry")
            incorrect += 1
            costate = 1
            itq += 1
        elif itq >= 5:
            if question == 1:
                label.config(text = "you answered wrong 5 times this question. the answer was 2. -1 score penalty applied.")
            elif question == 1:
                label.config(text = "you answered wrong 5 times this question. the answer was length. -1 score penalty applied.")
            elif question == 1:
                label.config(text = "you answered wrong 5 times this question. the answer was Donald Trump. -1 score penalty applied.")
            elif question == 1:
                label.config(text = "you answered wrong 5 times this question. the answer was 8th Mar. -1 score penalty applied.")
            elif question == 1:
                label.config(text = "you answered wrong 5 times this question. the answer was True. -1 score penalty applied.")
            buttoon.config(text = "next question")
            correct -= 1
            costate = 1
            question += 1
            itq = 0
    entry.delete(0,'end')
style = tk.Style

def questions():
    global costate
    global itq
    if question == 1:
        label.config(text = "whats 1+1?")
        label2.config(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}")
        costate = 0
    elif question == 2:
        label.config(text = "fill in the blank: the area of a rectangle is width x ___")
        label2.config(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}")
        costate = 0
    elif question == 3:
        label.config(text = "whos USA current president?")
        label2.config(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}")
        costate = 0
    elif question == 4:
        label.config(text = "when is the international women day? (say it like 1st Jan)")
        label2.config(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}")
        costate = 0
    elif question == 5:
        label.config(text = "a rubik's cube has 6 colors, TRUE/FALSE")
        label2.config(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}")
        costate = 0
    elif question == 6:
        label.config(text = "how many legs does a cat has?")
        label2.config(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}")
        costate = 0


#def shutdown():
    #a = messagebox.askyesnocancel("EXIT", "DO YOU WANT TO EXIT?")
    #if a == True:
        #app.destroy
itq = 0
data = tk.StringVar()
#def copy_color():
#    text = text1.cget("text")
#    root.clipboard_clear()
#    root.clipboard_append(text)
correct = 0
incorrect = 0
total = 6
label = tk.Label(text = "whats 1+1?", font = ("Arial", 15, "bold"),)
label.grid(row=5,column=240)
buton = tk.Button(root,text="enter",bootstyle='danger',command=hello)
buton.grid(row=200,column=240)
buttoon = tk.Button(root, text = "next question", command = questions)
buttoon.grid(row=201,column = 240)
label2 = tk.Label(text = f"score: {correct}, incorrect: {incorrect}, questions: {question}/{total}", font = ("Arial", 12, "bold"))
label2.grid(row = 202, column=240)
entry = tk.Entry(root)
entry.grid(row=40,column=240)
root.mainloop()
