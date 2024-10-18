import numpy as np
from cvxopt import matrix as cvxopt_matrix
from cvxopt import solvers as cvxopt_solvers
import matplotlib.pyplot as plt
import streamlit as st

# Tiêu đề ứng dụng
st.title('Support Vector Machine Visualization')

# Nhập tham số C
C = st.number_input("Nhập giá trị C cho SVM:", min_value=0.0, value=50.0)

# Dữ liệu huấn luyện
x = np.array([[0.2, 0.869],
              [0.687, 0.212],
              [0.822, 0.411],
              [0.738, 0.694],
              [0.176, 0.458],
              [0.306, 0.753],
              [0.936, 0.413],
              [0.215, 0.410],
              [0.612, 0.375],
              [0.784, 0.602],
              [0.612, 0.554],
              [0.357, 0.254],
              [0.204, 0.775],
              [0.512, 0.745],
              [0.498, 0.287],
              [0.251, 0.557],
              [0.502, 0.523],
              [0.119, 0.687],
              [0.495, 0.924],
              [0.612, 0.851]])

y = np.array([-1, 1, 1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1])
y = y.astype('float').reshape(-1, 1)

# ---- Tính λ sử dụng cvxopt ----
N = x.shape[0]

# Xây dựng các ma trận cần thiết cho QP trong định dạng chuẩn
H = np.dot(y * x, (y * x).T)
P = cvxopt_matrix(H)
q = cvxopt_matrix(np.ones(N) * -1)
A = cvxopt_matrix(y.reshape(1, -1))
b = cvxopt_matrix(np.zeros(1))

g = np.vstack([-np.eye(N), np.eye(N)])  # Định nghĩa G
G = cvxopt_matrix(g)

h1 = np.hstack([np.zeros(N), np.ones(N) * C])  # Định nghĩa h
h = cvxopt_matrix(h1)

# Tham số cho solver
cvxopt_solvers.options['abstol'] = 1e-10
cvxopt_solvers.options['reltol'] = 1e-10
cvxopt_solvers.options['feastol'] = 1e-10

# Thực hiện QP
sol = cvxopt_solvers.qp(P, q, G, h, A, b)

# Giải pháp cho QP, λ
lamb = np.array(sol['x'])

# ---------------------------------------------------------------

# Tính w từ λ
w = np.sum(lamb * y * x, axis=0)

# Tìm các vector hỗ trợ
sv_idx = np.where(lamb > 1e-5)[0]
sv_lamb = lamb[sv_idx]
sv_x = x[sv_idx]
sv_y = y[sv_idx]

# Tính b
b = np.mean(sv_y - np.dot(sv_x, w))

# Trực quan hóa
plt.figure(figsize=(7, 7))
color = ['red' if a == 1 else 'blue' for a in y]
plt.scatter(x[:, 0], x[:, 1], s=200, c=color, alpha=0.7)
plt.xlim(0, 1)
plt.ylim(0, 1)

# Tính đường biên quyết định
x1_dec = np.linspace(0, 1, 100)
x2_dec = -(w[0] * x1_dec + b) / w[1]  
plt.plot(x1_dec, x2_dec, c='black', lw=1.0, label='decision boundary')

# Hiển thị các biến slack
y_hat = np.dot(x, w) + b  
slack = np.maximum(0, 1 - y_hat * y.flatten())  

for s, (x1, x2) in zip(slack, x):
    plt.annotate(str(s.round(2)), (x1 - 0.02, x2 + 0.03))

# Tính các đường biên
w_norm = np.sqrt(np.sum(w ** 2))
half_margin = 1 / w_norm

# Tính và vẽ các đường biên
upper = x2_dec + half_margin
lower = x2_dec - half_margin

plt.plot(x1_dec, upper, '--', lw=1.0, label='positive boundary')
plt.plot(x1_dec, lower, '--', lw=1.0, label='negative boundary')

plt.scatter(sv_x[:, 0], sv_x[:, 1], s=60, marker='o', c='white')
plt.legend()
plt.title('C = ' + str(C) + ',  Σξ = ' + str(np.sum(slack).round(2)))
plt.grid()

# Hiển thị đồ thị
st.pyplot(plt)
