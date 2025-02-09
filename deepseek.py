import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import json
import pandas as pd

# قاموس لتخزين البيانات
data_storage = {
    "Dammam": [], "Riyad": [], "West-Tabuk": [], "Almadina": [], "Abha": [],
    "Makka": [], "Taif": [], "Jedda": [], "Center": [], "Distributor": [],
    "Franchise": [], "HeadOffc": []
}

# دالة لحفظ البيانات في ملف JSON
def save_data_to_json(filename="data.json"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_storage, file, indent=4, ensure_ascii=False)
        messagebox.showinfo("تم الحفظ", f"تم حفظ البيانات في الملف {filename}")
    except Exception as error:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ البيانات: {error}")

# دالة لتحميل البيانات من ملف JSON
def load_data_from_json(filename="data.json"):
    global data_storage
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data_storage = json.load(file)
        print(f"تم تحميل البيانات من الملف {filename}")
        return data_storage
    except FileNotFoundError:
        print(f"الملف {filename} غير موجود. سيتم استخدام بيانات افتراضية.")
        return data_storage
    except json.JSONDecodeError:
        print(f"حدث خطأ في قراءة الملف {filename}. سيتم استخدام بيانات افتراضية.")
        return data_storage
    except Exception as error:
        print(f"حدث خطأ أثناء تحميل البيانات: {error}")
        return data_storage

# تحميل البيانات عند بدء التشغيل
load_data_from_json()

# دالة لتوسيط النافذة على الشاشة
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# دالة للتحقق من تسجيل الدخول
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "1" and password == "1":
        #messagebox.showinfo("تم تسجيل الدخول بنجاح", "مرحباً!")
        login_window.destroy()
        open_main_form()
    else:
        messagebox.showerror("خطأ في تسجيل الدخول", "اسم المستخدم أو كلمة المرور غير صحيحة.")

# دالة للانتقال إلى الحقل التالي عند الضغط على Enter
def move_to_next_field(event):
    event.widget.tk_focusNext().focus()

# دالة لفتح نموذج إدخال البيانات
def open_data_entry_form(region_name):
    data_entry_window = tk.Toplevel()
    data_entry_window.title(f"بيانات {region_name}")
    window_width = 400
    window_height = 500
    center_window(data_entry_window, window_width, window_height)
    data_entry_window.resizable(False, False)
    data_entry_window.configure(bg="#2c3e50")
    entry_frame = ttk.Frame(data_entry_window, padding=20, relief="groove", borderwidth=2)
    entry_frame.pack(fill=tk.BOTH, expand=True)

    field_labels = [
        "BR NMB", "Branch name", "DISPLAY", "COMPUTER", "MODEL",
        "GENARATION", "HDD", "RAM", "PRINTER", "printer name"
    ]

    entry_fields = []
    for i, label_text in enumerate(field_labels):
        label = ttk.Label(entry_frame, text=label_text, style="Custom.TLabel")
        label.grid(row=i, column=0, sticky="w", pady=10)

        entry = ttk.Entry(entry_frame, style="Custom.TEntry", justify="right")
        entry.grid(row=i, column=1, pady=10, sticky="ew")
        entry_fields.append(entry)
        entry.bind("<Return>", move_to_next_field)
    data_entry_window.after(100, entry_fields[0].focus_force) #تأخير بسيط ثم تفعيل الفورم

    entry_frame.columnconfigure(1, weight=1)
    
    buttons_frame = ttk.Frame(data_entry_window, padding=10)
    buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # دالة لحفظ البيانات
    def save_entered_data():
        input_data = [entry.get() for entry in entry_fields]
        if all(input_data):  # التحقق من أن جميع الحقول مملوءة
            data_storage[region_name].append(input_data)
            messagebox.showinfo("تم الحفظ", "تم حفظ البيانات بنجاح.")
            save_data_to_json()
            data_entry_window.destroy()
            main_form.deiconify()
            print(data_storage)
        else:
            messagebox.showwarning("تحذير", "يرجى ملء جميع الحقول قبل الحفظ.")



    # دالة للعودة إلى النموذج الرئيسي
    def return_to_main_form():
        data_entry_window.destroy()
        main_form.deiconify()

    save_button = ttk.Button(buttons_frame, text="حفظ", style="Custom.TButton", command=save_entered_data)
    back_button = ttk.Button(buttons_frame, text="العودة", style="Custom.TButton", command=return_to_main_form)

    save_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    back_button.pack(side=tk.RIGHT, padx=10, fill=tk.X, expand=True)

    # ربط حدث الضغط على Enter بزر الحفظ
    data_entry_window.bind("<Return>", lambda event: save_entered_data() if save_button["state"] == tk.NORMAL else None)
# دالة لفتح النموذج الرئيسي
def open_main_form():
    global main_form
    main_form = tk.Tk()
    main_form.title("النموذج الرئيسي")
    window_width = 500
    window_height = 400
    center_window(main_form, window_width, window_height)
    main_form.resizable(False, False)
    main_form.configure(bg="#34495e")

    button_frame = ttk.Frame(main_form, padding=20, relief="groove", borderwidth=2)
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    region_names = [
        "Dammam", "Riyad", "West-Tabuk", "Almadina", "Abha",
        "Makka", "Taif", "Jedda", "Center", "Distributor",
        "Franchise", "HeadOffc"
    ]

    for i, name in enumerate(region_names):
        button = ttk.Button(button_frame, text=name, style="Custom.TButton", command=lambda name=name: [main_form.withdraw(), open_data_entry_form(name)])
        button.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="ew")

    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)

    export_button = ttk.Button(main_form, text="تصدير إلى Excel", style="Custom.TButton", command=export_to_excel)
    export_button.pack(side=tk.BOTTOM, pady=10)
    #main_form.after(1000, button_frame[0].focus_set)
    main_form.after(100, button_frame.focus_force) #تأخير بسيط ثم تفعيل الفورم
    main_form.mainloop()

# دالة لتصدير البيانات إلى ملف Excel
def export_to_excel():
    try:
        data_frame = pd.DataFrame.from_dict({(i,j): data_storage[i][j] 
                                     for i in data_storage.keys() 
                                     for j in range(len(data_storage[i]))}, orient='index')
        data_frame.to_excel("data_export.xlsx")
        messagebox.showinfo("تم التصدير", "تم تصدير البيانات إلى ملف Excel بنجاح.")
    except Exception as error:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء تصدير البيانات: {error}")

# دالة لتمكين زر تسجيل الدخول عند ملء الحقول
def enable_login_button(event=None):
    username = username_entry.get()
    password = password_entry.get()
    login_button.config(state=tk.NORMAL if username and password else tk.DISABLED)

# إنشاء نافذة تسجيل الدخول
login_window = tk.Tk()
login_window.title("تسجيل الدخول")

style = ttk.Style()
style.theme_use("clam")

# تخصيص الأنماط
style.configure("Custom.TLabel", background="#34495e", font=("tajawal", 18), foreground="#ecf0f1")
style.configure("Custom.TButton", background="#3498db", foreground="white", font=("tajawal", 18, "bold"), padding=15, borderwidth=0)
style.map("Custom.TButton",
          background=[("active", "#2980b9"), ("pressed", "#1c5980"), ("hover", "#5dade2")],
          foreground=[("pressed", "white"), ("active", "white")])
style.configure("Custom.TEntry", padding=12, font=("Arial", 14), relief="flat", borderwidth=2, foreground="#2c3e50", background="#ecf0f1")
style.map("Custom.TEntry",
          background=[("focus", "#ffffff"), ("hover", "#f0f0f0")],
          foreground=[("focus", "#2c3e50")])
style.configure("TFrame", background="#34495e")

window_width = 600
window_height = 450
center_window(login_window, window_width, window_height)
login_window.resizable(False, False)

# تحميل صورة الخلفية
image_path = "background.JPG"
if os.path.exists(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((window_width, window_height), Image.LANCZOS)
        background_image = ImageTk.PhotoImage(image)
        background_label = tk.Label(login_window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as error:
        print(f"Error loading image: {error}")
        login_window.configure(bg="#2c3e50")
else:
    print(f"Error: {image_path} not found. Using default background.")
    login_window.configure(bg="#2c3e50")

# إنشاء إطار لتسجيل الدخول
login_frame = ttk.Frame(login_window, padding=30, relief="groove", borderwidth=2)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# عنوان النموذج
title_label = ttk.Label(login_frame, text="تسجيل الدخول", font=("tajawal", 28, "bold"), style="Custom.TLabel")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# حقل اسم المستخدم
username_label = ttk.Label(login_frame, text="اسم المستخدم:", style="Custom.TLabel")
username_label.grid(row=1, column=0, sticky="w", pady=(10, 0))
username_entry = ttk.Entry(login_frame, style="Custom.TEntry")
username_entry.grid(row=1, column=1, pady=(10, 0), sticky="ew")
username_entry.bind("<KeyRelease>", enable_login_button)
username_entry.bind("<Return>", move_to_next_field)

# حقل كلمة المرور
password_label = ttk.Label(login_frame, text="كلمة المرور:", style="Custom.TLabel")
password_label.grid(row=2, column=0, sticky="w", pady=10)
password_entry = ttk.Entry(login_frame, show="*", style="Custom.TEntry")
password_entry.grid(row=2, column=1, pady=10, sticky="ew")
password_entry.bind("<KeyRelease>", enable_login_button)
password_entry.bind("<Return>", lambda event=None: login_button.invoke())

# زر تسجيل الدخول
login_button = ttk.Button(login_frame, text="تسجيل الدخول", style="Custom.TButton", command=validate_login, state=tk.DISABLED)
login_button.grid(row=3, column=0, columnspan=2, pady=(20, 0))

login_frame.columnconfigure(1, weight=1)

# توجيه التركيز إلى حقل اسم المستخدم عند بدء التشغيل
login_window.after(100, username_entry.focus_set)

# دالة للتعامل مع إغلاق النافذة
def on_closing():
    if messagebox.askokcancel("خروج", "هل تريد حفظ البيانات قبل الخروج؟"):
        save_data_to_json()
    login_window.destroy()

login_window.protocol("WM_DELETE_WINDOW", on_closing)

# بدء تشغيل نافذة تسجيل الدخول
login_window.mainloop()