import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Load dữ liệu từ file Excel
def load_excel(file) -> pd.DataFrame:
    data = pd.read_excel(file)
    return data

# Chia tập train-test
def split_train_test(data, target, ratio=0.25):
    data_X = data.drop([target], axis=1)
    data_y = data[[target]]
    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, test_size=ratio, random_state=42)
    data_train = pd.concat([X_train, y_train], axis=1)
    return data_train, X_test, y_test

# Tính trung bình của từng lớp trong biến target
def mean_class(data_train, target):
    numeric_data = data_train.select_dtypes(include=[np.number])
    df_group = numeric_data.groupby(data_train[target]).mean()
    return df_group

# Dự đoán lớp sử dụng khoảng cách Euclid
def target_pred(data_group, data_test):
    # Giữ lại các cột tương ứng giữa data_group và data_test
    data_test_numeric = pd.DataFrame(data_test, columns=data_group.columns)

    dict_ = dict()
    for index, value in enumerate(data_group.values):
        # Tính khoảng cách Euclid giữa các hàng của data_test_numeric và giá trị trung bình của mỗi lớp
        result = np.sqrt(np.sum(((data_test_numeric - value) ** 2), axis=1))
        dict_[index] = result
    df = pd.DataFrame(dict_)
    return df.idxmin(axis=1)  # Tìm cột chứa giá trị nhỏ nhất

# Ánh xạ các giá trị số thành tên lớp
class_mapping = {0: 'Iris-setosa', 1: 'Iris-versicolor', 2: 'Iris-virginica'}

# Giao diện chính với Streamlit
def main():
    st.title("Ứng dụng dự đoán bằng khoảng cách Euclid")

    # Bước 1: Người dùng tải file Excel
    uploaded_file = st.file_uploader("Tải lên file Excel", type="xlsx")
    
    if uploaded_file is not None:
        # Bước 2: Hiển thị dữ liệu
        data = load_excel(uploaded_file)
        st.write("Dữ liệu:")
        st.dataframe(data)

        # Kiểm tra giá trị NaN trong dữ liệu
        st.write("Kiểm tra giá trị thiếu:")
        st.write(data.isna().sum())

        # Bước 3: Chọn tỷ lệ chia tập dữ liệu
        ratio = st.slider("Chọn tỷ lệ test", 0.1, 0.5, 0.3)
        
        # Bước 4: Chia tập train-test
        target = st.selectbox("Chọn cột target", data.columns)
        
        # Mã hóa cột target nếu cần thiết
        if data[target].dtype == 'object':
            st.write(f"Ánh xạ cột target {target} thành giá trị số...")
            data[target] = data[target].map({'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2})
        
        data_train, X_test, y_test = split_train_test(data, target, ratio)
        
        st.write("Tập huấn luyện:")
        st.dataframe(data_train)

        st.write("Tập kiểm tra:")
        st.dataframe(X_test)

        # Lọc các cột số từ X_test để chuẩn bị cho dự đoán
        X_test_numeric = X_test.select_dtypes(include=[np.number])
        
        # Bước 5: Tính trung bình của từng lớp
        df_group = mean_class(data_train, target)
        st.write("Trung bình các lớp:")
        st.dataframe(df_group)

        # Kiểm tra cột của df_group và X_test_numeric để đảm bảo chúng khớp
        st.write("Các cột trong df_group:", df_group.columns)
        st.write("Các cột trong X_test_numeric:", X_test_numeric.columns)

        # Bước 6: Dự đoán dựa trên khoảng cách Euclid
        predictions = target_pred(df_group, X_test_numeric)
        st.write("Kết quả dự đoán trước khi ánh xạ:", predictions)

        df_pred = pd.DataFrame(predictions.map(class_mapping), columns=['Predict'])
        
        # Bước 7: Kết quả dự đoán
        y_test.index = range(0, len(y_test))
        y_test.columns = ['Actual']
        df_actual = pd.DataFrame(y_test)

        # Ánh xạ lớp thực tế nếu cần (nếu nó ở dạng số thay vì tên lớp)
        if df_actual['Actual'].dtype != 'object':
            df_actual['Actual'] = df_actual['Actual'].map(class_mapping)
        
        # Hiển thị kết quả dự đoán cuối cùng
        result = pd.concat([df_pred, df_actual], axis=1)
        st.write("Kết quả dự đoán:")
        st.dataframe(result)

if __name__ == '__main__':
    main()
