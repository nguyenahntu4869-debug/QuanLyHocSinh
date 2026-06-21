import pickle
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

FILE_SINH_VIEN = os.path.join(DATA_DIR, "SV.bin")
FILE_MON_HOC = os.path.join(DATA_DIR, "MH.bin")
FILE_LOP_HOC_PHAN = os.path.join(DATA_DIR, "LHP.bin")
FILE_DIEM = os.path.join(DATA_DIR, "Diem.bin")


def _ensure_data_dir():
    """Tạo thư mục data nếu chưa tồn tại."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_data(data, filepath):
    """
    Ghi dữ liệu vào file nhị phân bằng Pickle.
    
    Args:
        data: Dữ liệu cần lưu (list, dict, object...)
        filepath: Đường dẫn file .bin
        
    Returns:
        bool: True nếu lưu thành công, False nếu thất bại
    """
    try:
        _ensure_data_dir()
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        return True
    except (IOError, pickle.PicklingError) as e:
        print(f"[LỖI] Không thể ghi file {filepath}: {e}")
        return False


def load_data(filepath):
    """
    Đọc dữ liệu từ file nhị phân bằng Pickle.
    
    Args:
        filepath: Đường dẫn file .bin
        
    Returns:
        Dữ liệu đọc được, hoặc list rỗng nếu file chưa tồn tại
    """
    try:
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data
    except (IOError, pickle.UnpicklingError, EOFError) as e:
        print(f"[LỖI] Không thể đọc file {filepath}: {e}")
        return []


def save_all(ds_sinh_vien, ds_mon_hoc, ds_lop_hp, ds_diem):
    """
    Lưu tất cả dữ liệu vào các file tương ứng.
    
    Args:
        ds_sinh_vien: Danh sách sinh viên
        ds_mon_hoc: Danh sách môn học
        ds_lop_hp: Danh sách lớp học phần
        ds_diem: Danh sách bảng điểm
    """
    save_data(ds_sinh_vien, FILE_SINH_VIEN)
    save_data(ds_mon_hoc, FILE_MON_HOC)
    save_data(ds_lop_hp, FILE_LOP_HOC_PHAN)
    save_data(ds_diem, FILE_DIEM)


def load_all():
    """
    Đọc tất cả dữ liệu từ các file.
    
    Returns:
        tuple: (ds_sinh_vien, ds_mon_hoc, ds_lop_hp, ds_diem)
    """
    _ensure_data_dir()
    ds_sinh_vien = load_data(FILE_SINH_VIEN)
    ds_mon_hoc = load_data(FILE_MON_HOC)
    ds_lop_hp = load_data(FILE_LOP_HOC_PHAN)
    ds_diem = load_data(FILE_DIEM)
    return ds_sinh_vien, ds_mon_hoc, ds_lop_hp, ds_diem
