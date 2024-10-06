import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Tiêu đề của ứng dụng
st.title("Text Classification using Naive Bayes")

# Tải dữ liệu
dataset = "D:/HK1 NĂM 3/Học Máy và ứng dụng/Thực Hành/nguyenchihai_2274802010214_lab2/Education.csv"
data = pd.read_csv(dataset)

# Hiển thị dữ liệu đầu tiên
st.subheader("Dữ liệu đầu tiên:")
st.write(data.head())

# Chuyển đổi nhãn văn bản thành số
label_encoder = LabelEncoder()
data['Label_2'] = label_encoder.fit_transform(data['Label'])  # Mã hóa cột 'Label'

# Hiển thị dữ liệu sau khi mã hóa nhãn
st.subheader("Dữ liệu sau khi mã hóa nhãn:")
st.write(data[['Text', 'Label', 'Label_2']].head())

# Sử dụng CountVectorizer để chuyển đổi văn bản thành ma trận đặc trưng
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['Text'])
y = data['Label_2']

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

# Hiển thị kết quả
st.subheader("Kết quả:")
st.write(f"Độ chính xác của Bernoulli Naive Bayes: {accuracy_bernoulli:.2f}")
st.write(f"Độ chính xác của Multinomial Naive Bayes: {accuracy_multinomial:.2f}")

# Hiển thị báo cáo phân loại cho mô hình Bernoulli Naive Bayes
st.subheader("Báo cáo phân loại Bernoulli Naive Bayes:")
st.text(classification_report(y_test, y_pred_bernoulli))

# Hiển thị báo cáo phân loại cho mô hình Multinomial Naive Bayes
st.subheader("Báo cáo phân loại Multinomial Naive Bayes:")
st.text(classification_report(y_test, y_pred_multinomial))
