# Framework sử dụng trong bài 
tkinter trong tkinter có messagebox. Psycopg2 tương tác dữ liệu SQL
# Giải thích mô hình MVC
đầu tiên là model:
Chức năng: Quản lý dữ liệu và logic xử lý liên quan đến dữ liệu,kết nối và tương tác với cơ sở dữ liệu PostgreSQL.
các chương trình nhỏ như là: connect,fetch_data,insert_data,update_data,delete_data
tiếp theo là View:
Chức năng: quản lý giao diện người dùng, hiển thị dữ liệu từ người dùng
các chương trình bên trong bao gồm:create_widgets,set_controller
thứ ba là controller:
chức năng là: Điều phối giữa Model và View, Nhận sự kiện từ người dùng thông qua View và gọi các phương thức tương ứng từ Model.
các chương trình nhỏ bên trong là: connect_db,,load_data,insert_data,update_data,delete_data
cuối cùng là hàm main để chạy chương trình
# Kết quả:
![image](https://github.com/user-attachments/assets/8a09e3ff-bede-431d-95c6-4f40dfa094e1)
