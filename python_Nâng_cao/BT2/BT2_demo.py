import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Thông tin Cá Nhân")
        self.root.geometry("900x700")

        # Database connection fields
        self.db_name = tk.StringVar(value='db_cacu')  
        self.user = tk.StringVar(value='postgres')  
        self.password = tk.StringVar(value='hainguyen752004')  
        self.host = tk.StringVar(value='localhost')  
        self.port = tk.StringVar(value='5432') 

        # Các cột mà người dùng có thể chọn
        self.columns = ["hoten", "tuoi", "gioitinh", "quequan", "CCCD", "ngaysinh"]
        self.column_vars = {col: tk.IntVar(value=1) for col in self.columns}  # Lưu trạng thái checkbox

        # Create the GUI elements
        self.create_widgets()
        self.conn = None
        self.cur = None

    def create_widgets(self):
        # Connection section
        connection_frame = ttk.LabelFrame(self.root, text="Kết nối Database")
        connection_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(connection_frame, text="Database:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="User:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.user).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(connection_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Host:").grid(row=1, column=2, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.host).grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=2, columnspan=4, pady=10)

        # Cột lựa chọn để hiển thị
        column_frame = ttk.LabelFrame(self.root, text="Chọn cột để hiển thị")
        column_frame.pack(pady=10, padx=10, fill="x")

        for i, col in enumerate(self.columns):
            tk.Checkbutton(column_frame, text=col, variable=self.column_vars[col]).grid(row=0, column=i, padx=10, pady=5)

        # Data entry frame
        self.data_entry_frame = ttk.LabelFrame(self.root, text="Nhập dữ liệu")
        self.data_entry_frame.pack(pady=10, padx=10, fill="x")

        # Fields for data entry
        ttk.Label(self.data_entry_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5)
        self.hoten_entry = ttk.Entry(self.data_entry_frame)
        self.hoten_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.data_entry_frame, text="Tuổi:").grid(row=1, column=0, padx=5, pady=5)
        self.tuoi_entry = ttk.Entry(self.data_entry_frame)
        self.tuoi_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.data_entry_frame, text="Giới tính:").grid(row=2, column=0, padx=5, pady=5)
        self.gioitinh_entry = ttk.Entry(self.data_entry_frame)
        self.gioitinh_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.data_entry_frame, text="Quê quán:").grid(row=3, column=0, padx=5, pady=5)
        self.quequan_entry = ttk.Entry(self.data_entry_frame)
        self.quequan_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.data_entry_frame, text="CCCD:").grid(row=4, column=0, padx=5, pady=5)
        self.cccd_entry = ttk.Entry(self.data_entry_frame)
        self.cccd_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.data_entry_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=5, column=0, padx=5, pady=5)
        self.ngaysinh_entry = ttk.Entry(self.data_entry_frame)
        self.ngaysinh_entry.grid(row=5, column=1, padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill="x")

        ttk.Button(button_frame, text="Thêm", command=self.insert_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cập nhật", command=self.update_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_data).pack(side="left", padx=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(fill="both", expand=True)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Kết nối thành công!")
            # Hiển thị dữ liệu sau khi kết nối thành công
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Không thể kết nối tới cơ sở dữ liệu: {e}")

    def load_data(self):
        try:
            if self.conn is None:
                self.connect_db()

            # Lấy danh sách các cột được chọn
            selected_columns = [col for col in self.columns if self.column_vars[col].get() == 1]

            if not selected_columns:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một cột!")
                return

            # Tạo câu truy vấn chỉ lấy những cột đã chọn
            query = sql.SQL("SELECT {} FROM public.\"Thong_tin\"").format(
                sql.SQL(', ').join(map(sql.Identifier, selected_columns))
            )

            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Xóa dữ liệu cũ trong Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Cập nhật cột trong Treeview dựa trên cột được chọn
            self.tree["columns"] = selected_columns
            for col in selected_columns:
                self.tree.heading(col, text=col)

            # Thêm dữ liệu vào Treeview
            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Không thể tải dữ liệu: {e}")

    def insert_data(self):
        hoten = self.hoten_entry.get()
        tuoi = self.tuoi_entry.get()
        gioitinh = self.gioitinh_entry.get()
        quequan = self.quequan_entry.get()
        cccd = self.cccd_entry.get()
        ngaysinh = self.ngaysinh_entry.get()

        try:
            query = sql.SQL("""
                INSERT INTO public."Thong_tin" (hoten, tuoi, gioitinh, quequan, "CCCD", ngaysinh)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            self.cur.execute(query, (hoten, tuoi, gioitinh, quequan, cccd, ngaysinh))
            self.conn.commit()
            messagebox.showinfo("Success", "Dữ liệu đã được thêm!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Không thể thêm dữ liệu: {e}")

    def update_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Vui lòng chọn một hàng để cập nhật")
            return

        hoten = self.hoten_entry.get()
        tuoi = self.tuoi_entry.get()
        gioitinh = self.gioitinh_entry.get()
        quequan = self.quequan_entry.get()
        cccd = self.cccd_entry.get()
        ngaysinh = self.ngaysinh_entry.get()

        try:
            query = sql.SQL("""
                UPDATE public."Thong_tin"
                SET hoten = %s, tuoi = %s, gioitinh = %s, quequan = %s, ngaysinh = %s
                WHERE "CCCD" = %s
            """)
            self.cur.execute(query, (hoten, tuoi, gioitinh, quequan, ngaysinh, cccd))
            self.conn.commit()
            messagebox.showinfo("Success", "Dữ liệu đã được cập nhật!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Không thể cập nhật dữ liệu: {e}")

    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Vui lòng chọn một hàng để xóa")
            return

        try:
            selected_cccd = self.tree.item(selected_item, 'values')[4]
            query = sql.SQL("DELETE FROM public.\"Thong_tin\" WHERE \"CCCD\" = %s")
            self.cur.execute(query, (selected_cccd,))
            self.conn.commit()
            messagebox.showinfo("Success", "Dữ liệu đã được xóa!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Không thể xóa dữ liệu: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
