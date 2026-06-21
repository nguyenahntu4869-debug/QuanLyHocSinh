# managers.py - Logic nghiệp vụ: quản lý sinh viên, môn học, lớp HP, điểm
# Sử dụng các class từ models.py và file_handler.py

from models import SinhVien, MonHoc, LopHocPhan, BangDiem
from file_handler import (
    save_data, load_data, save_all, load_all,
    FILE_SINH_VIEN, FILE_MON_HOC, FILE_LOP_HOC_PHAN, FILE_DIEM
)
from utils import (
    vietnamese_sort_key,
    normalize_text,
    validate_mssv, validate_ho_ten, validate_ngay_sinh, validate_email,
    validate_ma_mon
)


class SinhVienManager:
    """Quản lý danh sách sinh viên: thêm, sửa, xóa, tìm kiếm, sắp xếp."""

    def __init__(self, ds_sinh_vien=None):
        self.ds_sinh_vien = ds_sinh_vien if ds_sinh_vien is not None else []
        self.sap_xep_mac_dinh()

    def sap_xep_mac_dinh(self):
        """Sắp xếp danh sách sinh viên theo tên tiếng Việt mặc định."""
        self.ds_sinh_vien.sort(key=lambda sv: vietnamese_sort_key(sv.ho_ten))

    def them(self, sv):
        """
        Thêm sinh viên mới vào danh sách.
        Kiểm tra trùng MSSV trước khi thêm.
        
        Returns:
            tuple: (bool, str) - (thành công, thông báo)
        """
        # Validate dữ liệu trước khi thêm
        ok, msg = validate_mssv(sv.mssv)
        if not ok:
            return False, msg
        ok, msg = validate_ho_ten(sv.ho_ten)
        if not ok:
            return False, msg
        ok, msg = validate_ngay_sinh(sv.ngay_sinh)
        if not ok:
            return False, msg
        ok, msg = validate_email(sv.email, sv.ho_ten, sv.mssv)
        if not ok:
            return False, msg

        # Kiểm tra trùng MSSV
        for s in self.ds_sinh_vien:
            if s.mssv.upper() == sv.mssv.upper():
                return False, f"MSSV '{sv.mssv}' đã tồn tại!"
        self.ds_sinh_vien.append(sv)
        self.sap_xep_mac_dinh()
        self.luu()
        return True, f"Đã thêm sinh viên {sv.ho_ten} thành công!"

    def sua(self, mssv, sv_moi):
        """
        Sửa thông tin sinh viên theo MSSV.
        
        Returns:
            tuple: (bool, str)
        """
        ok, msg = validate_ho_ten(sv_moi.ho_ten)
        if not ok:
            return False, msg
        ok, msg = validate_ngay_sinh(sv_moi.ngay_sinh)
        if not ok:
            return False, msg
        ok, msg = validate_email(sv_moi.email, sv_moi.ho_ten, sv_moi.mssv)
        if not ok:
            return False, msg

        for i, sv in enumerate(self.ds_sinh_vien):
            if sv.mssv.upper() == mssv.upper():
                self.ds_sinh_vien[i] = sv_moi
                self.sap_xep_mac_dinh()
                self.luu()
                return True, f"Đã cập nhật sinh viên {mssv} thành công!"
        return False, f"Không tìm thấy sinh viên có MSSV '{mssv}'!"

    def xoa(self, mssv):
        """
        Xóa sinh viên theo MSSV.
        
        Returns:
            tuple: (bool, str)
        """
        for i, sv in enumerate(self.ds_sinh_vien):
            if sv.mssv.upper() == mssv.upper():
                ten = sv.ho_ten
                self.ds_sinh_vien.pop(i)
                self.luu()
                return True, f"Đã xóa sinh viên {ten} ({mssv})!"
        return False, f"Không tìm thấy sinh viên có MSSV '{mssv}'!"

    def tim_kiem(self, keyword, tieu_chi="mssv"):
        """
        Tìm kiếm sinh viên theo tiêu chí.
        
        Args:
            keyword: Từ khóa tìm kiếm
            tieu_chi: "mssv", "ho_ten", "lop"
            
        Returns:
            list: Danh sách sinh viên tìm được
        """
        keyword = keyword.strip().lower()
        if not keyword:
            return self.ds_sinh_vien[:]

        normalized_keyword = normalize_text(keyword)
        ket_qua = []
        for sv in self.ds_sinh_vien:
            if tieu_chi == "mssv" and keyword in sv.mssv.lower():
                ket_qua.append(sv)
            elif tieu_chi == "ho_ten":
                ho_ten_normalized = normalize_text(sv.ho_ten)
                if keyword in sv.ho_ten.lower() or normalized_keyword in ho_ten_normalized:
                    ket_qua.append(sv)
            elif tieu_chi == "lop" and keyword in sv.lop.lower():
                ket_qua.append(sv)
        return ket_qua

    def sap_xep(self, tieu_chi="ho_ten", tang_dan=True):
        """
        Sắp xếp danh sách sinh viên.
        
        Args:
            tieu_chi: "ho_ten", "mssv", "lop"
            tang_dan: True = tăng dần, False = giảm dần
        """
        if tieu_chi == "ho_ten":
            self.ds_sinh_vien.sort(
                key=lambda sv: vietnamese_sort_key(sv.ho_ten),
                reverse=not tang_dan
            )
        elif tieu_chi == "mssv":
            self.ds_sinh_vien.sort(
                key=lambda sv: sv.mssv,
                reverse=not tang_dan
            )
        elif tieu_chi == "lop":
            self.ds_sinh_vien.sort(
                key=lambda sv: sv.lop,
                reverse=not tang_dan
            )

    def tim_theo_mssv(self, mssv):
        """Tìm sinh viên theo MSSV chính xác."""
        for sv in self.ds_sinh_vien:
            if sv.mssv.upper() == mssv.upper():
                return sv
        return None

    def luu(self):
        """Lưu danh sách sinh viên vào file."""
        save_data(self.ds_sinh_vien, FILE_SINH_VIEN)

    def so_luong(self):
        """Trả về số lượng sinh viên."""
        return len(self.ds_sinh_vien)


class MonHocManager:
    """Quản lý danh sách môn học."""

    def __init__(self, ds_mon_hoc=None):
        self.ds_mon_hoc = ds_mon_hoc if ds_mon_hoc is not None else []

    def them(self, mh):
        """Thêm môn học mới."""
        # Validate mã môn
        ok, msg = validate_ma_mon(mh.ma_mon)
        if not ok:
            return False, msg
        
        for m in self.ds_mon_hoc:
            if m.ma_mon.upper() == mh.ma_mon.upper():
                return False, f"Mã môn '{mh.ma_mon}' đã tồn tại!"
        self.ds_mon_hoc.append(mh)
        self.luu()
        return True, f"Đã thêm môn {mh.ten_mon} thành công!"

    def sua(self, ma_mon, mh_moi):
        """Sửa thông tin môn học."""
        # Validate mã môn mới
        ok, msg = validate_ma_mon(mh_moi.ma_mon)
        if not ok:
            return False, msg
        
        for i, mh in enumerate(self.ds_mon_hoc):
            if mh.ma_mon.upper() == ma_mon.upper():
                self.ds_mon_hoc[i] = mh_moi
                self.luu()
                return True, f"Đã cập nhật môn {ma_mon} thành công!"
        return False, f"Không tìm thấy môn có mã '{ma_mon}'!"

    def xoa(self, ma_mon):
        """Xóa môn học."""
        for i, mh in enumerate(self.ds_mon_hoc):
            if mh.ma_mon.upper() == ma_mon.upper():
                ten = mh.ten_mon
                self.ds_mon_hoc.pop(i)
                self.luu()
                return True, f"Đã xóa môn {ten} ({ma_mon})!"
        return False, f"Không tìm thấy môn có mã '{ma_mon}'!"

    def tim_theo_ma(self, ma_mon):
        """Tìm môn học theo mã."""
        for mh in self.ds_mon_hoc:
            if mh.ma_mon.upper() == ma_mon.upper():
                return mh
        return None

    def tim_kiem(self, keyword):
        """Tìm kiếm môn học theo mã hoặc tên."""
        keyword = keyword.strip().lower()
        if not keyword:
            return self.ds_mon_hoc[:]
        return [mh for mh in self.ds_mon_hoc
                if keyword in mh.ma_mon.lower() or keyword in mh.ten_mon.lower()]

    def luu(self):
        save_data(self.ds_mon_hoc, FILE_MON_HOC)

    def so_luong(self):
        return len(self.ds_mon_hoc)


class LopHocPhanManager:
    """Quản lý danh sách lớp học phần."""

    def __init__(self, ds_lop_hp=None):
        self.ds_lop_hp = ds_lop_hp if ds_lop_hp is not None else []

    def them(self, lhp):
        """Thêm lớp học phần mới."""
        for l in self.ds_lop_hp:
            if l.ma_lhp.upper() == lhp.ma_lhp.upper():
                return False, f"Mã lớp HP '{lhp.ma_lhp}' đã tồn tại!"
        self.ds_lop_hp.append(lhp)
        self.luu()
        return True, f"Đã tạo lớp HP {lhp.ma_lhp} thành công!"

    def sua(self, ma_lhp, lhp_moi):
        """Sửa thông tin lớp HP."""
        if lhp_moi.ma_lhp.upper() != ma_lhp.upper():
            for l in self.ds_lop_hp:
                if l.ma_lhp.upper() == lhp_moi.ma_lhp.upper():
                    return False, f"Mã lớp HP '{lhp_moi.ma_lhp}' đã tồn tại!"
        for i, lhp in enumerate(self.ds_lop_hp):
            if lhp.ma_lhp.upper() == ma_lhp.upper():
                self.ds_lop_hp[i] = lhp_moi
                self.luu()
                return True, f"Đã cập nhật lớp HP thành công!"
        return False, f"Không tìm thấy lớp HP '{ma_lhp}'!"

    def xoa(self, ma_lhp):
        """Xóa lớp HP."""
        for i, lhp in enumerate(self.ds_lop_hp):
            if lhp.ma_lhp.upper() == ma_lhp.upper():
                self.ds_lop_hp.pop(i)
                self.luu()
                return True, f"Đã xóa lớp HP {ma_lhp}!"
        return False, f"Không tìm thấy lớp HP '{ma_lhp}'!"

    def tim_theo_ma(self, ma_lhp):
        """Tìm lớp HP theo mã."""
        for lhp in self.ds_lop_hp:
            if lhp.ma_lhp.upper() == ma_lhp.upper():
                return lhp
        return None

    def them_sv_vao_lop(self, ma_lhp, mssv):
        """Thêm sinh viên vào lớp HP."""
        lhp = self.tim_theo_ma(ma_lhp)
        if lhp is None:
            return False, f"Không tìm thấy lớp HP '{ma_lhp}'!"
        if lhp.them_sinh_vien(mssv):
            self.luu()
            return True, f"Đã thêm SV {mssv} vào lớp {ma_lhp}!"
        return False, f"SV {mssv} đã có trong lớp {ma_lhp}!"

    def xoa_sv_khoi_lop(self, ma_lhp, mssv):
        """Xóa sinh viên khỏi lớp HP."""
        lhp = self.tim_theo_ma(ma_lhp)
        if lhp is None:
            return False, f"Không tìm thấy lớp HP '{ma_lhp}'!"
        if lhp.xoa_sinh_vien(mssv):
            self.luu()
            return True, f"Đã xóa SV {mssv} khỏi lớp {ma_lhp}!"
        return False, f"SV {mssv} không có trong lớp {ma_lhp}!"

    def tim_kiem(self, keyword):
        """Tìm kiếm lớp HP."""
        keyword = keyword.strip().lower()
        if not keyword:
            return self.ds_lop_hp[:]
        return [lhp for lhp in self.ds_lop_hp
                if keyword in lhp.ma_lhp.lower() or keyword in lhp.ma_mon.lower()]

    def luu(self):
        save_data(self.ds_lop_hp, FILE_LOP_HOC_PHAN)

    def so_luong(self):
        return len(self.ds_lop_hp)


class DiemManager:
    """Quản lý điểm số: nhập, cập nhật, tính GPA, xếp loại."""

    def __init__(self, ds_diem=None):
        self.ds_diem = ds_diem if ds_diem is not None else []

    def nhap_diem(self, bang_diem):
        """
        Nhập điểm cho sinh viên.
        Nếu đã có điểm môn đó thì cập nhật.
        """
        # Kiểm tra xem đã có điểm chưa
        for i, bd in enumerate(self.ds_diem):
            if (bd.mssv.upper() == bang_diem.mssv.upper() and
                    bd.ma_mon.upper() == bang_diem.ma_mon.upper()):
                self.ds_diem[i] = bang_diem
                self.luu()
                return True, f"Đã cập nhật điểm môn {bang_diem.ma_mon} cho SV {bang_diem.mssv}!"

        self.ds_diem.append(bang_diem)
        self.luu()
        return True, f"Đã nhập điểm môn {bang_diem.ma_mon} cho SV {bang_diem.mssv}!"

    def xoa_diem(self, mssv, ma_mon):
        """Xóa điểm."""
        for i, bd in enumerate(self.ds_diem):
            if bd.mssv.upper() == mssv.upper() and bd.ma_mon.upper() == ma_mon.upper():
                self.ds_diem.pop(i)
                self.luu()
                return True, f"Đã xóa điểm môn {ma_mon} của SV {mssv}!"
        return False, f"Không tìm thấy điểm!"

    def xoa_toan_bo_diem_mon(self, ma_mon):
        """Xóa tất cả điểm của một môn học."""
        diem_xoa = [bd for bd in self.ds_diem if bd.ma_mon.upper() == ma_mon.upper()]
        if not diem_xoa:
            return 0
        
        self.ds_diem = [bd for bd in self.ds_diem if bd.ma_mon.upper() != ma_mon.upper()]
        self.luu()
        return len(diem_xoa)

    def lay_diem_sv(self, mssv):
        """Lấy tất cả điểm của sinh viên."""
        return [bd for bd in self.ds_diem if bd.mssv.upper() == mssv.upper()]

    def lay_diem_mon(self, ma_mon):
        """Lấy tất cả điểm của một môn."""
        return [bd for bd in self.ds_diem if bd.ma_mon.upper() == ma_mon.upper()]

    def lay_diem(self, mssv, ma_mon):
        """Lấy điểm cụ thể của 1 SV 1 môn."""
        for bd in self.ds_diem:
            if bd.mssv.upper() == mssv.upper() and bd.ma_mon.upper() == ma_mon.upper():
                return bd
        return None

    def tinh_gpa_he4(self, mssv, ds_mon_hoc):
        """
        Tính GPA trung bình tích lũy hệ 4 (có trọng số tín chỉ).
        
        Args:
            mssv: Mã số sinh viên
            ds_mon_hoc: Danh sách môn học (để lấy số tín chỉ)
            
        Returns:
            float: GPA hệ 4 trung bình, -1 nếu chưa có điểm
        """
        ds_bd = self.lay_diem_sv(mssv)
        if not ds_bd:
            return -1

        tong_diem_he4 = 0
        tong_tin_chi = 0

        for bd in ds_bd:
            # Tìm số tín chỉ của môn
            so_tc = 1  # Mặc định 1 nếu không tìm thấy
            for mh in ds_mon_hoc:
                if mh.ma_mon.upper() == bd.ma_mon.upper():
                    so_tc = mh.so_tin_chi
                    break
            tong_diem_he4 += bd.diem_he4 * so_tc
            tong_tin_chi += so_tc

        if tong_tin_chi == 0:
            return -1
        return round(tong_diem_he4 / tong_tin_chi, 2)

    def tinh_gpa_he10(self, mssv, ds_mon_hoc):
        """
        Tính GPA trung bình tích lũy hệ 10 (có trọng số tín chỉ).
        """
        ds_bd = self.lay_diem_sv(mssv)
        if not ds_bd:
            return -1

        tong_diem = 0
        tong_tin_chi = 0

        for bd in ds_bd:
            so_tc = 1
            for mh in ds_mon_hoc:
                if mh.ma_mon.upper() == bd.ma_mon.upper():
                    so_tc = mh.so_tin_chi
                    break
            tong_diem += bd.diem_tong_ket * so_tc
            tong_tin_chi += so_tc

        if tong_tin_chi == 0:
            return -1
        return round(tong_diem / tong_tin_chi, 2)

    def xep_loai_sv(self, mssv, ds_mon_hoc):
        """
        Xếp loại học lực của sinh viên dựa trên GPA tích lũy hệ 10.
        
        Returns:
            str: Xếp loại học lực
        """
        gpa = self.tinh_gpa_he10(mssv, ds_mon_hoc)
        if gpa < 0:
            return "Chưa có điểm"
        if gpa >= 9.0:
            return "Xuất sắc"
        elif gpa >= 8.0:
            return "Giỏi"
        elif gpa >= 7.0:
            return "Khá"
        elif gpa >= 6.5:
            return "TB Khá"
        elif gpa >= 5.5:
            return "Trung bình"
        elif gpa >= 4.0:
            return "Yếu"
        else:
            return "Kém"

    def tim_kiem(self, keyword):
        """Tìm kiếm điểm theo MSSV hoặc mã môn."""
        keyword = keyword.strip().lower()
        if not keyword:
            return self.ds_diem[:]
        return [bd for bd in self.ds_diem
                if keyword in bd.mssv.lower() or keyword in bd.ma_mon.lower()]

    def thong_ke_xep_loai(self, ds_sinh_vien, ds_mon_hoc):
        """
        Thống kê số lượng sinh viên theo xếp loại.
        
        Returns:
            dict: {xếp_loại: số_lượng}
        """
        thong_ke = {
            "Xuất sắc": 0, "Giỏi": 0, "Khá": 0,
            "TB Khá": 0, "Trung bình": 0, "Yếu": 0,
            "Kém": 0, "Chưa có điểm": 0
        }
        for sv in ds_sinh_vien:
            xl = self.xep_loai_sv(sv.mssv, ds_mon_hoc)
            if xl in thong_ke:
                thong_ke[xl] += 1
        return thong_ke

    def top_sinh_vien(self, ds_sinh_vien, ds_mon_hoc, n=10):
        """
        Lấy top N sinh viên có GPA cao nhất.
        
        Returns:
            list: [(SinhVien, gpa_he4, gpa_he10, xep_loai)]
        """
        ket_qua = []
        for sv in ds_sinh_vien:
            gpa4 = self.tinh_gpa_he4(sv.mssv, ds_mon_hoc)
            gpa10 = self.tinh_gpa_he10(sv.mssv, ds_mon_hoc)
            xl = self.xep_loai_sv(sv.mssv, ds_mon_hoc)
            if gpa4 >= 0:
                ket_qua.append((sv, gpa4, gpa10, xl))

        ket_qua.sort(key=lambda x: x[1], reverse=True)
        return ket_qua[:n]

    def luu(self):
        save_data(self.ds_diem, FILE_DIEM)

    def so_luong(self):
        return len(self.ds_diem)
