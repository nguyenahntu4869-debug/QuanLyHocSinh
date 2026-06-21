import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_handler import load_all
from managers import SinhVienManager, MonHocManager, LopHocPhanManager, DiemManager
from gui.main_window import MainWindow


def main():
    """Hàm chính - khởi động chương trình."""
    print("=" * 50)
    print("  CHUONG TRINH QUAN LY SINH VIEN")
    print("  Dang khoi dong...")
    print("=" * 50)

    # Bước 1: Đọc dữ liệu từ file nhị phân
    print("[1/3] Dang tai du lieu tu file...")
    ds_sv, ds_mh, ds_lhp, ds_diem = load_all()
    print(f"  + Sinh vien: {len(ds_sv)}")
    print(f"  + Mon hoc: {len(ds_mh)}")
    print(f"  + Lop HP: {len(ds_lhp)}")
    print(f"  + Ban ghi diem: {len(ds_diem)}")

    # Bước 2: Khởi tạo các Manager
    print("[2/3] Dang khoi tao he thong...")
    sv_manager = SinhVienManager(ds_sv)
    mh_manager = MonHocManager(ds_mh)
    lhp_manager = LopHocPhanManager(ds_lhp)
    diem_manager = DiemManager(ds_diem)
    print("  + Da khoi tao cac module quan ly")

    # Bước 3: Khởi tạo GUI
    print("[3/3] Dang khoi tao giao dien...")
    app = MainWindow(sv_manager, mh_manager, lhp_manager, diem_manager)
    print("  + Giao dien da san sang!")
    print("=" * 50)

    # Chạy ứng dụng
    app.run()

    # Khi thoát
    print("\n  Cam on da su dung chuong trinh!")
    print("  Du lieu da duoc luu tu dong.")


if __name__ == "__main__":
    main()
