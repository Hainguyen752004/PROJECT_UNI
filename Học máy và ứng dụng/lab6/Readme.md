# Công nghệ sử dụng
framework: PyTorch: công cụ hỗ trợ tính toán trong có bài toán học máy và học sâu, nhờ khả năng tính toán nhanh, hỗ trợ sử dụng GPU dễ dàng 
các hàm sử dụng trong bài này là torch.nn.functional: xây dựng các mạng NN, torch.tensor: được sử dụng để lưu trữ và xử lý dữ liệu số. Nó tương tự như các mảng (arrays) trong thư viện NumPy nhưng có nhiều tính năng mạnh mẽ hơn
# Thuật toán sử dụng
Trong bài này có 2 thuật toán chính 
đầu tiên là  Loss Functions gồm 3 cái nhỏ là:  MSE,Cross Entropy Loss, Binary Cross Entropy
Activation Functions: Sigmoid:, ReLU, Softmax, Tanh
# giải thích cách hoạt động 
Loss Function:  thuật toán này để đo lường sự khác nhau giữ giá trị dự đoán và thưc tế 
+ Mean Square Error:  dùng đánh giá độ chính xác bằng cách tính bình phương sai số giữ 2 giá trị, trong bài nó được định nghĩa để tính MSE dựa trên hai vector đầu vào là inputs (giá trị dự đoán) và target (giá trị thực tế).
![image](https://github.com/user-attachments/assets/f30e0507-8695-4e05-b451-741da60e1863)
+ Cross Entropy Loss: dùng để đo lường mức độ khác biệt giữa hai phân phối xác suất: một phân phối xác suất dự đoán và một phân phối thực tế (target), trong bài này nó đực được sử dụng để tính toán độ sai lệch giữa phân phối xác suất dự đoán và nhãn thực tế
+ ![image](https://github.com/user-attachments/assets/957ac128-987f-4ea9-a137-59ffd7924df5)
+ Binary Cross Entropy: trong bài sẽ tính tổng BCE cho toàn bộ các phần tử của vector dự đoán và sau đó chia cho tổng số lượng phần tử để lấy trung bình
![image](https://github.com/user-attachments/assets/e9fccb6b-ee04-42b1-b8aa-e3cc0a08b2c8)
Activation Functions:  giúp biến đổi các giá trị đầu ra của mỗi tầng mạng thành một dạng phù hợp để đưa vào các tầng tiếp theo
+ Sigmoid: trong bài này nó  được định nghĩa để áp dụng hàm sigmoid cho mỗi phần tử của vector đầu vào.
![image](https://github.com/user-attachments/assets/412caf7d-d5f1-4f46-a390-4d99ebadd84f)
+ ReLU: Trong bài hàm relu nhận đầu vào và trả về các giá trị âm sẽ bị đổi biến thành 0
![image](https://github.com/user-attachments/assets/71bdaf3b-e26a-4b0c-9309-d1766f6f5f59)
+ Softmax: trong bài nó được định nghĩa để tính toán softmax cho một vector đầu vào, giúp biến đổi các giá trị thành xác suất.
![image](https://github.com/user-attachments/assets/a63267ef-a576-4e0d-8cfc-48ff7cbe7cf1)
+ Tanh: Trong bài hàm tanh biến đổi mỗi phần tử của vector đầu vào thành một giá trị nằm trong khoảng (-1, 1).
![image](https://github.com/user-attachments/assets/4ff43d47-0851-4f82-a6c8-0793fba46365)
# Kết quả local
![image](https://github.com/user-attachments/assets/f064fd85-dd90-40c8-9345-a98c4a31859c)
![image](https://github.com/user-attachments/assets/79f0ab94-d51a-463b-9d69-46369ca71633)
# kết quả web 
![image](https://github.com/user-attachments/assets/d6ea3c95-7049-4452-81a1-4aacc4eba9aa)
# kết quả  
![Uploading Screenshot 2024-10-21 194119.png…]()



