import json
import os
import fnmatch
import re

import ttkbootstrap as tk
from tkinter import messagebox

################################################################################################################
saved = True
student_list = dict()
dshs_list = dict()

name_limit = 1000
class_limit = 100

os.makedirs("data", exist_ok=True)
################################################################################################################
def process_string2(string, off):
    if not string: return
    global student_list
    attributes = dict()
    attribute, _, n, bracket = "", 0, len(string), False
    names = set()
    scores = set()
    classes = set()
    while _<n:
        attribute = ""
        while _<n and string[_] == " ": _ += 1
        while _<n and string[_] != ":":
            if string[_].isalpha():
                attribute += string[_]
                _ += 1
            else:
                messagebox.showerror("", f"❗Error❗\n{_+off}: Thuộc tính chỉ chứa chữ (name, score, class)")
                return {"ERROR": True}
        _ += 1
        if attribute == "name":
            if _<n and string[_] == "[":
                bracket = True
                _ += 1
                temp = ""
                while _<n and string[_] != "]":
                    if string[_].isalpha() or string[_] == "_" or string[_] == "*": temp += string[_]
                    elif string[_] == " ":
                        temp = " ".join((" ".join(temp.split("_"))).split())
                        if temp: names.add(temp)
                    else:
                        messagebox.showerror("", f"❗Error❗\n{_+off}: Tên học sinh chỉ chứa chữ, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                    if _<n and string[_] == "]": bracket = False
                _ += 1
                if bracket:
                    messagebox.showerror("", f"❗Error❗\n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                    return {"ERROR": True}
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp: names.add(temp)
            else:
                temp = ""
                while _<n and string[_] != " ":
                    if string[_].isalpha() or string[_] == "_" or string[_] == "*": temp += string[_]
                    else:
                        messagebox.showerror("", f"❗Error❗\n{_+off}: Tên học sinh chỉ chứa chữ, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp: names.add(temp)
        elif attribute == "score":
            compare = "="
            if _ < n and string[_] == "[":
                bracket = True
                _ += 1
                temp = ""
                while _ < n and string[_] != "]":
                    if string[_] == ">":
                        if compare == "=" and not temp: compare = ">"
                        else:
                            messagebox.showerror("", f"❗Error❗\n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                            return {"ERROR": True}
                    elif string[_] == "<":
                        if compare == "=" and not temp: compare = "<"
                        else:
                            messagebox.showerror("", f"❗Error❗\n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                            return {"ERROR": True}
                    elif string[_].isdigit() or string[_] == "." or string[_] == "*" or string[_] == "#":
                        temp += string[_]
                    elif string[_] == " ":
                        if temp.count("*"):
                            scores.add((None, compare))
                            compare = "="
                            temp = ""
                        else:
                            try:
                                score = float(temp)
                                scores.add((score, compare))
                                compare = "="
                                temp = ""
                            except ValueError:
                                messagebox.showerror("", f"❗Error❗\n{_ + off}: Điểm số là số thực (VD: 3, 6.7)")
                                return {"ERROR": True}
                    else:
                        messagebox.showerror("", f"❗Error❗\n{_ + off}: Điểm số là số thực (VD: 3, 6.7)")
                        return {"ERROR": True}
                    _ += 1
                    if _ < n and string[_] == "]": bracket = False
                if bracket:
                    messagebox.showerror("", f"❗Error❗\n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                    return {"ERROR": True}
                if temp.count("#"):
                    scores.add((None, compare))
                else:
                    try:
                        score = float(temp)
                        scores.add((score, compare))
                    except ValueError:
                        messagebox.showerror("", f"❗Error❗\n{_ + off}: Điểm số là số thực (VD: 3, 6.7)")
                        return {"ERROR": True}
            else:
                temp = ""
                while _ < n and string[_] != " ":
                    if string[_] == ">":
                        if compare == "=" and not temp: compare = ">"
                        else:
                            messagebox.showerror("", f"❗Error❗\n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                            return {"ERROR": True}
                    elif string[_] == "<":
                        if compare == "=" and not temp: compare = "<"
                        else:
                            messagebox.showerror("", f"❗Error❗\n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                            return {"ERROR": True}
                    elif string[_].isdigit() or string[_] == "." or string[_] == "*" or string[_] == "#":
                        temp += string[_]
                    else:
                        messagebox.showerror("", f"❗Error❗\n{_ + off}: Điểm số là số thực (VD: 3, 6.7)")
                        return {"ERROR": True}
                    _ += 1
                if temp.count("#"):
                    scores.add((None, compare))
                else:
                    try:
                        score = float(temp)
                        scores.add((score, compare))
                    except ValueError:
                        messagebox.showerror("", f"❗Error❗\n{_ + off}: Điểm số là số thực (VD: 3, 6.7)")
                        return {"ERROR": True}
        elif attribute == "class":
            if _ < n and string[_] == "[":
                bracket = True
                _ += 1
                temp = ""
                while _ < n and string[_] != "]":
                    if string[_].isalpha() or string[_].isdigit() or string[_] == "_" or string[_] == "*" or string[_] == "#":
                        temp += string[_]
                    elif string[_] == " ":
                        temp = " ".join((" ".join(temp.split("_"))).split())
                        if temp: classes.add(temp)
                    else:
                        messagebox.showerror("", f"❗Error❗\n{_ + off}: Tên lớp học chỉ chứa chữ, số, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                    if _ < n and string[_] == "]": bracket = False
                _ += 1
                if bracket:
                    messagebox.showerror("", f"❗Error❗\n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                    return {"ERROR": True}
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp.count("#"): temp = "#"
                if temp: classes.add(temp)
            else:
                temp = ""
                while _ < n and string[_] != " ":
                    if string[_].isalpha() or string[_].isdigit() or string[_] == "_" or string[_] == "*" or string[_] == "#":
                        temp += string[_]
                    else:
                        messagebox.showerror("", f"❗Error❗\n{_ + off}: Tên lớp học chỉ chứa chữ, số, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp.count("#"): temp = "#"
                if temp: classes.add(temp)
        else:
            messagebox.showerror("", f"❗Error❗{_-len(attribute)-1+off}-{_-2+off}: Các thuộc tính hợp lệ: name, score, class")
            return {"ERROR": True}
        _ += 1
    if names: attributes["names"] = names
    if scores: attributes["scores"] = scores
    if classes: attributes["classes"] = classes
    return attributes

################################################################################################################
def process_string1(string, off):
    if not string: return
    global student_list
    attributes = dict()
    attribute, _, n, bracket = "", 0, len(string), False
    names = set()
    while _<n:
        attribute = ""
        while _<n and string[_] == " ": _ += 1
        while _<n and string[_] != ":":
            if string[_].isalpha():
                attribute += string[_]
                _ += 1
            else:
                messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Thuộc tính chỉ chứa chữ (name, class)")
                return {"ERROR": True}
        _ += 1
        if attribute == "name":
            if _<n and string[_] == "[":
                bracket = True
                _ += 1
                temp = ""
                while _<n and string[_] != "]":
                    if string[_].isalpha() or string[_] == "_": temp += string[_]
                    elif string[_] == " ":
                        temp = " ".join((" ".join(temp.split("_"))).split())
                        if temp:
                            if len(temp) <= name_limit: names.add(temp)
                            else:
                                messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Độ dài tên học sinh tối đa là {name_limit} chữ")
                                return {"ERROR": True}
                        temp = ""
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Tên học sinh chỉ chứa chữ, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                    if _<n and string[_] == "]": bracket = False
                if bracket:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                    return {"ERROR": True}
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp:
                    if len(temp) <= name_limit: names.add(temp)
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Độ dài tên học sinh tối đa là {name_limit} chữ")
                        return {"ERROR": True}
            else:
                temp = ""
                while _<n and string[_] != " ":
                    if string[_].isalpha() or string[_] == "_": temp += string[_]
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Tên học sinh chỉ chứa chữ, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp:
                    if len(temp) <= name_limit: names.add(temp)
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Độ dài tên học sinh tối đa là {name_limit} chữ")
                        return {"ERROR": True}
        elif attribute == "class":
            temp = ""
            while _ < n and string[_] != " ":
                if string[_].isalpha() or string[_].isdigit() or string[_] == "_" or string[_]=="#":
                    temp += string[_]
                else:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Tên lớp học chỉ chứa chữ, số, dấu cách thay bằng _")
                    return {"ERROR": True}
                _ += 1
            temp = " ".join((" ".join(temp.split("_"))).split())
            if temp:
                if len(temp) <= class_limit:
                    if temp.count("#"): temp = "#"
                    if "class" in attributes and attributes["class"] != temp:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Tên lớp học có nhiều hơn 1 giá trị ({attributes["class"]} và {temp})")
                        return {"ERROR": True}
                    attributes["class"] = temp
                else:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Độ dài tên lớp học tối đa là {class_limit} chữ")
                    return {"ERROR": True}
        else:
            messagebox.showwarning("", f"⚠️Warning⚠️: {_-len(attribute)-1+off}-{_-2+off}: Các thuộc tính hợp lệ: name, class")
            return {"ERROR": True}
        _ += 1
    attributes["names"] = names
    if attributes["names"]: return attributes
    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Phải có thuộc tính tên học sinh")
    return {"ERROR": True}

################################################################################################################
def process_string(string, off):
    if not string: return
    global student_list
    attributes = dict()
    attribute, _, n, bracket = "", 0, len(string), False
    names = set()
    while _<n:
        attribute = ""
        while _<n and string[_] == " ": _ += 1
        while _<n and string[_] != ":":
            if string[_].isalpha():
                attribute += string[_]
                _ += 1
            else:
                messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Thuộc tính chỉ chứa chữ (name, score, class)")
                return {"ERROR": True}
        _ += 1
        if attribute == "name":
            if _<n and string[_] == "[":
                bracket = True
                _ += 1
                temp = ""
                while _<n and string[_] != "]":
                    if string[_].isalpha() or string[_] == "_": temp += string[_]
                    elif string[_] == " ":
                        temp = " ".join((" ".join(temp.split("_"))).split())
                        if temp:
                            if len(temp) <= name_limit: names.add(temp)
                            else:
                                messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Độ dài tên học sinh tối đa là {name_limit} chữ")
                                return {"ERROR": True}
                        temp = ""
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Tên học sinh chỉ chứa chữ, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                    if _<n and string[_] == "]": bracket = False
                if bracket:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                    return {"ERROR": True}
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp:
                    if len(temp) <= name_limit: names.add(temp)
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Độ dài tên học sinh tối đa là {name_limit} chữ")
                        return {"ERROR": True}
            else:
                temp = ""
                while _<n and string[_] != " ":
                    if string[_].isalpha() or string[_] == "_": temp += string[_]
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_+off}: Tên học sinh chỉ chứa chữ, dấu cách thay bằng _")
                        return {"ERROR": True}
                    _ += 1
                temp = " ".join((" ".join(temp.split("_"))).split())
                if temp:
                    if len(temp) <= name_limit: names.add(temp)
                    else:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Độ dài tên học sinh tối đa là {name_limit} chữ")
                        return {"ERROR": True}
        elif attribute == "score":
            temp = ""
            while _ < n and string[_] != " ":
                if string[_].isdigit() or string[_] == "." or string[_] == "#":
                    temp += string[_]
                else:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Điểm số là số thực (VD: 3, 6.7)")
                    return {"ERROR": True}
                _ += 1
            if temp.count("#"):
                score = None
                if "score" in attributes and attributes["score"] != score:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Điểm số có nhiều hơn 1 giá trị ({"" if attributes["score"] == None else attributes["score"]} và {"" if score == None else score})")
                    return {"ERROR": True}
                attributes["score"] = score
            else:
                try:
                    score = float(temp)
                    if "score" in attributes and attributes["score"] != score:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Điểm số có nhiều hơn 1 giá trị ({"" if attributes["score"] == None else attributes["score"]} và {"" if score == None else score})")
                        return {"ERROR": True}
                    attributes["score"] = score
                except ValueError:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Điểm số là số thực (VD: 3, 6.7)")
                    return {"ERROR": True}
        elif attribute == "class":
            temp = ""
            while _ < n and string[_] != " ":
                if string[_].isalpha() or string[_].isdigit() or string[_] == "_" or string[_] == "#":
                    temp += string[_]
                else:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Tên lớp học chỉ chứa chữ, số, dấu cách thay bằng _")
                    return {"ERROR": True}
                _ += 1
            temp = " ".join((" ".join(temp.split("_"))).split())
            if temp:
                if temp.count("#"): temp = "#"
                if len(temp) <= class_limit:
                    if "class" in attributes and attributes["class"] != temp:
                        messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Tên lớp học có nhiều hơn 1 giá trị ({attributes["class"]} và {temp})")
                        return {"ERROR": True}
                    attributes["class"] = temp
                else:
                    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Độ dài tên lớp học tối đa là {class_limit} chữ")
                    return {"ERROR": True}
        else:
            messagebox.showwarning("", f"⚠️Warning⚠️: {_-len(attribute)-1+off}-{_-2+off}: Các thuộc tính hợp lệ: name, score, class")
            return {"ERROR": True}
        _ += 1
    attributes["names"] = names
    if attributes["names"]: return attributes
    messagebox.showwarning("", f"⚠️Warning⚠️: \n{_ + off}: Phải có thuộc tính tên học sinh")
    return {"ERROR": True}

################################################################################################################
def file_functions(command_line):
    global student_list, saved
    strings = command_line.split()
    try:
        action = strings[0]
        if action.isalpha() or action.count('_') or action.isdigit():
            if action == "create":
                try:
                    file = strings[1]
                    if file.isalpha() or file.count("_") or file.isdigit():
                        if len(strings)>2:
                            messagebox.showwarning("", "⚠️Warning⚠️: Kiểm tra lại tên file (không ký tự đặc biệt, dấu cách thay bằng _)")
                            return
                        if os.path.exists(f"data/{file}.json"):
                            overwrite = messagebox.askyesno(f"{file} đã tồn tại", "Bạn có muốn ghi đè không?")
                            if overwrite: open(f"data/{file}.json", "w").close()
                            return
                        confirm = messagebox.askyesno("", f"Bạn có muốn tạo {file} không?")
                        if confirm: open(f"data/{file}.json", "w").close()
                    else: messagebox.showerror("", "❗Error❗\nTên file PHẢI là chuỗi KHÔNG ký tự đặc biệt")
                except IndexError: messagebox.showwarning("", "⚠️Warning⚠️: Thiếu thông tin file cần thực hiện hành động")
            elif action == "delete":
                try:
                    file = strings[1]
                    if file.isalpha() or file.count("_") or file.isdigit():
                        if len(strings)>2:
                            messagebox.showwarning("", "⚠️Warning⚠️: Kiểm tra lại tên file (không ký tự đặc biệt, dấu cách thay bằng _)")
                            return
                        if os.path.exists(f"data/{file}.json"):
                            confirm = messagebox.askyesno("", f"{file} sẽ bị xoá vĩnh viễn. Bạn có muốn tiếp tục không?")
                            if confirm: os.remove(f"data/{file}.json")
                        else: messagebox.showwarning("", f"⚠️Warning⚠️: {file} không tồn tại")
                    else: messagebox.showerror("", "❗Error❗\nTên file PHẢI là chuỗi KHÔNG ký tự đặc biệt")
                except IndexError: messagebox.showwarning("", "⚠️Warning⚠️: Thiếu thông tin file cần thực hiện hành động")
            elif action == "load":
                try:
                    file = strings[1]
                    if file.isalpha() or file.count("_") or file.isdigit():
                        if len(strings)>2:
                            messagebox.showwarning("", "⚠️Warning⚠️: Kiểm tra lại tên file (không ký tự đặc biệt, dấu cách thay bằng _)")
                            return
                        try:
                            with open(f"data/{file}.json", "r", encoding="utf-8") as f:
                                confirm = messagebox.askyesno("", f"Bạn có muốn tải dữ liệu từ {file} không? Các dữ liệu chưa lưu hiện tại có thể sẽ mất")
                                if confirm: student_list = json.load(f)
                                #for (name, score) in student_list.items(): print(name, score)
                        except FileNotFoundError: messagebox.showerror("", f"❗Error❗\nKhông tìm thấy {file}. Hãy kiểm tra lại tên file")
                        except json.JSONDecodeError: student_list = {}
                    else: messagebox.showerror("", "❗Error❗\nTên file PHẢI là chuỗi KHÔNG ký tự đặc biệt")
                except IndexError: messagebox.showwarning("", "⚠️Warning⚠️: Thiếu thông tin file cần thực hiện hành động")
            elif action == "save":
                try:
                    file = strings[1]
                    if file.isalpha() or file.count("_") or file.isdigit():
                        if len(strings)>2:
                            messagebox.showwarning("", "⚠️Warning⚠️: Kiểm tra lại tên file (không ký tự đặc biệt, dấu cách thay bằng _)")
                            return
                        if os.path.exists(f"data/{file}.json"):
                            confirm = messagebox.askyesno("", f"Bạn có chắc chắn muốn lưu vào {file} không?")
                            if not confirm: return
                            with open(f"data/{file}.json", "w", encoding="utf-8") as f:
                                json.dump(student_list, f, ensure_ascii=False, indent=4)
                                saved = True
                        else: messagebox.showerror("", f"❗Error❗\nKhông tìm thấy {file}. Hãy kiểm tra lại tên file")
                    else: messagebox.showerror("","❗Error❗\nTên file PHẢI là chuỗi KHÔNG ký tự đặc biệt")
                except IndexError: messagebox.showwarning("", "⚠️Warning⚠️: Thiếu thông tin file cần thực hiện hành động")
            else: messagebox.showwarning("", "⚠️Warning⚠️: Các hành động hợp lệ: create, delete, load, save")
        else: messagebox.showerror("", "❗Error❗\nHành động PHẢI là chuỗi KHÔNG ký tự đặc biệt (create, delete, load, save)")
    except IndexError: messagebox.showwarning("", "⚠️Warning⚠️: Thiếu hành động (create, delete, load, save)")

################################################################################################################
def student_functions(command_line):
    global student_list, saved
    action, _, cnt = "", 0, 0
    n = len(command_line)
    while _<n and command_line[_] == " ": _ += 1
    while _<n and command_line[_] != " ":
        action += command_line[_]
        _ += 1
    if action:
        if not (action.isalpha() or action.count('_') or action.isdigit()):
            messagebox.showerror("", "❗Error❗\nHành động PHẢI là chuỗi KHÔNG ký tự đặc biệt (create, edit, delete)")
            return
        bracket, temp, pos = False, "", 0
        temp_list = dict()
        warning_list = set()
        while _<n and command_line[_] == " ": _ += 1
        if action == "create":
            while _ < n:
                if command_line[_] == "{":
                    if bracket:
                        messagebox.showerror("", f"❗Error❗\n{_+2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                        return
                    pos = _+3
                    bracket = True
                elif command_line[_] == "}":
                    if not bracket:
                        messagebox.showerror("", f"❗Error❗\n{_+2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                        return
                    attributes = process_string(temp, pos)
                    if not "ERROR" in attributes:
                        score = attributes["score"] if "score" in attributes else None
                        student_class = attributes["class"] if "class" in attributes else "#"
                        for name in attributes["names"]:
                            key = f"{student_class}-{name}"
                            if key in student_list:
                                if student_list[key]["score"] != score: warning_list.add(key)
                            elif key in temp_list:
                                if temp_list[key]["score"] != score:
                                    messagebox.showerror("", f"❗Error❗: Thông tin {name} lớp {student_class} không khớp ({temp_list[key]} và {score})")
                                    return
                            else:
                                temp_list[key] = dict()
                                temp_list[key]["score"] = score
                    temp = ""
                    bracket = False
                else:
                    c = command_line[_]
                    if bracket:
                        if c.isalpha() or c.isdigit() or c == "_" or c == ":" or c == "[" or c == "]" or c == " " or c == "." or c == "#":
                            temp += c
                        else:
                            messagebox.showerror("", f"❗Error❗\n{_+2}: Câu lệnh chứa ký tự đặc biệt không hợp lệ")
                            return
                    elif c != " ":
                        messagebox.showerror("", f"❗Error❗\n{_+2}: Câu lệnh chứa ký tự kỳ lạ")
                        return
                _ += 1
            if bracket:
                messagebox.showerror("", f"❗Error❗\n{_ + 2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                return
            for key, attributes in temp_list.items():
                student_list[key] = dict()
                student_list[key]["score"] = attributes["score"]
            if warning_list: messagebox.showwarning("", f"⚠️Warning⚠️: {len(warning_list)} học sinh đã tồn tại")
            saved = False
        elif action == "edit":
            while _ < n:
                if command_line[_] == "{":
                    if bracket:
                        messagebox.showerror("", f"❗Error❗\n{_+2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                        return
                    pos = _ + 3
                    bracket = True
                elif command_line[_] == "}":
                    if not bracket:
                        messagebox.showerror("", f"❗Error❗\n{_+2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                        return
                    attributes = process_string(temp, pos)
                    if not "ERROR" in attributes:
                        score = attributes["score"] if "score" in attributes else None
                        student_class = attributes["class"] if "class" in attributes else "#"
                        for name in attributes["names"]:
                            key = f"{student_class}-{name}"
                            if key not in student_list: warning_list.add(key)
                            elif key in temp_list:
                                if temp_list[key]["score"] != score:
                                    messagebox.showerror("", f"❗Error❗: Thông tin {name} lớp {student_class} không khớp ({temp_list[key]} và {score})")
                                    return
                            else:
                                temp_list[key] = dict()
                                temp_list[key]["score"] = score
                    temp = ""
                    bracket = False
                else:
                    c = command_line[_]
                    if bracket:
                        if c.isalpha() or c.isdigit() or c == "_" or c == ":" or c == "[" or c == "]" or c == " " or c == "." or c == "#":
                            temp += c
                        else:
                            messagebox.showerror("", f"❗Error❗\n{_ + 2}: Câu lệnh chứa ký tự đặc biệt không hợp lệ")
                            return
                    elif c != " ":
                        messagebox.showerror("", f"❗Error❗\n{_ + 2}: Câu lệnh chứa ký tự kỳ lạ")
                        return
                _ += 1
            if bracket:
                messagebox.showerror("", f"❗Error❗\n{_ + 2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                return
            for key, attributes in temp_list.items():
                student_list[key]["score"] = attributes["score"]
            if warning_list: messagebox.showwarning("", f"⚠️Warning⚠️: {len(warning_list)} học sinh không tồn tại")
            saved = False
        elif action == "delete":
            delete_list, student_excess_list = set(), set()
            while _ < n:
                if command_line[_] == "{":
                    if bracket:
                        messagebox.showerror("", f"❗Error❗\n{_ + 2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                        return
                    pos = _ + 3
                    bracket = True
                elif command_line[_] == "}":
                    if not bracket:
                        messagebox.showerror("", f"❗Error❗\n{_ + 2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                        return
                    attributes = process_string1(temp, pos)
                    if not "ERROR" in attributes:
                        student_class = attributes["class"] if "class" in attributes else "#"
                        for name in attributes["names"]:
                            key = f"{student_class}-{name}"
                            if key not in student_list:
                                warning_list.add(key)
                                continue
                            if len(name)>name_limit or (student_class != None and len(student_class)>class_limit):
                                student_excess_list.add(key)
                                continue
                            delete_list.add(key)
                    temp = ""
                    bracket = False
                else:
                    c = command_line[_]
                    if bracket:
                        if c.isalpha() or c.isdigit() or c == "_" or c == ":" or c == "[" or c == "]" or c == " " or c == "." or c == "#":
                            temp += c
                        else:
                            messagebox.showerror("", f"❗Error❗\n{_ + 2}: Câu lệnh chứa ký tự đặc biệt không hợp lệ")
                            return
                    elif c != " ":
                        messagebox.showerror("", f"❗Error❗\n{_ + 2}: Câu lệnh chứa ký tự kỳ lạ")
                        return
                _ += 1
            if bracket:
                messagebox.showerror("", f"❗Error❗\n{_ + 2}: Lỗi cú pháp. Vui lòng kiểm tra lại cú pháp")
                return
            for key in delete_list: student_list.pop(key, None)
            if warning_list: messagebox.showwarning("", f"⚠️Warning⚠️: {len(warning_list)} học sinh không tồn tại")
            if student_excess_list: messagebox.showwarning("", f"⚠️Warning⚠️: {len(student_excess_list)} học sinh có thông tin vượt quá giới hạn")
            saved = False
        else:
            messagebox.showwarning("", "⚠️Warning⚠️: Các hành động hợp lệ: create, edit, delete")
            return
    else: messagebox.showwarning("", "⚠️Warning⚠️: Thiếu hành động (create, edit, delete)")

################################################################################################################
def list_functions(command_line):
    global student_list, dshs_list
    action, _, cnt = "", 0, 0
    n = len(command_line)
    while _<n and command_line[_] == " ": _ += 1
    while _<n and command_line[_] != " ":
        action += command_line[_]
        _ += 1
    if action:
        if not (action.isalpha() or action.count('_') or action.isdigit()):
            messagebox.showerror("", "❗Error❗\nHành động PHẢI là chuỗi KHÔNG ký tự đặc biệt (show, hide)")
            return
        while _<n and command_line[_] == " ": _ += 1
        if action == "show":
            rules = process_string2(command_line[_:], _+2)
            if rules == None: rules = dict()
            '''print(*rules["names"])
            print(*rules["scores"])'''
            if "ERROR" in rules: return
            show_list = student_list
            if "names" in rules:
                temp_list = dict()
                regex_str = "|".join(fnmatch.translate(p) for p in rules["names"])
                regex_obj = re.compile(regex_str)
                for key, data in show_list.items():
                    name = key.split("-")[1]
                    if regex_obj.match(name): temp_list[key] = data
                show_list = temp_list
            if "scores" in rules:
                temp_list = dict()
                for score in rules["scores"]:
                    for key, data in show_list.items():
                        student_score = data["score"]
                        if student_score == None:
                            if score[0] == None: temp_list[key] = data
                        elif score[1]=="=" and student_score==score[0]: temp_list[key] = data
                        elif score[1]==">" and student_score>score[0]: temp_list[key] = data
                        elif score[1]=="<" and student_score<score[0]: temp_list[key] = data
                show_list = temp_list
            if "classes" in rules:
                temp_list = dict()
                allow_none = any(p == "#" for p in rules["classes"])
                regex_str = "|".join(fnmatch.translate(p) for p in rules["classes"] if set(p) != {"*"})
                regex_obj = re.compile(regex_str)
                for key, data in show_list.items():
                    student_class = key.split("-")[0]
                    if student_class == "#" and allow_none: temp_list[key] = data
                    elif regex_obj.match(student_class): temp_list[key] = data
                show_list = temp_list
            for key, data in show_list.items(): dshs_list[key] = data
            delete_list = set()
            for key in dshs_list:
                if key not in student_list: delete_list.add(key)
            for key in delete_list: dshs_list.pop(key, None)
            for row in dshs.get_children(): dshs.delete(row)
            dshs.tag_configure("evenrow", background="#1F1F1F")
            dshs.tag_configure("oddrow", background="#2F2F2F")
            for i, (key, data) in enumerate(dshs_list.items()):
                tag = "oddrow" if i&1 else "evenrow"
                temp = key.split("-")
                name, student_class = temp[1], temp[0]
                dshs.insert("", "end", values=("" if student_class == "#" else student_class, name, "" if data["score"] == None else data["score"]), tags=(tag,))
            view_frame.pack(side="top", fill="both", expand=True)
        elif action == "hide":
            rules = process_string2(command_line[_:], _+2)
            if rules == None: rules = dict()
            '''print(*rules["names"])
            print(*rules["scores"])
            print(*rules["warnings"])'''
            if "ERROR" in rules: return
            hide_list = student_list
            if "names" in rules:
                temp_list = dict()
                regex_str = "|".join(fnmatch.translate(p) for p in rules["names"])
                regex_obj = re.compile(regex_str)
                for key, data in hide_list.items():
                    name = key.split("-")[1]
                    if regex_obj.match(name): temp_list[key] = data
                hide_list = temp_list
            if "scores" in rules:
                temp_list = dict()
                for score in rules["scores"]:
                    for key, data in hide_list.items():
                        student_score = data["score"]
                        if student_score == None:
                            if score[0] == None: temp_list[key] = data
                        elif score[1]=="=" and student_score==score[0]: temp_list[key] = data
                        elif score[1]==">" and student_score>score[0]: temp_list[key] = data
                        elif score[1]=="<" and student_score<score[0]: temp_list[key] = data
                hide_list = temp_list
            if "classes" in rules:
                temp_list = dict()
                allow_none = any(p == "#" for p in rules["classes"])
                regex_str = "|".join(fnmatch.translate(p) for p in rules["classes"] if set(p) != {"*"})
                regex_obj = re.compile(regex_str)
                for key, data in hide_list.items():
                    student_class = key.split("-")[0]
                    if student_class == "#" and allow_none: temp_list[key] = data
                    elif regex_obj.match(student_class): temp_list[key] = data
                hide_list = temp_list
            for key in hide_list: dshs_list.pop(key, None)
            delete_list = set()
            for key in dshs_list:
                if key not in student_list: delete_list.add(key)
            for key in delete_list: dshs_list.pop(key, None)
            for row in dshs.get_children(): dshs.delete(row)
            dshs.tag_configure("evenrow", background="#1F1F1F")
            dshs.tag_configure("oddrow", background="#2F2F2F")
            for i, (key, data) in enumerate(dshs_list.items()):
                tag = "oddrow" if i & 1 else "evenrow"
                temp = key.split("-")
                name, student_class = temp[1], temp[0]
                dshs.insert("", "end", values=("" if student_class == "#" else student_class, name, "" if data["score"] == None else data["score"]), tags=(tag,))
            view_frame.pack(side="top", fill="both", expand=True)
        else:
            messagebox.showwarning("", "⚠️Warning⚠️: Các hành động hợp lệ: show, hide")
            return
    else: messagebox.showwarning("", "⚠️Warning⚠️: Thiếu hành động (show, hide)")

################################################################################################################
def show_guide():
    messagebox.showinfo("Information",
"Danh sách cú pháp các câu lệnh:\n"
        "0 create <file name>\n"
        "0 delete <file name>\n"
        "0 save <file name>\n"
        "0 load <file name>\n\n"
        "1 create {name:<hs> name:[<hs> <hs> ...] score:<điểm> class:<lớp> ...} ...\n"
        "1 edit {name:<hs> name:[<hs> <hs> ...] score:<điểm> class:<lớp> ...} ...\n"
        "1 delete <hs> <hs> ...\n\n"
        "2 show name:<filter> name:[<filter> <filter> ...] score:<filter> score:[<filter> <filter> ...] class:<filter> class:[<filter> <filter> ...] ...\n"
        "2 hide name:<filter> name:[<filter> <filter> ...] score:<filter> score:[<filter> <filter> ...] class:<filter> class:[<filter> <filter> ...] ...\n\n"
        "Để chạy các lệnh, bạn chỉ cần nhập vào entry và ấn enter\n"
        "⚠️LƯU Ý: cần phải nhập ĐÚNG CÚ PHÁP hoặc chương trình sẽ hiển thị thông tin về lỗi. Nhập đúng cú pháp nhưng input không hợp lệ cũng tương tự⚠️\n"
        "Tips: trước khi chạy entry nên copy lại đoạn lệnh để phòng trường hợp code có vấn đề vì sau mỗi lần enter entry sẽ xoá hết đoạn lệnh")

################################################################################################################
def run_entry(event):
    command_line = str_var.get().strip()
    if not command_line: return
    func, _, n = "", 0, len(command_line)
    while _<n and command_line[_] != " ":
        func += command_line[_]
        _ += 1
    str_var.set("")
    if not func.isdigit():
        messagebox.showerror("", "❗ValueError❗\nGiá trị đầu tiên PHẢI là số nguyên (0-5)")
        return
    func = int(func)
    if func == 0: file_functions(command_line[_:])
    elif func == 1: student_functions(command_line[_:])
    elif func == 2: list_functions(command_line[_:])

################################################################################################################
window = tk.Window(
    title="Student Manager (real)",
    size=(640, 640),
    themename="darkly"
)

dshs_style = tk.Style()
dshs_style.theme_use("darkly")
dshs_style.configure("Treeview",
                background="#1F1F1F",
                foreground="#FFFFFF",
                rowheight=25,
                bordercolor="#FFFFFF",
                borderwidth=2,
                relief="solid")
dshs_style.configure("Treeview.Heading",
                background="#4F4F4F",
                foreground="#FFFFFF",
                relief="solid",
                borderwidth=2)
dshs_style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

main_frame = tk.Frame(window)
main_frame.pack(side="top", fill="both", expand=True)

interact_frame = tk.Frame(main_frame)
interact_frame.pack(side="top", fill="x")
view_frame = tk.Frame(main_frame)
#view_frame.pack(side="top", fill="both", expand=True)

info_button = tk.Button(interact_frame, text='?', width=2, command=show_guide)
info_button.pack(side="left")

str_var = tk.StringVar()
entry = tk.Entry(interact_frame, textvariable=str_var)
entry.bind("<Return>", run_entry)
entry.pack(side="left", fill="x", expand=True)

dshs = tk.Treeview(view_frame, columns=("class", "name", "score"), show="headings")
dshs.heading("class", text="Lớp")
dshs.heading("name", text="Học sinh")
dshs.heading("score", text="Điểm")

scrollbar = tk.Scrollbar(view_frame, orient="vertical", command=dshs.yview)
dshs.configure(yscrollcommand=scrollbar.set)

dshs.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

window.mainloop()