from dc import DecisionTreeClass, most_value
from rd import RandomForest
# Import các thư viện
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from rd import RandomForest  
from dc import DecisionTreeClass, accuracy  
import sys
import io

# Thiết lập mã hóa UTF-8 cho stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Đọc dữ liệu từ tệp CSV
data = pd.read_csv('D:\\HK1_Nam_3\\Machine_leanning\\Thực Hành\\code_data\\code_data\\drug200.csv')

# Tạo tập X (tất cả các cột trừ cột cuối cùng) và y (cột cuối cùng)
X = data.iloc[:, :-1]  # Tất cả các cột trừ cột cuối cùng
y = data.iloc[:, -1]   # Cột cuối cùng là biến mục tiêu

# Hiển thị X và y để kiểm tra
print(X.head())  # Hiển thị 5 dòng đầu tiên của X
print(y.head())  # Hiển thị 5 dòng đầu tiên của y

# Lấy các giá trị duy nhất từ các cột định tính và in ra
print(set(X['Sex']))  # Cột 'Sex'
print(set(X['BP']))   # Cột 'BP'
print(set(X['Cholesterol']))  # Cột 'Cholesterol'
print(set(y))  # Cột mục tiêu 'Drug' (biến y)

# Biến đổi dữ liệu định tính sang định lượng
X['Sex'] = X['Sex'].map({'M': 0, 'F': 1})
X['BP'] = X['BP'].map({'LOW': 0, 'NORMAL': 1, 'HIGH': 2})
X['Cholesterol'] = X['Cholesterol'].map({'NORMAL': 0, 'HIGH': 1})
y = y.map({'drugA': 0, 'drugB': 1, 'drugC': 2, 'drugX': 3, 'DrugY': 4})

print(X.head())  # Hiển thị dữ liệu đã biến đổi
print(y.head())  # Hiển thị biến mục tiêu đã biến đổi

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# In ra dữ liệu tập huấn luyện và kiểm tra
print("X_train:")
print(X_train.to_string()) 
print("\ny_train:")
print(y_train.to_string()) 
print("\nX_test:")
print(X_test.to_string())   
print("\ny_test:")
print(y_test.to_string())   

# Sử dụng model Decision Tree
decisionTree = DecisionTreeClass(min_samples_split=2, max_depth=10)
decisionTree.fit(X_train, y_train)
y_pred = decisionTree.predict(X_test)

# In kết quả dự đoán
print("Dự đoán của Decision Tree:")
print(y_pred)

# In giá trị thực tế
print("Giá trị thực tế của y_test:")
print(y_test.values)

# Tính độ chính xác cho Decision Tree
accuracy_value = accuracy(y_test.values, y_pred)
print(f"Độ chính xác của Decision Tree: {accuracy_value}%")

# Sử dụng model Random Forest
randomForest = RandomForest(n_trees=3, max_depth=5, n_features=4)
randomForest.fit(X_train, y_train)

# Huấn luyện trên một phần nhỏ của tập dữ liệu
X_train_sample = X_train.sample(frac=0.2, random_state=42)
y_train_sample = y_train.loc[X_train_sample.index]
randomForest.fit(X_train_sample, y_train_sample)

# Dự đoán với Random Forest
y_pred_rf = randomForest.predict(X_test)

# In kết quả dự đoán của Random Forest
print("Dự đoán của Random Forest:")
print(y_pred_rf)

# Tính độ chính xác cho Random Forest
accuracy_value_rf = accuracy(y_test.values, y_pred_rf)
print(f"Độ chính xác của Random Forest: {accuracy_value_rf}%")

