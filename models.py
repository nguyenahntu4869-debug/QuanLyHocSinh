from datetime import datetime


class SinhVien:
    

    def __init__(self, mssv="", ho_ten="", ngay_sinh="", gioi_tinh="Nam", lop="", email=""):
        self._mssv = mssv
        self._ho_ten = ho_ten
        self._ngay_sinh = ngay_sinh  # Định dạng: dd/mm/yyyy
        self._gioi_tinh = gioi_tinh  # "Nam" hoặc "Nữ"
        self._lop = lop
        self._email = email

    # --- Getter ---
    @property
    def mssv(self):
        return self._mssv

    @property
    def ho_ten(self):
        return self._ho_ten

    @property
    def ngay_sinh(self):
        return self._ngay_sinh

    @property
    def gioi_tinh(self):
        return self._gioi_tinh

    @property
    def lop(self):
        return self._lop

    @property
    def email(self):
        return self._email

    # --- Setter ---
    @mssv.setter
    def mssv(self, value):
        self._mssv = value

    @ho_ten.setter
    def ho_ten(self, value):
        self._ho_ten = value

    @ngay_sinh.setter
    def ngay_sinh(self, value):
        self._ngay_sinh = value

    @gioi_tinh.setter
    def gioi_tinh(self, value):
        self._gioi_tinh = value

    @lop.setter
    def lop(self, value):
        self._lop = value

    @email.setter
    def email(self, value):
        self._email = value

    def __str__(self):
        return f"SV[{self._mssv}] {self._ho_ten} - Lớp: {self._lop}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        
        return {
            "MSSV": self._mssv,
            "Họ tên": self._ho_ten,
            "Ngày sinh": self._ngay_sinh,
            "Giới tính": self._gioi_tinh,
            "Lớp": self._lop,
            "Email": self._email
        }


class MonHoc:

    def __init__(self, ma_mon="", ten_mon="", so_tin_chi=0):
        self._ma_mon = ma_mon
        self._ten_mon = ten_mon
        self._so_tin_chi = so_tin_chi

    # --- Getter ---
    @property
    def ma_mon(self):
        return self._ma_mon

    @property
    def ten_mon(self):
        return self._ten_mon

    @property
    def so_tin_chi(self):
        return self._so_tin_chi

    # --- Setter ---
    @ma_mon.setter
    def ma_mon(self, value):
        self._ma_mon = value

    @ten_mon.setter
    def ten_mon(self, value):
        self._ten_mon = value

    @so_tin_chi.setter
    def so_tin_chi(self, value):
        self._so_tin_chi = value

    def __str__(self):
        return f"MH[{self._ma_mon}] {self._ten_mon} ({self._so_tin_chi} tín chỉ)"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "Mã môn": self._ma_mon,
            "Tên môn": self._ten_mon,
            "Số tín chỉ": self._so_tin_chi
        }


class LopHocPhan:

    def __init__(self, ma_lhp="", ma_mon="", hoc_ky="", nam_hoc="", ds_mssv=None):
        self._ma_lhp = ma_lhp
        self._ma_mon = ma_mon
        self._hoc_ky = hoc_ky        # VD: "HK1", "HK2"
        self._nam_hoc = nam_hoc      # VD: "2024-2025"
        self._ds_mssv = ds_mssv if ds_mssv is not None else []

    # --- Getter ---
    @property
    def ma_lhp(self):
        return self._ma_lhp

    @property
    def ma_mon(self):
        return self._ma_mon

    @property
    def hoc_ky(self):
        return self._hoc_ky

    @property
    def nam_hoc(self):
        return self._nam_hoc

    @property
    def ds_mssv(self):
        return self._ds_mssv

    # --- Setter ---
    @ma_lhp.setter
    def ma_lhp(self, value):
        self._ma_lhp = value

    @ma_mon.setter
    def ma_mon(self, value):
        self._ma_mon = value

    @hoc_ky.setter
    def hoc_ky(self, value):
        self._hoc_ky = value

    @nam_hoc.setter
    def nam_hoc(self, value):
        self._nam_hoc = value

    @ds_mssv.setter
    def ds_mssv(self, value):
        self._ds_mssv = value

    def them_sinh_vien(self, mssv):
        """Thêm MSSV vào danh sách lớp."""
        if mssv not in self._ds_mssv:
            self._ds_mssv.append(mssv)
            return True
        return False

    def xoa_sinh_vien(self, mssv):
    
        if mssv in self._ds_mssv:
            self._ds_mssv.remove(mssv)
            return True
        return False

    def so_luong_sv(self):
       
        return len(self._ds_mssv)

    def __str__(self):
        return f"LHP[{self._ma_lhp}] Môn: {self._ma_mon} - {self._hoc_ky}/{self._nam_hoc} ({self.so_luong_sv()} SV)"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "Mã LHP": self._ma_lhp,
            "Mã môn": self._ma_mon,
            "Học kỳ": self._hoc_ky,
            "Năm học": self._nam_hoc,
            "Số SV": self.so_luong_sv()
        }


class BangDiem:

    def __init__(self, mssv="", ma_mon="", diem_qua_trinh=0.0, diem_thi=0.0):
        self._mssv = mssv
        self._ma_mon = ma_mon
        self._diem_qua_trinh = diem_qua_trinh  # Điểm quá trình (50%)
        self._diem_thi = diem_thi                # Điểm thi (50%)

    # --- Getter ---
    @property
    def mssv(self):
        return self._mssv

    @property
    def ma_mon(self):
        return self._ma_mon

    @property
    def diem_qua_trinh(self):
        return self._diem_qua_trinh

    @property
    def diem_thi(self):
        return self._diem_thi

    @property
    def diem_tong_ket(self):
        return round(self._diem_qua_trinh * 0.5 + self._diem_thi * 0.5, 2)

    @property
    def diem_he4(self):
        
        dtk = self.diem_tong_ket
        if dtk >= 9.0:
            return 4.0
        elif dtk >= 8.5:
            return 3.7
        elif dtk >= 8.0:
            return 3.5
        elif dtk >= 7.0:
            return 3.0
        elif dtk >= 6.5:
            return 2.5
        elif dtk >= 5.5:
            return 2.0
        elif dtk >= 5.0:
            return 1.5
        elif dtk >= 4.0:
            return 1.0
        else:
            return 0.0

    @property
    def diem_chu(self):
        
        dtk = self.diem_tong_ket
        if dtk >= 9.0:
            return "A+"
        elif dtk >= 8.5:
            return "A"
        elif dtk >= 8.0:
            return "B+"
        elif dtk >= 7.0:
            return "B"
        elif dtk >= 6.5:
            return "C+"
        elif dtk >= 5.5:
            return "C"
        elif dtk >= 5.0:
            return "D+"
        elif dtk >= 4.0:
            return "D"
        else:
            return "F"

    @property
    def xep_loai(self):
        
        dtk = self.diem_tong_ket
        if dtk >= 9.0:
            return "Xuất sắc"
        elif dtk >= 8.0:
            return "Giỏi"
        elif dtk >= 7.0:
            return "Khá"
        elif dtk >= 6.5:
            return "TB Khá"
        elif dtk >= 5.5:
            return "Trung bình"
        elif dtk >= 4.0:
            return "Yếu"
        else:
            return "Kém"

    # --- Setter ---
    @mssv.setter
    def mssv(self, value):
        self._mssv = value

    @ma_mon.setter
    def ma_mon(self, value):
        self._ma_mon = value

    @diem_qua_trinh.setter
    def diem_qua_trinh(self, value):
        self._diem_qua_trinh = value

    @diem_thi.setter
    def diem_thi(self, value):
        self._diem_thi = value

    def __str__(self):
        return (f"Điểm[{self._mssv}-{self._ma_mon}] "
                f"QT: {self._diem_qua_trinh} | Thi: {self._diem_thi} | "
                f"TK: {self.diem_tong_ket} ({self.diem_chu})")

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "MSSV": self._mssv,
            "Mã môn": self._ma_mon,
            "Điểm QT": self._diem_qua_trinh,
            "Điểm thi": self._diem_thi,
            "Tổng kết": self.diem_tong_ket,
            "Hệ 4": self.diem_he4,
            "Điểm chữ": self.diem_chu,
            "Xếp loại": self.xep_loai
        }
