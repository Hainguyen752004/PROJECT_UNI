import streamlit as st
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine

# Tải dữ liệu Wine từ sklearn
data = load_wine()
X, y = data.data, data.target

# Giao diện người dùng để nhập giá trị k và chia dữ liệu
st.title("Mô hình KNN phân loại dữ liệu Wine")
k = st.slider("Chọn giá trị k:", min_value=1, max_value=20, value=5)
test_size = st.slider("Chọn tỷ lệ tập kiểm tra:", min_value=0.1, max_value=0.5, step=0.05, value=0.3)

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

# Hiển thị một vài mẫu dữ liệu
st.write("Một vài mẫu từ tập huấn luyện:")
st.write(X_train[:5])
st.write("Một vài mẫu từ tập kiểm tra:")
st.write(X_test[:5])

# Định nghĩa hàm tính khoảng cách Euclidean
def euclidean_distance(a, b):
    return np.sum((a - b) ** 2)

# Hàm dự đoán KNN
def knn_predict(X_train, y_train, X_test, k=5):
    y_pred = []
    for test_point in X_test:
        distances = [euclidean_distance(test_point, x) for x in X_train]
        k_indices = np.argsort(distances)[:k]
        k_nearest_labels = [y_train[i] for i in k_indices]
        most_common = max(set(k_nearest_labels), key=k_nearest_labels.count)
        y_pred.append(most_common)
    return np.array(y_pred)

# Dự đoán trên tập kiểm tra với giá trị k do người dùng chọn
y_pred_knn = knn_predict(X_train, y_train, X_test, k=k)

# Định nghĩa hàm tính ma trận nhầm lẫn
def confusion_matrix(y_true, y_pred):
    TP = np.sum((y_true == 1) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    FN = np.sum((y_true == 1) & (y_pred == 0))
    return np.array([[TN, FP], [FN, TP]])

# Hàm tính toán và in các chỉ số
def evaluate_model(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm.ravel()
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) != 0 else 0
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    # Hiển thị kết quả trên Streamlit
    st.write("Confusion Matrix:")
    st.write(cm)
    st.write(f"Accuracy: {accuracy:.2f}")
    st.write(f"Recall: {recall:.2f}")
    st.write(f"Specificity: {specificity:.2f}")
    st.write(f"Precision: {precision:.2f}")
    st.write(f"F1 Score: {f1:.2f}")

# Đánh giá mô hình KNN
st.header("Đánh giá mô hình KNN:")
evaluate_model(y_test, y_pred_knn)
