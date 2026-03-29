#bài báo cáo cuối khoá
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
python_basic_questions = [
    {
        "question": "Python được tạo ra bởi ai?",
        "options": ["Guido van Rossum", "James Gosling", "Dennis Ritchie", "Linus Torvalds"],
        "answer": 0
    },
    {
        "question": "Kiểu dữ liệu để lưu một số nguyên trong Python là gì?",
        "options": ["int", "float", "str", "boolean"],
        "answer": 0
    },
    {
        "question": "Hàm nào dùng để in ra màn hình?",
        "options": ["print()", "input()", "display()", "show()"],
        "answer": 0
    },
    {
        "question": "Toán tử để lấy phần dư trong Python là?",
        "options": ["//", "%", "/", "**"],
        "answer": 1
    },
    {
        "question": "Kiểu dữ liệu để lưu chuỗi?",
        "options": ["string", "char", "str", "text"],
        "answer": 2
    },
    {
        "question": "Lệnh dùng để lấy dữ liệu từ bàn phím?",
        "options": ["keyboard()", "scan()", "input()", "get()"],
        "answer": 2
    },
    {
        "question": "Ký hiệu bắt đầu comment một dòng trong Python?",
        "options": ["//", "#", "/*", "<!--"],
        "answer": 1
    },
    {
        "question": "Len() dùng để làm gì?",
        "options": ["Tính độ dài", "Tính tổng", "Ép kiểu", "In ra màn hình"],
        "answer": 0
    },
    {
        "question": "Trong Python, 2 ** 3 có kết quả là?",
        "options": ["5", "6", "8", "9"],
        "answer": 2
    },
    {
        "question": "Kiểu dữ liệu bool có thể chứa giá trị nào?",
        "options": ["yes/no", "0/1", "true/false", "right/wrong"],
        "answer": 2
    }
]
current_question = 0
score = 0
def load_question():
    """Hiển thị câu hỏi lên giao diện"""
    q = python_basic_questions[current_question]
    question_label.config(text=f"Câu {current_question + 1}: {q['question']}")
    for i, text in enumerate(q["options"]):
        option_buttons[i].config(text=text)
    answer_var.set(-1)
def check_answer():
    global current_question, score
    if answer_var.get() == python_basic_questions[current_question]["answer"]:
        score_label.config(text="Kết quả: Đúng!", bootstyle=SUCCESS)
        score_label.after(1200, lambda: score_label.config(text=""))
        score += 1
    else:
        score_label.config(text="Kết quả: Sai!", bootstyle=DANGER)
        score_label.after(1200, lambda: score_label.config(text=""))
    current_question += 1
    if current_question < len(python_basic_questions):
        load_question()
    else:
        finish_quiz()
def finish_quiz():
    for widget in frame.winfo_children():
        widget.destroy()
    final_text = f"Bạn đã hoàn thành Quiz!\nĐiểm số: {score}/{len(python_basic_questions)}"
    done_label = ttk.Label(frame, text=final_text, font=("Arial", 20))
    done_label.pack(pady=40)
app = ttk.Window(themename="flatly") #Theme color: lumen, darkly, flatly, journal, cosmo, simplex, minty, pulse, sandstone, yeti, cyborg
app.title("Quiz Game")
app.geometry("600x400")
title = ttk.Label(app, text="Chào mừng bạn đến với Quiz Game!", font=("Arial", 22, "bold"), bootstyle=INFO)
title.pack(pady=20)
frame = ttk.Frame(app)
frame.pack(pady=10)
question_label = ttk.Label(frame, text="", font=("Arial", 16))
question_label.pack(pady=10)
answer_var = ttk.IntVar()
option_buttons = []
for i in range(4):
    btn = ttk.Radiobutton(frame, text="", variable=answer_var, value=i, bootstyle="info")
    btn.pack(anchor="w", padx=40, pady=4)
    option_buttons.append(btn)
submit_btn = ttk.Button(app, text="Kiểm tra", bootstyle=PRIMARY, command=check_answer)
submit_btn.pack(pady=10)
score_label = ttk.Label(app, text="", font=("Arial", 14))
score_label.pack()
load_question()
app.mainloop()