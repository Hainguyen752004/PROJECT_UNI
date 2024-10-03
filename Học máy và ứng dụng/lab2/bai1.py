#bài 1
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Đọc file dữ liệu
dataset = "D:/HK1 NĂM 3/Học Máy và ứng dụng/Thực Hành/nguyenchihai_2274802010214_lab2/Education.csv"
data = pd.read_csv(dataset)

# Hiển thị dữ liệu đầu tiên để kiểm tra
print("Dữ liệu đầu tiên:")
print(data.head())

# Sử dụng LabelEncoder để chuyển đổi nhãn từ văn bản thành số
label_encoder = LabelEncoder()
data['Label_2'] = label_encoder.fit_transform(data['Label'])  # Mã hóa cột 'Label' (Positive/Negative)

# In dữ liệu sau khi mã hóa nhãn
print("\nDữ liệu sau khi mã hóa nhãn:")
print(data[['Text', 'Label', 'Label_2']].head())

# Sử dụng CountVectorizer để chuyển đổi văn bản thành ma trận đặc trưng
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['Text'])  # Chuyển đổi cột 'Text' thành ma trận số
y = data['Label_2']  # Cột 'Label_2' là nhãn đã mã hóa

# Chia dữ liệu thành tập huấn luyện và tập kiểm thử
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình Bernoulli Naive Bayes
bernoulli_nb = BernoulliNB()
bernoulli_nb.fit(X_train, y_train)
y_pred_bernoulli = bernoulli_nb.predict(X_test)
accuracy_bernoulli = accuracy_score(y_test, y_pred_bernoulli)

# Huấn luyện mô hình Multinomial Naive Bayes
multinomial_nb = MultinomialNB()
multinomial_nb.fit(X_train, y_train)
y_pred_multinomial = multinomial_nb.predict(X_test)
accuracy_multinomial = accuracy_score(y_test, y_pred_multinomial)

# In kết quả
print(f"Accuracy Bernoulli Naive Bayes: {accuracy_bernoulli:.2f}")
print(f"Accuracy Multinomial Naive Bayes: {accuracy_multinomial:.2f}")
