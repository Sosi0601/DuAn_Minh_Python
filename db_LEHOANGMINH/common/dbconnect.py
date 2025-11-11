import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='qlpc'
        )
        if connection.is_connected():
            print("✅ Kết nối MySQL thành công")
            return connection

    except Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")
        return None
