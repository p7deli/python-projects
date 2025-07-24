import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import database

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

FONT_MAIN = ("Arial", 13)
FONT_TITLE = ("Arial", 25, "bold")
width = 470
height = 500


def refresh_list():
    tasks = database.get_all_tasks()
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔️" if task[2] else "❌"
        listbox.insert(tk.END, f"{task[0]}. {task[1]} [{status}]")

def add_task():
    title = entry.get().strip()
    if title:
        database.add_task(title)
        entry.delete(0, ctk.END)
        refresh_list()
    else:
        messagebox.showwarning('خطا', 'عنوان تسک را وارد کنید!')

def delete_task():
    selected = listbox.curselection()
    if selected:
        task_str = listbox.get(selected[0])
        task_id = int(task_str.split('.')[0])
        database.delete_task(task_id)
        refresh_list()
    else:
        messagebox.showwarning('خطا', 'تسکی را انتخاب کنید!')

def toggle_done():
    selected = listbox.curselection()
    if selected:
        task_str = listbox.get(selected[0])
        task_id = int(task_str.split('.')[0])
        tasks = database.get_all_tasks()
        for t in tasks:
            if t[0] == task_id:
                new_status = 0 if t[2] else 1
                database.update_task_status(task_id, new_status)
                break
        refresh_list()
    else:
        messagebox.showwarning('خطا', 'تسکی را انتخاب کنید!')

import os
if not os.path.exists(database.DB_NAME):
    database.create_table()
else:
    try:
        database.get_all_tasks()
    except:
        database.create_table()

root = ctk.CTk()

x = ((root.winfo_screenwidth() // 2) - (width // 2))
y = ((root.winfo_screenheight() // 2) - (height // 2)) - 20

root.title('TODO List')
root.geometry(f'{width}x{height}+{x}+{y}')
root.resizable(False, False)

ctk.CTkLabel(root, text='TODO List', font=FONT_TITLE).pack(pady=(25, 10))

frame = ctk.CTkFrame(root)
frame.pack(pady=10)

entry = ctk.CTkEntry(frame, width=260, font=FONT_MAIN, placeholder_text="New task ...")
entry.pack(side="left", padx=8)

add_btn = ctk.CTkButton(frame, text='add task', command=add_task, font=FONT_MAIN, width=100)
add_btn.pack(side="left")

list_frame = ctk.CTkFrame(root)
list_frame.pack(pady=10, padx=10)

# استفاده از tk.Listbox برای انتخاب و اسکرول
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(list_frame, width=50, height=15, font=FONT_MAIN, bg="#f5f6fa", fg="#2d3436", selectbackground="#dfe6e9", selectforeground="#0984e3", yscrollcommand=scrollbar.set, relief='solid', borderwidth=1)
listbox.pack(side="left")
scrollbar.config(command=listbox.yview)

btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=15)

delete_btn = ctk.CTkButton(btn_frame, text='delete task', command=delete_task, font=FONT_MAIN, fg_color="#e17055", hover_color="#d35400", width=120)
delete_btn.pack(side="left", padx=10)

done_btn = ctk.CTkButton(btn_frame, text='change status', command=toggle_done, font=FONT_MAIN, width=160)
done_btn.pack(side="left", padx=10)

refresh_list()

root.mainloop() 