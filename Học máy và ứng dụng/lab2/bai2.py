# bài 2
import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

try:
    drug_data = pd.read_csv(r"D:/HK1 NĂM 3/Học Máy và ứng dụng/Thực Hành/nguyenchihai_2274802010214_lab2/drug.csv")
    print(drug_data.head())  # Kiểm tra vài dòng dữ liệu đầu tiên
except Exception as e:
    print(f"Lỗi khi đọc file CSV: {e}")


# Mã hóa các biến phân loại
label_encoders = {}
for column in ['Sex', 'BP', 'Cholesterol', 'Drug']:
    le = LabelEncoder()
    drug_data[column] = le.fit_transform(drug_data[column])
    label_encoders[column] = le

# Tách dữ liệu thành các đặc trưng và nhãn mục tiêu
X = drug_data.drop(columns='Drug')
y = drug_data['Drug']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Khởi tạo mô hình Naive Bayes Gaussian
gnb = GaussianNB()

# Huấn luyện mô hình
gnb.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = gnb.predict(X_test)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoders['Drug'].classes_)
accuracy, report
print(accuracy, report)
