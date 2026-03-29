import ttkbootstrap as tk
from ttkbootstrap.dialogs import Messagebox

app = tk.Window(title="BMI App", themename="morph", size=(300, 250))

height_var = tk.StringVar()
weight_var = tk.StringVar()

label = tk.Label(app, text = "Chiều cao (m)")
label.pack()
entry = tk.Entry(app, textvariable = height_var)
entry.pack()

label1 = tk.Label(app, text = "Cân nặng (kg)")
label1.pack()
entry1 = tk.Entry(app, textvariable = weight_var)
entry1.pack()

def calculate_BMI():
    try:
        h = float(height_var.get())
        w = float(weight_var.get())

        bmi = w / (h * h)
        if bmi < 16:
            result = "Gầy độ III"
            Messagebox.show_warning(f"{bmi:.2f} \n {result}", "Cảnh báo")
        elif bmi < 17:
            result = "Gầy độ II"
            Messagebox.show_warning(f"{bmi:.2f} \n {result}", "Cảnh báo")
        elif bmi < 18.5:
            result = "Gầy độ I"   
            Messagebox.show_warning(f"{bmi:.2f} \n {result}", "Cảnh báo")
        elif bmi < 25:
            result = "Bình thường" 
            Messagebox.show_info(f"{bmi:.2f} \n {result}", "Tốt")
        elif bmi < 30:
            result = "Thừa cân" 
            Messagebox.show_error(f"{bmi:.2f} \n {result}", "Chú ý")
        elif bmi < 35:
            result = "Béo phì độ I" 
            Messagebox.show_error(f"{bmi:.2f} \n {result}", "Nguy hiểm")
        elif bmi < 40:
            result = "Béo phì độ II" 
            Messagebox.show_error(f"{bmi:.2f} \n {result}", "Nguy hiểm")
        else:
            result = "Béo phì độ III" 
            Messagebox.show_error(f"{bmi:.2f} \n {result}", "Rất nguy hiểm")
    except:
        Messagebox.show_error("Nhập sai dữ liệu", "Lỗi")

button = tk.Button(app, text = "Xem kết quả", command = calculate_BMI)
button.pack(pady = 10)

exit_button = tk.Button(app, text = "Thoát", command = app.destroy)
exit_button.pack()

app.mainloop()
