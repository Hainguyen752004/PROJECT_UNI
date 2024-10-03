import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
X = np.array([180, 162, 183, 174, 160, 163, 180, 165, 175, 170, 170, 169,
168, 175, 169, 171, 155, 158, 175, 165]).reshape(-1,1)
y = np.array([86, 55, 86.5, 70, 62, 54, 60, 72, 93, 89, 60, 82, 59, 75,
56, 89, 45, 60, 60, 72]).reshape((-1,1))
# học lõm google mà đã hiểu
x2 = np.hstack([np.ones((X.shape[0], 1)), X]) # dòng này tạo thêm 1 b[0] Intercept : nói cụ thể hơn là tạo thêm 1 cột toàn số 1 và dùng hstack để gọp chung vào X tạo ra x2 mang 20 dòng và 2 cột cột đầu là 1 cột 2 là chiều cao
theta = np.linalg.inv(x2.T.dot(x2)).dot(x2.T).dot(y) # công thức hồi quy tuyến tính   np.linalg.inv nghịch đảo ma trận x2.T.dot(x2) tích vô hướng 2 ma trận y là biến phụ thuộc vào x khi x thay đổi y thay đổi ma trận chuyển vị x2.T
x1 = 150
y1 = theta[0] + theta[1] * x1
x2 = 190
y2 = theta[0] + theta[1] * x2
plt.plot([x1, x2], [y1, y2], 'r-')
plt.plot(X[:,0], y[:,0], 'bo')
plt.xlabel('Chiều cao')
plt.ylabel('Cân nặng')
plt.title('Chiều cao và cân nặng của sinh viên VLU')
plt.show()
