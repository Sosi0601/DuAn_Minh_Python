import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ====== CẤU HÌNH KẾT NỐI MYSQL ======
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "qlpc"   # đổi nếu DB bạn khác

# ====== LỚP LÀM VIỆC VỚI CSDL ======
class DanhMucRepo:
    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn and self.conn.is_connected():
            return
        try:
            self.conn = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
            )
        except Error as e:
            messagebox.showerror("Lỗi kết nối", f"Không kết nối được MySQL:\n{e}")
            raise

    def fetch_all(self):
        """Lấy (madm, tendm, mo_ta)"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute("SELECT madm, tendm, COALESCE(mo_ta,'') FROM danhmuc ORDER BY madm ASC")
            return cur.fetchall()

    def insert(self, tendm: str, mo_ta: str | None):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO danhmuc (tendm, mo_ta) VALUES (%s, %s)", (tendm, mo_ta))
            self.conn.commit()
            return cur.lastrowid

    def update(self, madm: int, tendm: str, mo_ta: str | None):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute("UPDATE danhmuc SET tendm=%s, mo_ta=%s WHERE madm=%s", (tendm, mo_ta, madm))
            self.conn.commit()
            return cur.rowcount

    def delete(self, madm: int):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM danhmuc WHERE madm=%s", (madm,))
            self.conn.commit()
            return cur.rowcount

# ====== ỨNG DỤNG TKINTER ======
class DanhMucApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý Danh mục ")
        self.geometry("860x600")
        self.minsize(820, 560)

        self.repo = DanhMucRepo()

        # ---- Khung nhập liệu
        form = ttk.LabelFrame(self, text="Thông tin danh mục")
        form.pack(fill="x", padx=12, pady=10)

        # Mã
        ttk.Label(form, text="Mã danh mục:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.var_madm = tk.StringVar()
        self.ent_madm = ttk.Entry(form, textvariable=self.var_madm, state="readonly", width=18)
        self.ent_madm.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        # Tên
        ttk.Label(form, text="Tên danh mục:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.var_tendm = tk.StringVar()
        self.ent_tendm = ttk.Entry(form, textvariable=self.var_tendm, width=40)
        self.ent_tendm.grid(row=0, column=3, padx=8, pady=8, sticky="w")

        # Mô tả
        ttk.Label(form, text="Mô tả:").grid(row=1, column=0, padx=8, pady=(0,8), sticky="nw")
        self.txt_mota = tk.Text(form, height=5, width=70, wrap="word")
        self.txt_mota.grid(row=1, column=1, columnspan=3, padx=8, pady=(0,8), sticky="we")

        # ---- Nút chức năng
        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=12, pady=(0,10))

        ttk.Button(btns, text="➕ Thêm",  command=self.on_add).pack(side="left", padx=5)
        ttk.Button(btns, text="✏️ Sửa",   command=self.on_update).pack(side="left", padx=5)
        ttk.Button(btns, text="🗑️ Xóa",   command=self.on_delete).pack(side="left", padx=5)
        ttk.Button(btns, text="🧹 Làm mới", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(btns, text="🔄 Tải lại", command=self.load_data).pack(side="left", padx=5)

        # ---- Bảng hiển thị
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=12, pady=10)

        columns = ("madm", "tendm", "mo_ta")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("madm", text="Mã")
        self.tree.heading("tendm", text="Tên danh mục")
        self.tree.heading("mo_ta", text="Mô tả (rút gọn)")
        self.tree.column("madm",  width=80, anchor="center")
        self.tree.column("tendm", width=250, anchor="w")
        self.tree.column("mo_ta", width=460, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Bind
        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)
        self.bind("<Return>", lambda e: self.on_add())  # Enter = Thêm nhanh

        self.load_data()

    # ---- Helpers
    @staticmethod
    def _short(text: str, limit: int = 140) -> str:
        if not text:
            return ""
        text = text.strip()
        return text if len(text) <= limit else text[:limit].rstrip() + "…"

    def clear_form(self):
        self.var_madm.set("")
        self.var_tendm.set("")
        self.txt_mota.delete("1.0", "end")
        self.ent_tendm.focus()

    def load_data(self):
        try:
            rows = self.repo.fetch_all()  # [(madm, tendm, mo_ta), ...]
            for i in self.tree.get_children():
                self.tree.delete(i)
            # Nhét cả mô tả FULL vào 'values'; bảng hiển thị bản rút gọn
            for madm, tendm, mo_ta in rows:
                self.tree.insert("", "end", values=(madm, tendm, mo_ta),  # giữ full trong values
                                 tags=("row",))
                # đổi text hiển thị của cột mô tả thành bản rút gọn
                item = self.tree.get_children()[-1]
                cur_vals = list(self.tree.item(item, "values"))
                cur_vals[2] = self._short(mo_ta)
                self.tree.item(item, values=tuple(cur_vals))
        except Exception as e:
            messagebox.showerror("Lỗi tải dữ liệu", str(e))

    def on_select_row(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        # lấy lại bản FULL từ DB values ban đầu:
        # mẹo: lấy values hiện tại (đã rút gọn) và query lại bản full bằng fetch_all hoặc
        # lưu full trong item 'iid' → ở trên ta đã giữ full rồi trước khi rút gọn.
        # Vì chúng ta đã thay values để rút gọn, nên ta đọc lại từ DB theo id cho chắc.
        try:
            item = sel[0]
            values = self.tree.item(item, "values")
            madm = values[0]
            self.var_madm.set(madm)
            self.var_tendm.set(values[1])

            # Lấy full từ DB (đảm bảo đúng)
            for r_madm, r_ten, r_mo_ta in self.repo.fetch_all():
                if str(r_madm) == str(madm):
                    self.txt_mota.delete("1.0", "end")
                    self.txt_mota.insert("1.0", r_mo_ta or "")
                    break
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ---- CRUD actions
    def on_add(self):
        tendm = self.var_tendm.get().strip()
        mo_ta = self.txt_mota.get("1.0", "end").strip()
        if not tendm:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên danh mục")
            self.ent_tendm.focus()
            return
        try:
            new_id = self.repo.insert(tendm, mo_ta)
            messagebox.showinfo("Thành công", f"Đã thêm danh mục (ID={new_id})")
            self.clear_form()
            self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi thêm", str(e))

    def on_update(self):
        madm = self.var_madm.get().strip()
        tendm = self.var_tendm.get().strip()
        mo_ta = self.txt_mota.get("1.0", "end").strip()
        if not madm:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn một danh mục để sửa")
            return
        if not tendm:
            messagebox.showwarning("Thiếu dữ liệu", "Tên danh mục không được rỗng")
            self.ent_tendm.focus()
            return
        try:
            cnt = self.repo.update(int(madm), tendm, mo_ta)
            if cnt > 0:
                messagebox.showinfo("Thành công", f"Đã cập nhật danh mục ID={madm}")
                self.load_data()
            else:
                messagebox.showwarning("Không thay đổi", "Không tìm thấy danh mục hoặc dữ liệu không đổi")
        except Error as e:
            messagebox.showerror("Lỗi cập nhật", str(e))

    def on_delete(self):
        madm = self.var_madm.get().strip()
        if not madm:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn một danh mục để xóa")
            return
        if not messagebox.askyesno("Xác nhận xóa", f"Bạn chắc chắn muốn xóa danh mục ID={madm}?"):
            return
        try:
            cnt = self.repo.delete(int(madm))
            if cnt > 0:
                messagebox.showinfo("Thành công", f"Đã xóa danh mục ID={madm}")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showwarning("Không tìm thấy", "ID không tồn tại")
        except Error as e:
            messagebox.showerror("Lỗi xóa", str(e))

if __name__ == "__main__":
    app = DanhMucApp()
    app.mainloop()
