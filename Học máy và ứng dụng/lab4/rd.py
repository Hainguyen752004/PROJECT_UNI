import dc
import pandas as pd 
import numpy as np
# random.py
from dc import DecisionTreeClass, most_value




# hàm lấy các mẫu dữ liệu ngẫu nhiên trong đó các phần tử có thể lặp lại (trùng nhau)
def bootstrap(X, y):  # X là DataFrame, y là Series
    n_sample = X.shape[0]  # số lượng mẫu trong X
    _id = np.random.choice(n_sample, n_sample, replace=True)  # chọn ngẫu nhiên với hoàn lại
    return X.iloc[_id], y.iloc[_id]  # trả về X và y tương ứng với các chỉ số ngẫu nhiên

# lớp RandomForest 
class RandomForest:
    def __init__(self, n_trees=5, max_depth=10, min_samples_split=2, n_features=None):
        self.n_trees = n_trees  # số cây để đưa ra quyết định cho giá trị dự đoán
        self.max_depth = max_depth  # độ sâu tối đa của mỗi cây
        self.min_samples_split = min_samples_split  # số lượng mẫu tối thiểu để chia một nút
        self.n_features = n_features  # số lượng đặc trưng được chọn ngẫu nhiên cho mỗi cây
        self.trees = []  # danh sách chứa các cây quyết định

    def fit(self, X, y):  # X là DataFrame, y là Series
        self.trees = []  # tạo list chứa các cây cho dự đoán
        for i in range(self.n_trees):
            # với mỗi giá trị i, ta tạo một cây quyết định 
            tree = DecisionTreeClass(min_samples_split=self.min_samples_split, max_depth=self.max_depth, n_features=self.n_features)
            X_sample, y_sample = bootstrap(X, y)  # tạo mẫu X và y thay đổi qua mỗi lần lặp (sampling with replacement)
            tree.fit(X_sample, y_sample)  # huấn luyện cây trên tập dữ liệu đã được bootstrap
            self.trees.append(tree)  # thêm cây vào danh sách các cây

    def predict(self, X):  # X là DataFrame
        # lấy dự đoán từ từng cây
        arr_pred = np.array([tree.predict(X) for tree in self.trees])  # dự đoán từ từng cây
        final_pred = []
        for i in range(arr_pred.shape[1]): 
            sample_pred = arr_pred[:, i]  # lấy dự đoán cho từng mẫu từ các cây
            final_pred.append(most_value(pd.Series(sample_pred)))  # tính giá trị dự đoán cuối cùng bằng voting
        return np.array(final_pred)  # trả về giá trị dự đoán sau khi vote n cây


