import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import psycopg2
from hashlib import sha256

def connect_db():
    return psycopg2.connect(
        dbname="quanlykhachsan",
        user="postgres",
        password="123456",
        host="localhost"
    )

def open_manager_interface(window, db_connection):
    window.destroy()
    manager_window = tk.Tk()
    manager_window.title("Quản lý khách sạn")
    manager_window.geometry("600x400")

    ttk.Label(manager_window, text="Xin chào, Quản lý").grid(row=0, column=1, pady=10)

    # Nút xem trạng thái phòng
    ttk.Button(manager_window, text="Xem trạng thái phòng", command=lambda: view_room_status(db_connection)).grid(row=1, column=1, pady=10)

    # Nút xem tổng doanh thu
    ttk.Button(manager_window, text="Xem tổng doanh thu", command=lambda: view_total_revenue(db_connection)).grid(row=4, column=1, pady=10)

    # Nút xem phòng trống
    ttk.Button(manager_window, text="Xem phòng trống", command=lambda: view_available_rooms(db_connection)).grid(row=5, column=1, pady=10)

    manager_window.mainloop()

def open_search_and_booking_interface(main_window, db_connection, user_info):
    main_window.destroy()  # Close the login window
    window = tk.Tk()
    window.title("Tìm kiếm và đặt phòng")
    window.geometry("500x400")

    ttk.Label(window, text=f"Xin chào, {user_info[1]}").grid(row=0, column=1)

    ttk.Label(window, text="Số lượng giường:").grid(row=1, column=0)
    bed_count_var = tk.StringVar()
    bed_count_combobox = ttk.Combobox(window, textvariable=bed_count_var, values=["1", "2"])
    bed_count_combobox.grid(row=1, column=1)
    bed_count_combobox.set("1")  # Default value

    ttk.Label(window, text="Giá tối đa:").grid(row=2, column=0)
    price_var = tk.StringVar()
    price_entry = ttk.Entry(window, textvariable=price_var)
    price_entry.grid(row=2, column=1)

    ttk.Button(window, text="Tìm Phòng", command=lambda: search_available_rooms(bed_count_var.get(), price_var.get(), db_connection, user_info)).grid(row=3, column=1, pady=10)

    # Nút trả phòng
    ttk.Button(window, text="Trả phòng", command=lambda: open_return_room_interface(window, db_connection, user_info)).grid(row=4, column=1, pady=10)

    window.mainloop()

def view_total_revenue(connection):
    """ Hiển thị tổng doanh thu đã nhận từ các hóa đơn """
    cursor = connection.cursor()
    try:
        # Truy vấn tính tổng doanh thu
        cursor.execute("SELECT SUM(tongtien) FROM hoadon")
        total_revenue = cursor.fetchone()[0]  # Lấy tổng doanh thu

        # Nếu chưa có hóa đơn nào, tổng doanh thu là 0
        if total_revenue is None:
            total_revenue = 0

        # Hiển thị tổng doanh thu
        messagebox.showinfo("Tổng doanh thu", f"Tổng doanh thu đã nhận: {total_revenue} VND")
    except psycopg2.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tính tổng doanh thu: {str(e)}")
    finally:
        cursor.close()

def view_room_status(connection):
    """ Hiển thị danh sách phòng, trạng thái và khách hàng nếu có """
    cursor = connection.cursor()
    try:
        # Truy vấn lấy thông tin phòng và tình trạng
        cursor.execute("""
            SELECT phong.idphong, phong.tinhtrang, phong.tiennghi, khachhang.ten
            FROM phong
            LEFT JOIN lichsuluutru ON phong.idphong = lichsuluutru.idphong AND lichsuluutru.ngayra IS NULL
            LEFT JOIN khachhang ON lichsuluutru.idkhachhang = khachhang.id;
        """)
        rooms = cursor.fetchall()

        # Tạo cửa sổ hiển thị
        status_window = tk.Toplevel()
        status_window.title("Trạng Thái Phòng")
        status_window.geometry("500x300")

        # Tiêu đề cột
        ttk.Label(status_window, text="ID Phòng", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(status_window, text="Tình Trạng", font=('Arial', 12, 'bold')).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(status_window, text="Tiện Nghi", font=('Arial', 12, 'bold')).grid(row=0, column=2, padx=10, pady=5)
        ttk.Label(status_window, text="Khách Hàng", font=('Arial', 12, 'bold')).grid(row=0, column=3, padx=10, pady=5)

        # Hiển thị thông tin từng phòng
        for idx, (room_id, status, amenities, customer_name) in enumerate(rooms, start=1):
            customer_display = customer_name if customer_name else "Không có"
            ttk.Label(status_window, text=room_id).grid(row=idx, column=0, padx=10, pady=5)
            ttk.Label(status_window, text=status).grid(row=idx, column=1, padx=10, pady=5)
            ttk.Label(status_window, text=amenities).grid(row=idx, column=2, padx=10, pady=5)
            ttk.Label(status_window, text=customer_display).grid(row=idx, column=3, padx=10, pady=5)
        
    except psycopg2.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy thông tin phòng: {str(e)}")
    finally:
        cursor.close()

def view_available_rooms(connection):
    """ Hiển thị danh sách phòng trống và khách hàng nếu có ai đang ở """
    cursor = connection.cursor()
    try:
        # Truy vấn lấy thông tin phòng trống và phòng đang được sử dụng
        cursor.execute("""
            SELECT phong.idphong, phong.tinhtrang, phong.tiennghi, khachhang.ten
            FROM phong
            LEFT JOIN lichsuluutru ON phong.idphong = lichsuluutru.idphong AND lichsuluutru.ngayra IS NULL
            LEFT JOIN khachhang ON lichsuluutru.idkhachhang = khachhang.id;
        """)
        rooms = cursor.fetchall()

        # Tạo cửa sổ hiển thị
        available_window = tk.Toplevel()
        available_window.title("Phòng Trống và Phòng Đang Sử Dụng")
        available_window.geometry("600x400")

        # Tiêu đề cột
        ttk.Label(available_window, text="ID Phòng", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(available_window, text="Tình Trạng", font=('Arial', 12, 'bold')).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(available_window, text="Tiện Nghi", font=('Arial', 12, 'bold')).grid(row=0, column=2, padx=10, pady=5)
        ttk.Label(available_window, text="Khách Hàng", font=('Arial', 12, 'bold')).grid(row=0, column=3, padx=10, pady=5)

        # Hiển thị thông tin từng phòng
        for idx, (room_id, status, amenities, customer_name) in enumerate(rooms, start=1):
            customer_display = customer_name if customer_name else "Không có"
            ttk.Label(available_window, text=room_id).grid(row=idx, column=0, padx=10, pady=5)
            ttk.Label(available_window, text=status).grid(row=idx, column=1, padx=10, pady=5)
            ttk.Label(available_window, text=amenities).grid(row=idx, column=2, padx=10, pady=5)
            ttk.Label(available_window, text=customer_display).grid(row=idx, column=3, padx=10, pady=5)
        
    except psycopg2.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy thông tin phòng trống và phòng đang sử dụng: {str(e)}")
    finally:
        cursor.close()

def book_room(room_id, user_info, db_connection):
    booking_window = tk.Toplevel()
    booking_window.title("Đặt phòng")
    booking_window.geometry("300x200")

    ttk.Label(booking_window, text="Đặt phòng số: " + str(room_id)).grid(row=0, column=0, columnspan=2)

    ttk.Label(booking_window, text="Ngày nhận phòng:").grid(row=1, column=0)
    check_in_var = tk.StringVar()
    check_in_entry = ttk.Entry(booking_window, textvariable=check_in_var)
    check_in_entry.grid(row=1, column=1)

    ttk.Label(booking_window, text="Ngày trả phòng:").grid(row=2, column=0)
    check_out_var = tk.StringVar()
    check_out_entry = ttk.Entry(booking_window, textvariable=check_out_var)
    check_out_entry.grid(row=2, column=1)

    ttk.Button(booking_window, text="Xác nhận đặt phòng", command=lambda: confirm_booking(
        room_id, user_info[0], check_in_var.get(), check_out_var.get(), db_connection, booking_window
    )).grid(row=3, column=0, columnspan=2)

def confirm_booking(room_id, user_id, check_in, check_out, connection, window):
    cursor = connection.cursor()
    try:
        # Đảm bảo room_id và user_id là số nguyên
        room_id = int(room_id)
        user_id = int(user_id)

        # Chuyển đổi chuỗi ngày thành đối tượng datetime
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')

        # Tính số ngày lưu trú
        delta = check_out_date - check_in_date
        num_days = delta.days  # Số ngày lưu trú

        if num_days <= 0:
            messagebox.showerror("Lỗi", "Ngày trả phòng phải lớn hơn ngày nhận phòng.")
            return

        # Lấy giá phòng từ cơ sở dữ liệu
        cursor.execute("SELECT gia FROM phong WHERE idphong = %s", (room_id,))
        room_price = cursor.fetchone()[0]  # Giả sử giá phòng lấy từ cơ sở dữ liệu

        # Insert booking into DatPhong
        cursor.execute("INSERT INTO datphong (idkhachhang, idphong, ngaynhanphong, ngaytraphong) VALUES (%s, %s, %s, %s) RETURNING iddatphong",
                       (user_id, room_id, check_in_date, check_out_date))
        booking_id = cursor.fetchone()[0]

        # Cập nhật tình trạng phòng
        cursor.execute("UPDATE phong SET tinhtrang = 'đã đặt' WHERE idphong = %s", (room_id,))

        # Thêm thông tin vào lịch sử lưu trú
        cursor.execute("INSERT INTO lichsuluutru (idkhachhang, idphong, ngayvao) VALUES (%s, %s, %s)",
                       (user_id, room_id, check_in_date))

        connection.commit()
        messagebox.showinfo("Thành công", "Phòng đã được đặt thành công!")
        window.destroy()

    except psycopg2.Error as e:
        connection.rollback()
        messagebox.showerror("Lỗi", "Không thể đặt phòng: " + str(e))
    finally:
        cursor.close()

def return_room(room_id, connection, user_info):
    cursor = connection.cursor()
    try:
        # Kiểm tra nếu phòng đang trống
        cursor.execute("SELECT tinhtrang FROM phong WHERE idphong = %s", (room_id,))
        room_status = cursor.fetchone()

        if room_status is None or room_status[0] == 'trống':
            messagebox.showerror("Lỗi", "Phòng này hiện đang trống hoặc không tồn tại.")
            return

        # Lấy thông tin đặt phòng
        cursor.execute("SELECT ngaynhanphong, ngaytraphong, iddatphong FROM datphong WHERE idkhachhang = %s AND idphong = %s AND ngaytraphong IS NOT NULL",
                       (user_info[0], room_id))
        booking_info = cursor.fetchone()

        if booking_info is None:
            messagebox.showinfo("Lỗi", "Không có thông tin đặt phòng cho phòng này.")
            return

        # Tính số ngày đã ở
        check_in_date, check_out_date, booking_id = booking_info
        delta = check_out_date - check_in_date
        num_days = delta.days

        if num_days <= 0:
            messagebox.showerror("Lỗi", "Ngày trả phòng phải lớn hơn ngày nhận phòng.")
            return

        # Lấy giá phòng từ cơ sở dữ liệu
        cursor.execute("SELECT gia FROM phong WHERE idphong = %s", (room_id,))
        room_price = cursor.fetchone()[0]

        # Tính tổng tiền
        total_cost = num_days * room_price

        # Cập nhật trạng thái phòng và lưu trữ thông tin hóa đơn
        cursor.execute("UPDATE phong SET tinhtrang = 'trống' WHERE idphong = %s", (room_id,))
        cursor.execute("INSERT INTO hoadon (iddatphong, tongtien, ngaythanhtoan) VALUES (%s, %s, %s)",
                       (booking_id, total_cost, datetime.now()))

        # Cập nhật ngày ra trong lịch sử lưu trú
        cursor.execute("UPDATE lichsuluutru SET ngayra = %s WHERE idkhachhang = %s AND idphong = %s AND ngayra IS NULL",
                       (check_out_date, user_info[0], room_id))

        connection.commit()
        messagebox.showinfo("Thành công", f"Trả phòng thành công! Tổng tiền phải trả là: {total_cost} VND")

    except psycopg2.Error as e:
        connection.rollback()
        messagebox.showerror("Lỗi", "Không thể trả phòng: " + str(e))
    finally:
        cursor.close()

def open_return_room_interface(window, db_connection, user_info):
    return_window = tk.Toplevel(window)
    return_window.title("Trả phòng")
    return_window.geometry("400x200")

    ttk.Label(return_window, text="Nhập ID phòng muốn trả:").grid(row=0, column=0, padx=10, pady=10)
    room_id_var = tk.StringVar()
    room_id_entry = ttk.Entry(return_window, textvariable=room_id_var)
    room_id_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Button(return_window, text="Trả phòng", command=lambda: return_room(room_id_var.get(), db_connection, user_info)).grid(row=1, column=1, pady=10)

def search_available_rooms(bed_count, max_price, connection, user_info):
    cursor = connection.cursor()
    try:
        if not max_price.isdigit():
            messagebox.showerror("Lỗi", "Giá tối đa phải là một số nguyên hợp lệ.")
            return
        
        query = "SELECT idphong, gia, tiennghi FROM phong WHERE tinhtrang = 'trống' AND soluonggiuong = %s AND gia <= %s;"
        cursor.execute(query, (bed_count, max_price))
        rooms = cursor.fetchall()
        if rooms:
            room_selection_window = tk.Toplevel()
            room_selection_window.title("Chọn phòng để đặt")
            room_selection_window.geometry("400x400")
            ttk.Label(room_selection_window, text="Chọn một phòng để đặt:").grid(row=0, column=0)
            for idx, room in enumerate(rooms, start=1):
                room_info = f"Phòng {room[0]} - Giá: {room[1]} VND - Tiện nghi: {room[2]}"
                ttk.Button(room_selection_window, text=room_info, command=lambda room_id=room[0]: book_room(room_id, user_info, connection)).grid(row=idx, column=0)
        else:
            messagebox.showinfo("Phòng trống", "Không có phòng trống phù hợp.")
    except psycopg2.Error as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm phòng: {str(e)}")
    finally:
        cursor.close()

def register_user(name, phone, email, cmnd, password, window):
    connection = connect_db()
    cursor = connection.cursor()
    hashed_password = sha256(password.encode()).hexdigest()  # Mã hóa mật khẩu
    try:
        cursor.execute("INSERT INTO khachhang (ten, sodienthoai, email, cmnd_hochieu, matkhau) VALUES (%s, %s, %s, %s, %s)",
                       (name, phone, email, cmnd, hashed_password))
        connection.commit()
        messagebox.showinfo("Success", "Đăng ký thành công.")
        open_search_and_booking_interface(window, connection, (name, phone, email, cmnd, hashed_password))
    except psycopg2.Error as e:
        connection.rollback()
        messagebox.showerror("Error", "Đăng ký thất bại: " + str(e))
    finally:
        cursor.close()
        connection.close()

def login_user(phone, password, window):
    connection = connect_db()
    cursor = connection.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    try:
        # Lấy thông tin tài khoản từ cơ sở dữ liệu
        cursor.execute("SELECT * FROM khachhang WHERE sodienthoai = %s AND matkhau = %s", (phone, hashed_password))
        user = cursor.fetchone()
        if user:
            # Kiểm tra vai trò của người dùng, giả sử cột `vaitro` nằm ở vị trí cuối trong bảng khachhang
            if user[-1] == 'manager':
                messagebox.showinfo("Success", "Đăng nhập thành công với vai trò Quản lý.")
                open_manager_interface(window, connection)
            else:
                messagebox.showinfo("Success", "Đăng nhập thành công.")
                open_search_and_booking_interface(window, connection, user)
        else:
            messagebox.showerror("Error", "Số điện thoại hoặc mật khẩu không đúng.")
    finally:
        cursor.close()
        connection.close()

def create_login_ui():
    window = tk.Tk()
    window.title("Đăng nhập / Đăng ký")
    window.geometry("400x300")

    tab_control = ttk.Notebook(window)

    # Login tab
    login_tab = ttk.Frame(tab_control)
    ttk.Label(login_tab, text="Số điện thoại:").grid(row=0, column=0)
    phone_entry = ttk.Entry(login_tab)
    phone_entry.grid(row=0, column=1)

    ttk.Label(login_tab, text="Mật khẩu:").grid(row=1, column=0)
    password_entry = ttk.Entry(login_tab, show="*")
    password_entry.grid(row=1, column=1)

    ttk.Button(login_tab, text="Đăng nhập", command=lambda: login_user(phone_entry.get(), password_entry.get(), window)).grid(row=2, column=1, pady=10)

    tab_control.add(login_tab, text="Đăng nhập")

    # Register tab
    register_tab = ttk.Frame(tab_control)
    ttk.Label(register_tab, text="Tên:").grid(row=0, column=0)
    name_entry = ttk.Entry(register_tab)
    name_entry.grid(row=0, column=1)

    ttk.Label(register_tab, text="Số điện thoại:").grid(row=1, column=0)
    reg_phone_entry = ttk.Entry(register_tab)
    reg_phone_entry.grid(row=1, column=1)

    ttk.Label(register_tab, text="Email:").grid(row=2, column=0)
    email_entry = ttk.Entry(register_tab)
    email_entry.grid(row=2, column=1)

    ttk.Label(register_tab, text="CMND/Hộ chiếu:").grid(row=3, column=0)
    cmnd_entry = ttk.Entry(register_tab)
    cmnd_entry.grid(row=3, column=1)

    ttk.Label(register_tab, text="Mật khẩu:").grid(row=4, column=0)
    reg_password_entry = ttk.Entry(register_tab, show="*")
    reg_password_entry.grid(row=4, column=1)

    ttk.Button(register_tab, text="Đăng ký", command=lambda: register_user(name_entry.get(), reg_phone_entry.get(), email_entry.get(), cmnd_entry.get(), reg_password_entry.get(), window)).grid(row=5, column=1, pady=10)

    tab_control.add(register_tab, text="Đăng ký")

    tab_control.pack(expand=1, fill="both")

    window.mainloop()

create_login_ui()
