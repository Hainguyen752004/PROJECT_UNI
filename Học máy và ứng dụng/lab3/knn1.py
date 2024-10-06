import streamlit as st
import numpy as np
import pandas as pd

# Tạo hàm load dữ liệu
def loadCsv(filename) -> pd.DataFrame:
    df = pd.read_csv(filename)
    return df

# Chia tập train-test
def splitTrainTest(data, ratio_test):
    np.random.seed(28)
    index_permu = np.random.permutation(len(data))
    data_permu = data.iloc[index_permu]
    len_test = int(len(data_permu) * ratio_test)
    test_set = data_permu.iloc[:len_test, :]
    train_set = data_permu.iloc[len_test:, :]
    X_train = train_set.iloc[:, :-1]
    y_train = train_set.iloc[:, -1]
    X_test = test_set.iloc[:, :-1]
    y_test = test_set.iloc[:, -1]
    return X_train, y_train, X_test, y_test

# Lấy tần số từ
def get_words_frequency(data_X):
    bag_words = np.concatenate([i[0].split(' ') for i in data_X.values], axis=None)
    bag_words = np.unique(bag_words)
    matrix_freq = np.zeros((len(data_X), len(bag_words)), dtype=int)
    word_freq = pd.DataFrame(matrix_freq, columns=bag_words)
    for id, text in enumerate(data_X.values.reshape(-1)):
        for j in bag_words:
            word_freq.at[id, j] = text.split(' ').count(j)
    return word_freq, bag_words

# Chuyển đổi từ thành tần số cho tập test
def transform(data_test, bags):
    matrix_0 = np.zeros((len(data_test), len(bags)), dtype=int)
    frame_0 = pd.DataFrame(matrix_0, columns=bags)
    for id, text in enumerate(data_test.values.reshape(-1)):
        for j in bags:
            frame_0.at[id, j] = text.split(' ').count(j)
    return frame_0

# Hàm tính cosine distance
def cosine_distance(train_X_number_arr, test_X_number_arr):
    dict_kq = dict()
    train_magnitudes = np.sqrt(np.sum(train_X_number_arr**2, axis=1))
    for id, arr_test in enumerate(test_X_number_arr, start=1):
        q_i = np.sqrt(np.sum(arr_test**2))
        cosine_similarities = []
        for j, d_j in zip(train_X_number_arr, train_magnitudes):
            numerator = np.sum(j * arr_test)
            denominator = d_j * q_i
            kq = numerator / denominator if denominator != 0 else 0
            cosine_similarities.append(kq)
        dict_kq[id] = cosine_similarities
    return dict_kq

# KNN Text Class
class KNNText:
    def __init__(self, k):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        _distance = cosine_distance(self.X_train, X_test)
        _distance_frame = pd.DataFrame(_distance).T

        # In số lượng phần tử của các tập dữ liệu để theo dõi
        st.write(f"Số lượng mẫu trong X_train: {len(self.X_train)}")
        st.write(f"Số lượng mẫu trong y_train: {len(self.y_train)}")
        st.write(f"Số lượng mẫu trong _distance_frame (tương ứng với X_test): {len(_distance_frame)}")

        target_predict = {}

        # Dự đoán nhãn dựa trên khoảng cách cosine
        for i in range(1, len(X_test) + 1):
            sorted_distances = _distance_frame[[i]].join(self.y_train).sort_values(by=i, ascending=True).head(self.k)
            
            # Đếm tần số nhãn và lấy nhãn phổ biến nhất
            most_common_target = sorted_distances[self.y_train.name].value_counts().idxmax()

            # Gán nhãn dự đoán cho từng phần tử của X_test
            target_predict[i] = most_common_target
        return target_predict

    def score(self, X_test, y_test):
        predictions = self.predict(X_test)
        correct_predictions = sum(predictions[i] == y_test.iloc[i - 1] for i in predictions)
        accuracy = correct_predictions / len(y_test)
        return accuracy

# Streamlit UI
def main():
    st.title("KNN Text Classification")

    # Bước 1: Tải dữ liệu
    uploaded_file = st.file_uploader("Tải lên file CSV", type="csv")
    
    if uploaded_file is not None:
        data = loadCsv(uploaded_file)
        data['Text'] = data['Text'].apply(lambda x: x.replace(',', '').replace('.', ''))
        
        st.write("Dữ liệu đã tải:")
        st.dataframe(data)
        
        # Bước 2: Chia dữ liệu
        ratio = st.slider("Chọn tỷ lệ test", 0.1, 0.5, 0.25)
        X_train, y_train, X_test, y_test = splitTrainTest(data, ratio)
        
        st.write(f"Số lượng phần tử trong X_train: {len(X_train)}")
        st.write(f"Số lượng phần tử trong X_test: {len(X_test)}")
        
        # Bước 3: Lấy tần số từ
        words_train_fre, bags = get_words_frequency(X_train)
        st.write("Tần số từ trong tập train:")
        st.dataframe(words_train_fre)

        words_test_fre = transform(X_test, bags)
        
        # Bước 4: KNN
        k = st.slider("Chọn số lượng k (KNN)", 1, 10, 2)
        knn = KNNText(k)
        knn.fit(words_train_fre.values, y_train)

        # Dự đoán và hiển thị kết quả
        # Chuyển đổi kết quả từ `predict` thành DataFrame
        pred = pd.DataFrame.from_dict(knn.predict(words_test_fre.values), orient='index', columns=['Predict'])
        pred.index = range(1, len(pred) + 1)

        # Chuyển `y_test` thành DataFrame
        y_test.index = range(1, len(y_test) + 1)
        y_test = y_test.to_frame(name='Actual')

        # Kết hợp dự đoán và nhãn thực tế
        result = pd.concat([pred, y_test], axis=1)

        st.write("Kết quả dự đoán:")
        st.dataframe(result)

        
        # Độ chính xác
        accuracy = knn.score(words_test_fre.values, y_test['Actual'])
        st.write(f"Độ chính xác của mô hình: {accuracy:.2f}")

if __name__ == '__main__':
    main()
