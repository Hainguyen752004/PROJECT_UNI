import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dc import DecisionTreeClass, accuracy  
from rd import RandomForest  

# Tiêu đề ứng dụng
st.title('Dự đoán với Decision Tree và Random Forest')

# Tải tệp CSV
uploaded_file = st.file_uploader("Chọn tệp CSV", type="csv")
if uploaded_file is not None:
    # Đọc dữ liệu từ file
    data = pd.read_csv(uploaded_file)

    # Tách dữ liệu thành X và y
    X = data.iloc[:, :-1]  
    y = data.iloc[:, -1]  

    # Hiển thị dữ liệu đầu vào
    st.write("Dữ liệu đầu vào:")
    st.write(X.head())  
    st.write(y.head()) 

    # Biến đổi dữ liệu định tính sang định lượng
    X['Sex'] = X['Sex'].map({'M': 0, 'F': 1})
    X['BP'] = X['BP'].map({'LOW': 0, 'NORMAL': 1, 'HIGH': 2})
    X['Cholesterol'] = X['Cholesterol'].map({'NORMAL': 0, 'HIGH': 1})
    y = y.map({'drugA': 0, 'drugB': 1, 'drugC': 2, 'drugX': 3, 'DrugY': 4})

    st.write("Dữ liệu sau khi biến đổi:")
    st.write(X.head()) 
    st.write(y.head())  

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Các tham số cho Decision Tree
    st.sidebar.header("Tham số cho Decision Tree")
    max_depth_dt = st.sidebar.slider("Chọn độ sâu tối đa của Decision Tree", 1, 20, 10)
    min_samples_split_dt = st.sidebar.slider("Chọn số lượng mẫu tối thiểu để chia một nút", 2, 10, 2)

    # Huấn luyện và dự đoán với Decision Tree
    st.write("Sử dụng Decision Tree để dự đoán:")
    decisionTree = DecisionTreeClass(min_samples_split=min_samples_split_dt, max_depth=max_depth_dt)
    decisionTree.fit(X_train, y_train)
    y_pred = decisionTree.predict(X_test)

    st.write("Dự đoán của Decision Tree:")
    st.write(y_pred)

    # Tính độ chính xác cho Decision Tree
    accuracy_value = accuracy(y_test.values, y_pred)
    st.write(f"Độ chính xác của Decision Tree: {accuracy_value}%")

    # Các tham số cho Random Forest
    st.sidebar.header("Tham số cho Random Forest")
    n_trees_rf = st.sidebar.slider("Chọn số lượng cây trong Random Forest", 1, 50, 10)  # Giới hạn số cây
    max_depth_rf = st.sidebar.slider("Chọn độ sâu tối đa của Random Forest", 1, 15, 5)  # Giới hạn độ sâu
    n_features_rf = st.sidebar.slider("Chọn số lượng đặc trưng cho mỗi cây", 1, X.shape[1], 4)

    # Huấn luyện trên một phần nhỏ của dữ liệu để tiết kiệm bộ nhớ
    st.write("Sử dụng Random Forest để dự đoán:")
    randomForest = RandomForest(n_trees=n_trees_rf, max_depth=max_depth_rf, n_features=n_features_rf)

    # Huấn luyện trên một tập con (ví dụ: 20% của tập huấn luyện)
    X_train_sample = X_train.sample(frac=0.2, random_state=42)
    y_train_sample = y_train.loc[X_train_sample.index]

    randomForest.fit(X_train_sample, y_train_sample)

    # Dự đoán với Random Forest
    y_pred_rf = randomForest.predict(X_test)

    st.write("Dự đoán của Random Forest:")
    st.write(y_pred_rf)

    # Tính độ chính xác cho Random Forest
    accuracy_value_rf = accuracy(y_test.values, y_pred_rf)
    st.write(f"Độ chính xác của Random Forest: {accuracy_value_rf}%")
else:
    st.write("Vui lòng tải lên tệp CSV để tiếp tục.")
