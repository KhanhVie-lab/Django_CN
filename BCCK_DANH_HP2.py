import tkinter as tk
from tkinter import messagebox
import random

# ==========================================================
# 1. DỮ LIỆU CÂU HỎI
# Mỗi câu hỏi gồm:
# (Câu hỏi, [4 đáp án], đáp án đúng)
# ==========================================================
questions = [
    ("Python là gì?", ["Ngôn ngữ lập trình", "Con rắn", "Game", "Phần mềm"], "Ngôn ngữ lập trình"),
    ("2 + 2 = ?", ["3", "4", "5", "6"], "4"),
    ("Màu của lá cây?", ["Đỏ", "Xanh", "Vàng", "Trắng"], "Xanh"),
    ("Thủ đô của Việt Nam?", ["TP.HCM", "Đà Nẵng", "Hà Nội", "Huế"], "Hà Nội"),
]

# Trộn ngẫu nhiên thứ tự câu hỏi mỗi lần chơi
random.shuffle(questions)

# ==========================================================
# 2. BIẾN QUẢN LÝ TRẠNG THÁI GAME
# ==========================================================
q_index = 0       # Vị trí câu hỏi hiện tại
score = 0         # Điểm số
locked = False    # Khóa input khi đã chọn đáp án
time_left = 10    # Thời gian mỗi câu (giây)
timer_id = None   # ID của timer để có thể dừng

# ==========================================================
# 3. TẠO GIAO DIỆN CHÍNH
# ==========================================================
root = tk.Tk()
root.title("Quiz Game Pro")
root.geometry("420x450")
root.config(bg="#11111b")  # Nền tối

# Frame trên cùng chứa timer và tiến trình
top_frame = tk.Frame(root, bg="#11111b")
top_frame.pack(fill="x", pady=15)

# Hiển thị tiến độ (câu số)
progress_label = tk.Label(top_frame, text="", fg="#6c7086", bg="#11111b", font=("Arial", 10))
progress_label.pack(side="right", padx=20)

# Hiển thị thời gian còn lại
timer_label = tk.Label(top_frame, text="", fg="#f9e2af", bg="#11111b", font=("Arial", 10, "bold"))
timer_label.pack(side="left", padx=20)

# Thanh progress (canvas)
canvas = tk.Canvas(root, height=4, bg="#1e1e2e", highlightthickness=0)
canvas.pack(fill="x", padx=30, pady=5)

# Thanh màu thể hiện % hoàn thành
bar = canvas.create_rectangle(0, 0, 0, 4, fill="#89b4fa", outline="")

# Label hiển thị câu hỏi
question_label = tk.Label(
    root,
    text="",
    font=("Arial", 13, "bold"),
    fg="#cad3f5",
    bg="#11111b",
    wraplength=340,     # xuống dòng nếu dài
    justify="center",
    pady=20
)
question_label.pack()

# ==========================================================
# 4. LOGIC GAME
# ==========================================================

# Dừng timer hiện tại (tránh chạy chồng)
def stop_timer():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None


# Xử lý khi người chơi chọn đáp án
def check_answer(idx):
    global score, locked

    # Nếu đã chọn rồi thì không cho bấm nữa
    if locked:
        return

    locked = True
    stop_timer()

    # Lấy đáp án đúng
    correct_ans = questions[q_index][2]

    # Màu hiển thị kết quả
    color_correct = "#2e7d32"
    color_wrong = "#8a2a2a"
    color_black = "#000000"

    # Duyệt từng nút đáp án
    for i, btn in enumerate(buttons):
        btn_text = btn.cget("text")

        # Nếu là đáp án đúng → tô xanh
        if btn_text == correct_ans:
            btn.config(bg=color_correct, fg=color_black)

        # Nếu chọn sai → tô đỏ
        if i == idx and btn_text != correct_ans:
            btn.config(bg=color_wrong, fg=color_black)

    # Nếu chọn đúng → cộng điểm
    if idx is not None and buttons[idx].cget("text") == correct_ans:
        score += 1

    # Sau 1 giây → chuyển câu tiếp theo
    root.after(1000, next_question)


# Countdown thời gian mỗi câu
def countdown():
    global time_left, timer_id

    # Cập nhật UI thời gian
    timer_label.config(text=f"⏱ {time_left}s")

    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, countdown)  # gọi lại sau 1s
    else:
        # Hết giờ → tự động coi như sai
        check_answer(None)


# Load câu hỏi mới lên UI
def load_question():
    global locked, time_left

    locked = False
    time_left = 10

    # Lấy dữ liệu câu hỏi
    q_text, choices, _ = questions[q_index]

    # Trộn thứ tự đáp án
    display_choices = choices.copy()
    random.shuffle(display_choices)

    # Hiển thị câu hỏi
    question_label.config(text=q_text)

    # Hiển thị tiến độ
    progress_label.config(text=f"{q_index+1}/{len(questions)}")

    # Cập nhật thanh progress
    percent = (q_index + 1) / len(questions)
    canvas.coords(bar, 0, 0, 420 * percent, 4)

    # Cập nhật text và style cho các nút
    for i in range(4):
        buttons[i].config(
            text=display_choices[i],
            bg="#a6adc8",
            fg="#000000",
            activebackground="#cdd6f4"
        )

    # Bắt đầu đếm ngược
    countdown()


# Chuyển sang câu tiếp theo
def next_question():
    global q_index

    q_index += 1

    if q_index < len(questions):
        load_question()
    else:
        # Kết thúc game → hiện kết quả
        messagebox.showinfo("Kết quả", f"Xong! Bạn đúng {score}/{len(questions)} câu.")
        root.destroy()


# ==========================================================
# 5. TẠO NÚT ĐÁP ÁN
# ==========================================================
buttons = []

for i in range(4):
    btn = tk.Button(
        root,
        text="",
        font=("Arial", 10, "bold"),
        bg="#a6adc8",
        fg="#000000",
        relief="flat",
        bd=0,
        pady=12,
        activeforeground="#000000",
        cursor="hand2",

        # Khi bấm → gọi check_answer với index của nút
        command=lambda i=i: check_answer(i)
    )

    btn.pack(fill="x", padx=50, pady=6)
    buttons.append(btn)

# Load câu đầu tiên
load_question()

# Chạy app
root.mainloop()