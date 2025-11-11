import sys
sys.path.append("C:/Users/lehoa/PycharmProjects/PythonProject2/chuongtrinh")
from dbconnect import connect_db

db = connect_db()

if db:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM danhmuc")
    data = cursor.fetchall()

    print("📌 Dữ liệu bảng danhmuc:")
    for row in data:
        print(row)

    cursor.close()
    db.close()
