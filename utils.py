import re
import os
import platform
from datetime import datetime


def validate_mssv(mssv):
    """
    Kiểm tra MSSV hợp lệ.
    MSSV phải có ít nhất 3 ký tự, chỉ chứa chữ và số.
    
    Args:
        mssv: Mã số sinh viên cần kiểm tra
        
    Returns:
        tuple: (bool, str) - (hợp lệ, thông báo lỗi)
    """
    if not mssv or not mssv.strip():
        return False, "MSSV không được để trống"
    mssv = mssv.strip()
    if not re.match(r'^[0-9]+$', mssv):
        return False, "MSSV chỉ được chứa số"
    if len(mssv) < 8 or len(mssv) > 9:
        return False, "MSSV phải có 8 hoặc 9 ký tự"
    return True, ""


def validate_ho_ten(ho_ten):
    """
    Kiểm tra họ tên hợp lệ.
    
    Args:
        ho_ten: Họ tên cần kiểm tra
        
    Returns:
        tuple: (bool, str) - (hợp lệ, thông báo lỗi)
    """
    if not ho_ten or not ho_ten.strip():
        return False, "Họ tên không được để trống"
    if len(ho_ten.strip()) < 2:
        return False, "Họ tên phải có ít nhất 2 ký tự"
    if not re.match(r'^[a-zA-ZÀ-ỹ\s]+$', ho_ten.strip()):
        return False, "Họ tên chỉ được chứa chữ cái và khoảng trắng"
    return True, ""


def validate_ngay_sinh(ngay_sinh):
    """
    Kiểm tra ngày sinh hợp lệ (dd/mm/yyyy).
    
    Args:
        ngay_sinh: Chuỗi ngày sinh
        
    Returns:
        tuple: (bool, str) - (hợp lệ, thông báo lỗi)
    """
    if not ngay_sinh or not ngay_sinh.strip():
        return False, "Ngày sinh không được để trống"
    try:
        date_obj = datetime.strptime(ngay_sinh.strip(), "%d/%m/%Y")
        # Kiểm tra tuổi hợp lý (16-60)
        today = datetime.now()
        age = today.year - date_obj.year
        if age < 16:
            return False, "Sinh viên phải ít nhất 16 tuổi"
        if age > 60:
            return False, "Ngày sinh không hợp lý (quá 60 tuổi)"
        return True, ""
    except ValueError:
        return False, "Ngày sinh không hợp lệ"

def generate_hust_email(ho_ten, mssv):
    """
    Sinh email HUST theo quy tắc:
    - Tên (từ cuối cùng, bỏ dấu, viết hoa chữ đầu)
    - Dấu chấm "."
    - Chữ cái đầu viết hoa của Họ và Đệm (bỏ dấu)
    - MSSV bỏ đi tiền tố "20"
    - @sis.hust.edu.vn
    
    Ví dụ:
        "Nguyễn Văn An",  MSSV "20215678" → "An.NV215678@sis.hust.edu.vn"
        "Nguyễn Văn A B", MSSV "20215678" → "B.NVA215678@sis.hust.edu.vn"
    
    Args:
        ho_ten: Họ tên sinh viên
        mssv: Mã số sinh viên
        
    Returns:
        str: Email theo định dạng HUST, hoặc "" nếu dữ liệu không đủ
    """
    if not ho_ten or not mssv:
        return ""
    
    # Bản đồ bỏ dấu tiếng Việt
    char_map = {
        'à':'a', 'á':'a', 'ả':'a', 'ã':'a', 'ạ':'a',
        'ă':'a', 'ằ':'a', 'ắ':'a', 'ẳ':'a', 'ẵ':'a', 'ặ':'a',
        'â':'a', 'ầ':'a', 'ấ':'a', 'ẩ':'a', 'ẫ':'a', 'ậ':'a',
        'đ':'d',
        'è':'e', 'é':'e', 'ẻ':'e', 'ẽ':'e', 'ẹ':'e',
        'ê':'e', 'ề':'e', 'ế':'e', 'ể':'e', 'ễ':'e', 'ệ':'e',
        'ì':'i', 'í':'i', 'ỉ':'i', 'ĩ':'i', 'ị':'i',
        'ò':'o', 'ó':'o', 'ỏ':'o', 'õ':'o', 'ọ':'o',
        'ô':'o', 'ồ':'o', 'ố':'o', 'ổ':'o', 'ỗ':'o', 'ộ':'o',
        'ơ':'o', 'ờ':'o', 'ớ':'o', 'ở':'o', 'ỡ':'o', 'ợ':'o',
        'ù':'u', 'ú':'u', 'ủ':'u', 'ũ':'u', 'ụ':'u',
        'ư':'u', 'ừ':'u', 'ứ':'u', 'ử':'u', 'ữ':'u', 'ự':'u',
        'ỳ':'y', 'ý':'y', 'ỷ':'y', 'ỹ':'y', 'ỵ':'y'
    }
    
    def strip_accents(txt):
        """Bỏ dấu tiếng Việt."""
        return "".join(char_map.get(c, c) for c in txt.lower())
    
    parts = ho_ten.strip().split()
    if not parts:
        return ""
    
    # Tên = từ cuối cùng, bỏ dấu, viết hoa chữ đầu
    ten = strip_accents(parts[-1]).capitalize()
    
    # Chữ cái đầu của Họ Đệm (các từ trước tên), bỏ dấu, viết hoa
    ho_dem_initials = ""
    for part in parts[:-1]:
        if part:
            first_char = strip_accents(part[0]).upper()
            ho_dem_initials += first_char
    
    # Bỏ tiền tố "20" khỏi MSSV
    mssv_suffix = mssv.strip()
    if mssv_suffix.startswith("20"):
        mssv_suffix = mssv_suffix[2:]
    
    return f"{ten}.{ho_dem_initials}{mssv_suffix}@sis.hust.edu.vn"


def validate_email(email, ho_ten="", mssv=""):
    """
    Kiểm tra email hợp lệ.
    Nếu có ho_ten và mssv, kiểm tra email khớp định dạng HUST.
    
    Args:
        email: Địa chỉ email
        ho_ten: Họ tên sinh viên (tùy chọn, dùng để kiểm tra định dạng HUST)
        mssv: Mã số sinh viên (tùy chọn, dùng để kiểm tra định dạng HUST)
        
    Returns:
        tuple: (bool, str) - (hợp lệ, thông báo lỗi)
    """
    if not email or not email.strip():
        return False, "Email không được để trống"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email.strip()):
        return False, "Email không hợp lệ"
    
    # Nếu có đủ thông tin, kiểm tra email theo định dạng HUST
    if ho_ten and mssv:
        expected = generate_hust_email(ho_ten, mssv)
        if email.strip().lower() != expected.lower():
            return False, f"Email không đúng định dạng!\nEmail đúng phải là: {expected}"
    
    return True, ""


def normalize_text(text):
    """
    Chuẩn hóa văn bản tiếng Việt: bỏ dấu và chuyển về chữ thường.
    """
    if not text:
        return ""
    char_map = {
        'à':'a', 'á':'a', 'ả':'a', 'ã':'a', 'ạ':'a',
        'ă':'a', 'ằ':'a', 'ắ':'a', 'ẳ':'a', 'ẵ':'a', 'ặ':'a',
        'â':'a', 'ầ':'a', 'ấ':'a', 'ẩ':'a', 'ẫ':'a', 'ậ':'a',
        'đ':'d',
        'è':'e', 'é':'e', 'ẻ':'e', 'ẽ':'e', 'ẹ':'e',
        'ê':'e', 'ề':'e', 'ế':'e', 'ể':'e', 'ễ':'e', 'ệ':'e',
        'ì':'i', 'í':'i', 'ỉ':'i', 'ĩ':'i', 'ị':'i',
        'ò':'o', 'ó':'o', 'ỏ':'o', 'õ':'o', 'ọ':'o',
        'ô':'o', 'ồ':'o', 'ố':'o', 'ổ':'o', 'ỗ':'o', 'ộ':'o',
        'ơ':'o', 'ờ':'o', 'ớ':'o', 'ở':'o', 'ỡ':'o', 'ợ':'o',
        'ù':'u', 'ú':'u', 'ủ':'u', 'ũ':'u', 'ụ':'u',
        'ư':'u', 'ừ':'u', 'ứ':'u', 'ử':'u', 'ữ':'u', 'ự':'u',
        'ỳ':'y', 'ý':'y', 'ỷ':'y', 'ỹ':'y', 'ỵ':'y'
    }
    return "".join(char_map.get(c, c) for c in text.strip().lower())


def validate_diem(diem_str):
    """
    Kiểm tra điểm hợp lệ (0-10).
    
    Args:
        diem_str: Chuỗi điểm số
        
    Returns:
        tuple: (bool, float, str) - (hợp lệ, giá trị điểm, thông báo lỗi)
    """
    if not diem_str or not str(diem_str).strip():
        return False, 0.0, "Điểm không được để trống"
    try:
        diem = float(str(diem_str).strip())
        if diem < 0 or diem > 10:
            return False, 0.0, "Điểm phải trong khoảng 0 - 10"
        return True, round(diem, 2), ""
    except ValueError:
        return False, 0.0, "Điểm phải là số"


def validate_so_tin_chi(stc_str):
    """
    Kiểm tra số tín chỉ hợp lệ.
    Chỉ chấp nhận: 2, 3, 4, 6, 8.
    
    Args:
        stc_str: Chuỗi số tín chỉ
        
    Returns:
        tuple: (bool, int, str) - (hợp lệ, giá trị, thông báo lỗi)
    """
    if not stc_str or not str(stc_str).strip():
        return False, 0, "Số tín chỉ không được để trống"
    try:
        stc = int(str(stc_str).strip())
        if stc not in (2, 3, 4, 6, 8):
            return False, 0, "Số tín chỉ phải là 2, 3, 4, 6 hoặc 8"
        return True, stc, ""
    except ValueError:
        return False, 0, "Số tín chỉ phải là số nguyên"


def validate_ma_mon(ma_mon):
    """
    Kiểm tra mã môn hợp lệ.
    Mã môn phải có đúng 6 ký tự: 2 chữ cái VIẾT HOA + 4 chữ số.
    VD: IT1234, MI3010
    
    Args:
        ma_mon: Mã môn học
        
    Returns:
        tuple: (bool, str) - (hợp lệ, thông báo lỗi)
    """
    if not ma_mon or not ma_mon.strip():
        return False, "Mã môn không được để trống"
    ma_mon = ma_mon.strip()
    if not re.match(r'^[A-Z]{2}[0-9]{4}$', ma_mon):
        return False, "Mã môn phải có 6 ký tự: 2 chữ cái VIẾT HOA + 4 chữ số (VD: IT1234)"
    return True, ""


def validate_ma_lhp(ma_lhp):
    """
    Kiểm tra mã lớp học phần hợp lệ.
    Mã lớp học phần chỉ được phép nhập số, không chứa chữ cái hoặc ký tự đặc biệt.
    
    Args:
        ma_lhp: Mã lớp học phần
        
    Returns:
        tuple: (bool, str) - (hợp lệ, thông báo lỗi)
    """
    if not ma_lhp or not ma_lhp.strip():
        return False, "Mã lớp HP không được để trống"
    ma_lhp = ma_lhp.strip()
    if not re.match(r'^[0-9]+$', ma_lhp):
        return False, "Mã lớp HP chỉ được phép nhập số, không chứa chữ cái hoặc ký tự đặc biệt"
    return True, ""



def clear_screen():
    """Xóa màn hình console."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def format_diem(diem):
    """
    Định dạng hiển thị điểm (1 chữ số thập phân).
    
    Args:
        diem: Điểm số (float)
        
    Returns:
        str: Điểm đã format
    """
    return f"{diem:.1f}"


def get_xep_loai_color(xep_loai):
    """
    Trả về mã màu tương ứng với xếp loại để hiển thị trên GUI.
    
    Args:
        xep_loai: Chuỗi xếp loại
        
    Returns:
        str: Mã màu hex
    """
    colors = {
        "Xuất sắc": "#00e676",   # Xanh lá sáng
        "Giỏi": "#69f0ae",       # Xanh lá nhạt
        "Khá": "#40c4ff",        # Xanh dương nhạt
        "TB Khá": "#ffab40",     # Cam
        "Trung bình": "#ffd740", # Vàng
        "Yếu": "#ff6e40",       # Cam đỏ
        "Kém": "#ff5252",       # Đỏ
    }
    return colors.get(xep_loai, "#ffffff")


def vietnamese_sort_key(fullname):
    """
    Tạo khóa sắp xếp cho họ tên tiếng Việt.
    Sắp xếp ưu tiên theo Tên (từ cuối cùng), sau đó đến Họ lót (các từ trước).
    Chuyển tiếng Việt có dấu thành không dấu để so sánh chính xác theo bảng chữ cái A-Z.
    """
    if not fullname:
        return ""
    
    # Chuyển sang chữ thường
    name = fullname.strip().lower()
    
    # Bản đồ chuyển ký tự tiếng Việt có dấu sang không dấu
    char_map = {
        'à':'a', 'á':'a', 'ả':'a', 'ã':'a', 'ạ':'a',
        'ă':'a', 'ằ':'a', 'ắ':'a', 'ẳ':'a', 'ẵ':'a', 'ặ':'a',
        'â':'a', 'ầ':'a', 'ấ':'a', 'ẩ':'a', 'ẫ':'a', 'ậ':'a',
        'đ':'d',
        'è':'e', 'é':'e', 'ẻ':'e', 'ẽ':'e', 'ẹ':'e',
        'ê':'e', 'ề':'e', 'ế':'e', 'ể':'e', 'ễ':'e', 'ệ':'e',
        'ì':'i', 'í':'i', 'ỉ':'i', 'ĩ':'i', 'ị':'i',
        'ò':'o', 'ó':'o', 'ỏ':'o', 'õ':'o', 'ọ':'o',
        'ô':'o', 'ồ':'o', 'ố':'o', 'ổ':'o', 'ỗ':'o', 'ộ':'o',
        'ơ':'o', 'ờ':'o', 'ớ':'o', 'ở':'o', 'ỡ':'o', 'ợ':'o',
        'ù':'u', 'ú':'u', 'ủ':'u', 'ũ':'u', 'ụ':'u',
        'ư':'u', 'ừ':'u', 'ứ':'u', 'ử':'u', 'ữ':'u', 'ự':'u',
        'ỳ':'y', 'ý':'y', 'ỷ':'y', 'ỹ':'y', 'ỵ':'y'
    }
    
    def strip_accents(txt):
        return "".join(char_map.get(c, c) for c in txt)
    
    parts = name.split()
    if not parts:
        return ""
        
    # Lấy tên và họ lót
    ten = parts[-1]
    ho_lot = " ".join(parts[:-1]) if len(parts) > 1 else ""
    
    # Trả về tuple (Tên không dấu, Họ lót không dấu, Tên gốc, Họ lót gốc) để làm khóa sắp xếp
    return (strip_accents(ten), strip_accents(ho_lot), ten, ho_lot)

