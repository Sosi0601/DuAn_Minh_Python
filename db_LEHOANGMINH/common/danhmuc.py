# common/danhmuc.py
from .dbconnect import connect_db

def insert_danhmuc(tendm):
    db = connect_db()
    if not db:
        print("❌ Không kết nối được CSDL")
        return
    try:
        cur = db.cursor()
        cur.execute("INSERT INTO danhmuc (tendm) VALUES (%s)", (tendm,))
        db.commit()
        print(f"✅ Thêm danh mục: {tendm}")
    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        try: cur.close()
        except: pass
        db.close()

def delete_danhmuc(madm):
    db = connect_db()
    if not db:
        print("❌ Không kết nối được CSDL")
        return
    try:
        cur = db.cursor()
        cur.execute("DELETE FROM danhmuc WHERE madm = %s", (madm,))
        db.commit()
        if cur.rowcount > 0:
            print(f"🗑️  Đã xóa danh mục ID {madm}")
        else:
            print(f"⚠️  Không tìm thấy danh mục ID {madm}")
    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        try: cur.close()
        except: pass
        db.close()

def update_danhmuc(madm, tendm_moi):
    """CẬP NHẬT tên danh mục theo ID."""
    db = connect_db()
    if not db:
        print("❌ Không kết nối được CSDL")
        return
    try:
        cur = db.cursor()
        cur.execute("UPDATE danhmuc SET tendm = %s WHERE madm = %s", (tendm_moi, madm))
        db.commit()
        if cur.rowcount > 0:
            print(f"✅ Cập nhật ID {madm} -> {tendm_moi}")
        else:
            print(f"⚠️ Không tìm thấy danh mục ID {madm}")
    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        try: cur.close()
        except: pass
        db.close()

def list_danhmuc():
    """Tiện kiểm tra nhanh dữ liệu."""
    db = connect_db()
    if not db:
        print("❌ Không kết nối được CSDL")
        return []
    try:
        cur = db.cursor()
        cur.execute("SELECT madm, tendm FROM danhmuc ORDER BY madm")
        rows = cur.fetchall()
        for r in rows:
            print(r)
        return rows
    except Exception as e:
        print("❌ Lỗi:", e)
        return []
    finally:
        try: cur.close()
        except: pass
        db.close()
def list_danhmuc():
    db = connect_db()
    if not db:
        print("❌ Không kết nối được CSDL")
        return []

    try:
        cur = db.cursor()
        cur.execute("SELECT madm, tendm FROM danhmuc ORDER BY madm ASC")
        rows = cur.fetchall()

        if rows:
            print("📂 DANH SÁCH DANH MỤC:")
            for r in rows:
                print(f"ID: {r[0]} | Tên: {r[1]}")
        else:
            print("⚠️ Chưa có danh mục nào trong CSDL")

        return rows

    except Exception as e:
        print("❌ Lỗi:", e)
        return []

    finally:
        try: cur.close()
        except: pass
        db.close()


def update_mota_danhmuc(madm, mo_ta):
    db = connect_db()
    if not db:
        print("❌ Không kết nối được CSDL")
        return

    try:
        cur = db.cursor()
        sql = "UPDATE danhmuc SET mo_ta = %s WHERE madm = %s"
        cur.execute(sql, (mo_ta, madm))
        db.commit()

        if cur.rowcount > 0:
            print(f"✅ Cập nhật mô tả danh mục ID {madm}")
        else:
            print(f"⚠️ Không tìm thấy danh mục ID {madm}")

    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        try:
            cur.close()
        except:
            pass
        db.close()
