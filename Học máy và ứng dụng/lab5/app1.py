import numpy as np
from cvxopt import matrix, solvers
import matplotlib.pyplot as plt
import streamlit as st
st.title('Support Vector Machine Visualization')
st.subheader('Nhập tọa độ các điểm dữ liệu')
data_points = st.text_area("Nhập tọa độ điểm (x1, x2) theo định dạng: x1,x2;x1,x2;", 
                            value='1.0,3.0;2.0,2.0;1.0,1.0')
labels = st.text_area("Nhập nhãn cho các điểm (-1 hoặc 1) theo định dạng: -1;1;1;", 
                       value='1;1;-1')
if data_points and labels:
    x = np.array([list(map(float, point.split(','))) for point in data_points.split(';')])
    y = np.array(list(map(float, labels.split(';')))).reshape(-1, 1)
    H = np.dot(y * x, (y * x).T)
    n = x.shape[0]
    P = matrix(H)
    q = matrix(-np.ones(n)) 
    G = matrix(-np.eye(n))
    h = matrix(np.zeros(n))
    A = matrix(y.reshape(1, -1))
    b = matrix(np.zeros(1))
    solvers.options['abstol'] = 1e-10
    solvers.options['reltol'] = 1e-10
    solvers.options['feastol'] = 1e-10
    sol = solvers.qp(P, q, G, h, A, b)
    lamb = np.array(sol['x'])
    w = np.dot(lamb.T, y * x)
    sv_idx = np.where(lamb > 1e-5)[0]
    sv_lamb = lamb[sv_idx]
    sv_x = x[sv_idx]
    sv_y = y[sv_idx].flatten()
    b = np.mean(sv_y.flatten() - np.dot(sv_x, w.flatten()))
    plt.figure(figsize=(5, 5))
    color = ['red' if a == 1 else 'blue' for a in y.flatten()]
    plt.scatter(x[:, 0], x[:, 1], s=200, c=color, alpha=0.7)
    plt.xlim(0, 4)
    plt.ylim(0, 4)
    x1_dec = np.linspace(0, 4, 100)
    w_flat = w.flatten()
    x2_dec = -(w_flat[0] * x1_dec + b) / w_flat[1]
    plt.plot(x1_dec, x2_dec, c='black', lw=1.0, label='decision boundary')
    w_norm = np.sqrt(np.sum(w ** 2))
    half_margin = 1 / w_norm
    upper = x2_dec + half_margin
    lower = x2_dec - half_margin
    plt.plot(x1_dec, upper, '--', lw=1.0, label='positive boundary')
    plt.plot(x1_dec, lower, '--', lw=1.0, label='negative boundary')
    plt.scatter(sv_x[:, 0], sv_x[:, 1], s=50, marker='o', c='white', label='Support Vectors')

    for s, (x1, x2) in zip(lamb, x):
        plt.annotate(f'λ={s[0].round(2)}', (x1 - 0.05, x2 + 0.2))

    plt.legend()
    plt.title('SVM with 3 Data Points')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.grid()
    st.pyplot(plt)
    st.write(f"Margin = {half_margin * 2:.4f}")
