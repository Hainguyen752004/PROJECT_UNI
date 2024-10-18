# đây là ở đồ thị 1 (App1)
# Công nghệ sử dụng
numpy : làm việc mãng đa chiều, các phép tính toán
matplotlib : hỗ trợ vẽ đồ thị 
cvxopt (Quadratic Programming - QP): hỗ trợ giải quyết các bài toán tối ưu hóa
# Thuật Toán sử dụng và giải thích
Thuật toán chính trong bài này là Support Vector Machine (SVM) trong bài toán này nó được thực hiện để phân loại các điểm dữ liệu dựa trên nhãn của chúng (1 hoặc -1).
Quadratic Programming (QP) Tối ưu hoá để tìm ra giá trị λ cho cực tiểu hàm mục tiêu với việc sử dụng QP lưu ý rằng phải Thỏa mãn các ràng buộc là các λ đều lớn hơn hoặc bằng 0 và tổng của λiyi phải bằng 0.
Sau khi xác định được vector hỗ trợ sau đó bắt đầu tính b từ các vector hỗ trợ
Cuối cùng là vẽ đồ thị bằng phương trình w0x1 + w1x2 + b ‎ =  0.
# kết quả:
- Trên web: ![image](https://github.com/user-attachments/assets/650dfed9-f98a-4ed6-b473-b2cb547c7aa2)
- local: ![image](https://github.com/user-attachments/assets/23ab623b-117c-4cd6-988f-0807b27c65dc)
# đây là ở đồ thị 2 (App2)
# Công nghệ sử dụng
numpy : làm việc mãng đa chiều, các phép tính toán
matplotlib : hỗ trợ vẽ đồ thị 
cvxopt (Quadratic Programming - QP): hỗ trợ giải quyết các bài toán tối ưu hóa
# Thuật toán sử dụng và giải thích
Thuật toán chính là Support Vector Machine (SVM) với tham số C. Trong bài toán này để điều chỉnh cách mô hình đối xử với các điểm dữ liệu
+ Nếu C lớn: Mô hình cố gắng giảm thiểu số lượng lỗi phân loại bằng cách yêu cầu các điểm dữ liệu phải nằm bên đúng của biên phân cách
+ Nếu C nhỏ, mô hình SVM sẽ cho phép một số lỗi phân loại, tạo ra soft margin, giúp siêu phẳng phân loại tổng quát hơn.
Quadratic Programming (QP) từ thư viện cvxopt để tìm ra các giá trị λλ tối ưu.
Khi có λλ, chúng ta tính vector trọng số ww và bias bb để xác định đường phân tách giữa hai lớp dữ liệu
các giá trị slack ξξ được tính để đo lường mức độ các điểm dữ liệu nằm ngoài margin
cuối cùng vẽ phương trình.
# Kết quả:
- trên web: ![image](https://github.com/user-attachments/assets/5104dd22-1b4e-4b2d-97bc-c2c9e26d8ca4)
- Local: ![image](https://github.com/user-attachments/assets/7202e8a7-a3aa-4c63-973f-b0bd288eed35)



