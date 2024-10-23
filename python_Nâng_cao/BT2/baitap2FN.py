import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql

# Model
class DatabaseModel:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            return True, "Kết nối thành công!"
        except Exception as e:
            return False, f"Không thể kết nối tới cơ sở dữ liệu: {e}"

    def fetch_data(self, selected_columns):
        try:
            query = sql.SQL("SELECT {} FROM public.\"Thong_tin\"").format(
                sql.SQL(', ').join(map(sql.Identifier, selected_columns))
            )
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            raise Exception(f"Không thể tải dữ liệu: {e}")

    def insert_data(self, hoten, tuoi, gioitinh, quequan, cccd, ngaysinh):
        try:
            query = sql.SQL("""
                INSERT INTO public."Thong_tin" (hoten, tuoi, gioitinh, quequan, "CCCD", ngaysinh)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            self.cur.execute(query, (hoten, tuoi, gioitinh, quequan, cccd, ngaysinh))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Không thể thêm dữ liệu: {e}")

    def update_data(self, hoten, tuoi, gioitinh, quequan, ngaysinh, cccd):
        try:
            query = sql.SQL("""
                UPDATE public."Thong_tin"
                SET hoten = %s, tuoi = %s, gioitinh = %s, quequan = %s, ngaysinh = %s
                WHERE "CCCD" = %s
            """)
            self.cur.execute(query, (hoten, tuoi, gioitinh, quequan, ngaysinh, cccd))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Không thể cập nhật dữ liệu: {e}")

    def delete_data(self, cccd):
        try:
            query = sql.SQL("DELETE FROM public.\"Thong_tin\" WHERE \"CCCD\" = %s")
            self.cur.execute(query, (cccd,))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Không thể xóa dữ liệu: {e}")

# View
class DatabaseView:
    def __init__(self, root):
        self.root = root
        self.controller = None  # Gán controller sau
        self.root.title("Quản lý Thông tin Cá Nhân")
        self.root.geometry("900x700")
        self.columns = ["hoten", "tuoi", "gioitinh", "quequan", "CCCD", "ngaysinh"]
        self.column_vars = {col: tk.IntVar(value=1) for col in self.columns}
        self.create_widgets()

    def create_widgets(self):
        connection_frame = ttk.LabelFrame(self.root, text="Kết nối Database")
        connection_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(connection_frame, text="Database:").grid(row=0, column=0, padx=5, pady=5)
        self.db_name = ttk.Entry(connection_frame)
        self.db_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="User:").grid(row=0, column=2, padx=5, pady=5)
        self.user = ttk.Entry(connection_frame)
        self.user.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(connection_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password = ttk.Entry(connection_frame, show="*")
        self.password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Host:").grid(row=1, column=2, padx=5, pady=5)
        self.host = ttk.Entry(connection_frame)
        self.host.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(connection_frame, text="Kết nối", command=lambda: self.controller.connect_db()).grid(row=2, columnspan=4, pady=10)

        column_frame = ttk.LabelFrame(self.root, text="Chọn cột để hiển thị")
        column_frame.pack(pady=10, padx=10, fill="x")

        for i, col in enumerate(self.columns):
            tk.Checkbutton(column_frame, text=col, variable=self.column_vars[col]).grid(row=0, column=i, padx=10, pady=5)

        self.data_entry_frame = ttk.LabelFrame(self.root, text="Nhập dữ liệu")
        self.data_entry_frame.pack(pady=10, padx=10, fill="x")

        fields = ["Họ tên", "Tuổi", "Giới tính", "Quê quán", "CCCD", "Ngày sinh (YYYY-MM-DD)"]
        self.entries = {}
        for i, field in enumerate(fields):
            ttk.Label(self.data_entry_frame, text=field).grid(row=i, column=0, padx=5, pady=5)
            self.entries[field] = ttk.Entry(self.data_entry_frame)
            self.entries[field].grid(row=i, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill="x")

        ttk.Button(button_frame, text="Thêm", command=lambda: self.controller.insert_data()).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cập nhật", command=lambda: self.controller.update_data()).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa", command=lambda: self.controller.delete_data()).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(fill="both", expand=True)

    def set_controller(self, controller):
        self.controller = controller

# Controller
class DatabaseController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)  
    def connect_db(self):
        self.model.db_name = self.view.db_name.get()
        self.model.user = self.view.user.get()
        self.model.password = self.view.password.get()
        self.model.host = self.view.host.get()
        self.model.port = '5432'
        success, message = self.model.connect()
        if success:
            messagebox.showinfo("Success", message)
            self.load_data()
        else:
            messagebox.showerror("Error", message)

    def load_data(self):
        selected_columns = [col for col in self.view.columns if self.view.column_vars[col].get() == 1]
        if not selected_columns:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một cột!")
            return
        try:
            rows = self.model.fetch_data(selected_columns)
            self.view.tree["columns"] = selected_columns
            for col in selected_columns:
                self.view.tree.heading(col, text=col)
            for row in self.view.tree.get_children():
                self.view.tree.delete(row)
            for row in rows:
                self.view.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_data(self):
        try:
            hoten = self.view.entries["Họ tên"].get()
            tuoi = self.view.entries["Tuổi"].get()
            gioitinh = self.view.entries["Giới tính"].get()
            quequan = self.view.entries["Quê quán"].get()
            cccd = self.view.entries["CCCD"].get()
            ngaysinh = self.view.entries["Ngày sinh (YYYY-MM-DD)"].get()
            self.model.insert_data(hoten, tuoi, gioitinh, quequan, cccd, ngaysinh)
            messagebox.showinfo("Success", "Dữ liệu đã được thêm!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_data(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Vui lòng chọn một hàng để cập nhật")
            return
        try:
            hoten = self.view.entries["Họ tên"].get()
            tuoi = self.view.entries["Tuổi"].get()
            gioitinh = self.view.entries["Giới tính"].get()
            quequan = self.view.entries["Quê quán"].get()
            cccd = self.view.entries["CCCD"].get()
            ngaysinh = self.view.entries["Ngày sinh (YYYY-MM-DD)"].get()
            self.model.update_data(hoten, tuoi, gioitinh, quequan, ngaysinh, cccd)
            messagebox.showinfo("Success", "Dữ liệu đã được cập nhật!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_data(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Vui lòng chọn một hàng để xóa")
            return
        try:
            selected_cccd = self.view.tree.item(selected_item, 'values')[4]
            self.model.delete_data(selected_cccd)
            messagebox.showinfo("Success", "Dữ liệu đã được xóa!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Main
if __name__ == "__main__":
    root = tk.Tk()
    model = DatabaseModel(db_name='db_cacu', user='postgres', password='postgres', host='localhost', port='5432')
    view = DatabaseView(root)
    controller = DatabaseController(model, view)
    root.mainloop()
