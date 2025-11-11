# common/testupdatedanhmuc.py
from common.danhmuc import update_danhmuc

madm = int(input("Nhập ID danh mục cần cập nhật: "))
tendm_moi = input("Nhập tên mới: ")
update_danhmuc(madm, tendm_moi)
