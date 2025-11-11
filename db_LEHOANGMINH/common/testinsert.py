import sys
sys.path.append(r"C:\Users\lehoa\PycharmProjects\PythonProject2")  # thư mục gốc dự án

from common.danhmuc import insert_danhmuc

name = input("Nhập tên danh mục: ")
insert_danhmuc(name)
