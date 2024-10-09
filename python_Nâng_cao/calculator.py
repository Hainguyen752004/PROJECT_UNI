import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import math

# Hàm tính toán dựa trên phép tính được chọn
def calculate(operation):
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        
        # Thực hiện phép tính dựa trên nút được nhấn
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Không thể chia cho 0"
        
        # Hiển thị kết quả
        result_var.set(result)
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Hàm xử lý sự kiện khi nhấn nút "Click Me"
def on_click():
    name = entry_name.get()
    if name:
        messagebox.showinfo("Thông báo", f"Xin chào {name}!")
    else:
        messagebox.showinfo("Thông báo", "Vui lòng nhập tên của bạn.")

# Hàm giải phương trình bậc 2
def solve_quadratic():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        # Tính delta
        delta = b**2 - 4*a*c
        
        if delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)
            result_var_2.set(f"Nghiệm x1: {x1}, x2: {x2}")
        elif delta == 0:
            x = -b / (2*a)
            result_var_2.set(f"Nghiệm kép: {x}")
        else:
            result_var_2.set("Phương trình vô nghiệm")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập hệ số hợp lệ")
    except ZeroDivisionError:
        messagebox.showerror("Lỗi", "a không thể bằng 0")

# Hàm giải phương trình bậc 3
def solve_cubic():
    try:
        # Lấy hệ số a, b, c, d từ các ô nhập
        a = float(entry_a3.get())
        b = float(entry_b3.get())
        c = float(entry_c3.get())
        d = float(entry_d3.get())

        # Phương trình bậc 3 dạng: ax^3 + bx^2 + cx + d = 0
        # Sử dụng thư viện NumPy để giải
        coefficients = [a, b, c, d]
        roots = np.roots(coefficients)

        # Hiển thị các nghiệm, bao gồm nghiệm phức (nếu có)
        formatted_roots = [f"{root.real:.2f} + {root.imag:.2f}i" if root.imag != 0 else f"{root.real:.2f}" for root in roots]
        result_var_3.set(f"Nghiệm: {', '.join(formatted_roots)}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập hệ số hợp lệ!")

# Hàm đóng cửa sổ
def exit_program():
    root.quit()

# Hàm hiển thị thông tin trợ giúp
def show_help():
    messagebox.showinfo("Help", "Chương trình này giúp bạn tính toán cơ bản, giải phương trình bậc 2, và giải phương trình bậc 3.\n\nTab 1: Tính cộng, trừ, nhân, chia.\nTab 2: Giải phương trình bậc 2 dạng ax^2 + bx + c = 0.\nTab 3: Giải phương trình bậc 3 dạng ax^3 + bx^2 + cx + d = 0.")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Máy Tính Đơn Giản")

# Tạo Menu chính
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Tạo menu "File" với nút Exit
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=exit_program)
menu_bar.add_cascade(label="File", menu=file_menu)

# Tạo menu "Help" với thông tin trợ giúp
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=show_help)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Tạo Notebook để chứa các tab
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, expand=True)

# Tạo tab 1 - Tính toán cơ bản
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tính Toán Cơ Bản")

# Frame cho các thành phần của tab 1
frame1 = ttk.Frame(tab1, padding="10 10 10 10")
frame1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Nhãn và ô nhập tên
label_name = ttk.Label(frame1, text="Enter a name:")
label_name.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_name = ttk.Entry(frame1, width=20)
entry_name.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

# Nút "Click Me"
click_button = ttk.Button(frame1, text="Click Me!", command=on_click)
click_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô nhập Số A
label_num1 = ttk.Label(frame1, text="Số A:")
label_num1.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_num1 = ttk.Entry(frame1, width=20)
entry_num1.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô nhập Số B
label_num2 = ttk.Label(frame1, text="Số B:")
label_num2.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_num2 = ttk.Entry(frame1, width=20)
entry_num2.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

# Tạo các nút cho các phép tính
add_button = ttk.Button(frame1, text="+", command=lambda: calculate('add'))
add_button.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)

subtract_button = ttk.Button(frame1, text="-", command=lambda: calculate('subtract'))
subtract_button.grid(row=1, column=3, padx=10, pady=10, sticky=tk.W)

multiply_button = ttk.Button(frame1, text="x", command=lambda: calculate('multiply'))
multiply_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

divide_button = ttk.Button(frame1, text="÷", command=lambda: calculate('divide'))
divide_button.grid(row=2, column=3, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô hiển thị kết quả
label_result = ttk.Label(frame1, text="Kết quả:")
label_result.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
result_var = tk.StringVar()
result_entry = ttk.Entry(frame1, textvariable=result_var, state='readonly', width=20)
result_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky=(tk.W, tk.E))

# Tạo tab 2 - Giải phương trình bậc 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Giải PT Bậc 2")

# Frame cho các thành phần của tab 2
frame2 = ttk.Frame(tab2, padding="10 10 10 10")
frame2.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Nhãn và ô nhập hệ số a
label_a = ttk.Label(frame2, text="Hệ số a:")
label_a.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_a = ttk.Entry(frame2, width=20)
entry_a.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô nhập hệ số b
label_b = ttk.Label(frame2, text="Hệ số b:")
label_b.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_b = ttk.Entry(frame2, width=20)
entry_b.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô nhập hệ số c
label_c = ttk.Label(frame2, text="Hệ số c:")
label_c.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_c = ttk.Entry(frame2, width=20)
entry_c.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

# Nút giải phương trình bậc 2
solve_button = ttk.Button(frame2, text="Giải PT", command=solve_quadratic)
solve_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Nhãn và ô hiển thị kết quả phương trình bậc 2
label_result_2 = ttk.Label(frame2, text="Kết quả:")
label_result_2.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
result_var_2 = tk.StringVar()
result_entry_2 = ttk.Entry(frame2, textvariable=result_var_2, state='readonly', width=40)
result_entry_2.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

# Tạo tab 3 - Giải phương trình bậc 3
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Giải PT Bậc 3")

# Frame cho các thành phần của tab 3
frame3 = ttk.Frame(tab3, padding="10 10 10 10")
frame3.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Nhãn và ô nhập hệ số a
label_a3 = ttk.Label(frame3, text="Hệ số a:")
label_a3.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_a3 = ttk.Entry(frame3, width=20)
entry_a3.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô nhập hệ số b
label_b3 = ttk.Label(frame3, text="Hệ số b:")
label_b3.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_b3 = ttk.Entry(frame3, width=20)
entry_b3.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô nhập hệ số c
label_c3 = ttk.Label(frame3, text="Hệ số c:")
label_c3.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_c3 = ttk.Entry(frame3, width=20)
entry_c3.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

# Nhãn và ô nhập hệ số d
label_d3 = ttk.Label(frame3, text="Hệ số d:")
label_d3.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
entry_d3 = ttk.Entry(frame3, width=20)
entry_d3.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

# Nút giải phương trình bậc 3
solve_button_3 = ttk.Button(frame3, text="Giải PT Bậc 3", command=solve_cubic)
solve_button_3.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Nhãn và ô hiển thị kết quả phương trình bậc 3
label_result_3 = ttk.Label(frame3, text="Kết quả:")
label_result_3.grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)
result_var_3 = tk.StringVar()
result_entry_3 = ttk.Entry(frame3, textvariable=result_var_3, state='readonly', width=40)
result_entry_3.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))

# Chạy chương trình
root.mainloop()
