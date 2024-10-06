import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# Tiêu đề của ứng dụng
st.title("Drug Classification using Naive Bayes")

# Tải file CSV từ đường dẫn
csv_file_path = r"D:/HK1 NĂM 3/Học Máy và ứng dụng/Thực Hành/nguyenchihai_2274802010214_lab2/drug.csv"

try:
    # Đọc dữ liệu từ file CSV
    drug_data = pd.read_csv(csv_file_path)
    st.subheader("Dữ liệu đầu tiên:")
    st.write(drug_data.head())  # Hiển thị vài dòng đầu tiên của dữ liệu
except Exception as e:
    st.error(f"Lỗi khi đọc file CSV: {e}")

# Mã hóa các biến phân loại
st.subheader("Mã hóa các biến phân loại:")
label_encoders = {}
for column in ['Sex', 'BP', 'Cholesterol', 'Drug']:
    le = LabelEncoder()
    drug_data[column] = le.fit_transform(drug_data[column])
    label_encoders[column] = le
st.write(drug_data.head())  # Hiển thị dữ liệu sau khi mã hóa

# Tách dữ liệu thành các đặc trưng và nhãn mục tiêu
X = drug_data.drop(columns='Drug')
y = drug_data['Drug']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Khởi tạo và huấn luyện mô hình Naive Bayes Gaussian
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = gnb.predict(X_test)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoders['Drug'].classes_)

# Hiển thị kết quả
st.subheader("Kết quả đánh giá mô hình:")
st.write(f"Độ chính xác của mô hình: {accuracy:.2f}")

# Hiển thị báo cáo phân loại
st.subheader("Báo cáo phân loại:")
st.text(report)
