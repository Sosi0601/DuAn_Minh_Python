def update_danhmuc(madm, tendm_moi):
    db = connect_db()
    if not db:
        print("❌ Không kết nối được CSDL")
        return

    try:
        cur = db.cursor()
        sql = "UPDATE danhmuc SET tendm = %s WHERE madm = %s"
        cur.execute(sql, (tendm_moi, madm))
        db.commit()

        if cur.rowcount > 0:
            print(f"✅ Cập nhật danh mục ID {madm} thành: {tendm_moi}")
        else:
            print(f"⚠️ Không tìm thấy danh mục ID {madm}")

    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        cur.close()
        db.close()
