import streamlit as st
import numpy as np
import math

# Hàm tính toán dựa trên phép tính được chọn
def calculate(num1, num2, operation):
    try:
        num1 = float(num1)
        num2 = float(num2)

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
        return result
    except ValueError:
        return "Vui lòng nhập số hợp lệ"

# Hàm giải phương trình bậc 2
def solve_quadratic(a, b, c):
    try:
        a = float(a)
        b = float(b)
        c = float(c)

        delta = b**2 - 4*a*c

        if delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)
            return f"Nghiệm x1: {x1}, x2: {x2}"
        elif delta == 0:
            x = -b / (2*a)
            return f"Nghiệm kép: {x}"
        else:
            return "Phương trình vô nghiệm"
    except ValueError:
        return "Vui lòng nhập hệ số hợp lệ"
    except ZeroDivisionError:
        return "a không thể bằng 0"

# Hàm giải phương trình bậc 3
def solve_cubic(a, b, c, d):
    try:
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)

        coefficients = [a, b, c, d]
        roots = np.roots(coefficients)

        formatted_roots = [f"{root.real:.2f} + {root.imag:.2f}i" if root.imag != 0 else f"{root.real:.2f}" for root in roots]
        return f"Nghiệm: {', '.join(formatted_roots)}"
    except ValueError:
        return "Vui lòng nhập hệ số hợp lệ!"

# Giao diện Streamlit
st.title("Máy Tính Đơn Giản")

# Tính toán cơ bản
st.header("Tính Toán Cơ Bản")
num1 = st.text_input("Số A", "0")
num2 = st.text_input("Số B", "0")
operation = st.selectbox("Chọn phép tính", ["add", "subtract", "multiply", "divide"])

if st.button("Tính Toán"):
    result = calculate(num1, num2, operation)
    st.write(f"Kết quả: {result}")

# Giải phương trình bậc 2
st.header("Giải Phương Trình Bậc 2")
a = st.text_input("Hệ số a", "0")
b = st.text_input("Hệ số b", "0")
c = st.text_input("Hệ số c", "0")

if st.button("Giải Phương Trình Bậc 2"):
    result = solve_quadratic(a, b, c)
    st.write(result)

# Giải phương trình bậc 3
st.header("Giải Phương Trình Bậc 3")
a3 = st.text_input("Hệ số a", "0", key="a3")
b3 = st.text_input("Hệ số b", "0", key="b3")
c3 = st.text_input("Hệ số c", "0", key="c3")
d3 = st.text_input("Hệ số d", "0", key="d3")

if st.button("Giải Phương Trình Bậc 3"):
    result = solve_cubic(a3, b3, c3, d3)
    st.write(result)
