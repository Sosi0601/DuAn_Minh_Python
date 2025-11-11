from common.danhmuc import update_mota_danhmuc

madm = int(input("Nhập ID danh mục cần cập nhật mô tả: "))
mo_ta = input("Nhập mô tả mới: ")

update_mota_danhmuc(madm, mo_ta)
