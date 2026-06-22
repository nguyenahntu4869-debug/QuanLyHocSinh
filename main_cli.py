import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import SinhVien, MonHoc, LopHocPhan, BangDiem
from file_handler import load_all, save_all
from managers import SinhVienManager, MonHocManager, LopHocPhanManager, DiemManager
from utils import clear_screen, vietnamese_sort_key, validate_ho_ten, validate_ngay_sinh, validate_ma_mon, validate_so_tin_chi, validate_ma_lhp


def show_menu():
    print("=" * 60)
    print("      HỆ THỐNG QUẢN LÝ SINH VIÊN VÀ ĐIỂM SỐ (CLI) - HUST")
    print("=" * 60)
    print(" 1. Quản lý danh sách Sinh viên (SV.bin)")
    print(" 2. Quản lý danh mục Học phần (MH.bin)")
    print(" 3. Quản lý Lớp học phần (LopHP.bin)")
    print(" 4. Quản lý Nhập/Cập nhật điểm số (Diem.bin)")
    print(" 5. In bảng điểm chi tiết của Sinh viên ra màn hình")
    print(" 6. Thống kê kết quả học tập")
    print(" 0. Lưu dữ liệu & Thoát chương trình")
    print("=" * 60)


def quan_ly_sinh_vien(manager):
    while True:
        clear_screen()
        print("--- QUẢN LÝ DANH SÁCH SINH VIÊN (SV.bin) ---")
        print(" 1. Xem danh sách sinh viên (Sắp xếp A-Z)")
        print(" 2. Thêm sinh viên mới")
        print(" 3. Sửa thông tin sinh viên")
        print(" 4. Xóa sinh viên")
        print(" 0. Quay lại menu chính")
        choice = input("Lựa chọn của bạn: ").strip()

        if choice == "1":
            manager.sap_xep_mac_dinh()
            print(f"\nDanh sách sinh viên ({manager.so_luong()} SV):")
            print(f"{'STT':<4} | {'MSSV':<10} | {'Họ tên':<20} | {'Ngày sinh':<11} | {'Lớp':<10} | {'Email'}")
            print("-" * 80)
            for idx, sv in enumerate(manager.ds_sinh_vien, 1):
                print(f"{idx:<4} | {sv.mssv:<10} | {sv.ho_ten:<20} | {sv.ngay_sinh:<11} | {sv.lop:<10} | {sv.email}")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "2":
            mssv = input("Nhập MSSV: ").strip()
            ho_ten = input("Nhập Họ tên: ").strip()
            ngay_sinh = input("Nhập Ngày sinh (dd/mm/yyyy): ").strip()
            gioi_tinh = input("Nhập Giới tính (Nam/Nữ): ").strip()
            lop = input("Nhập Lớp sinh hoạt: ").strip()
            email = input("Nhập Email: ").strip()
            
            if not mssv or not ho_ten or not lop:
                print("Lỗi: Các thông tin cốt lõi (MSSV, Họ tên, Lớp) không được trống!")
            else:
                ok, msg = validate_ho_ten(ho_ten)
                if not ok:
                    print(f"Lỗi: {msg}")
                else:
                    ok, msg = validate_ngay_sinh(ngay_sinh)
                    if not ok:
                        print(f"Lỗi: {msg}")
                    else:
                        sv = SinhVien(mssv, ho_ten, ngay_sinh, gioi_tinh, lop, email)
                        ok, msg = manager.them(sv)
                        print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "3":
            mssv = input("Nhập MSSV cần sửa: ").strip()
            sv = manager.tim_theo_mssv(mssv)
            if not sv:
                print("Không tìm thấy sinh viên!")
            else:
                print(f"Đang sửa thông tin SV: {sv.ho_ten}")
                ho_ten = input(f"Họ tên mới ({sv.ho_ten}): ").strip() or sv.ho_ten
                ngay_sinh = input(f"Ngày sinh mới ({sv.ngay_sinh}): ").strip() or sv.ngay_sinh
                gioi_tinh = input(f"Giới tính mới ({sv.gioi_tinh}): ").strip() or sv.gioi_tinh
                lop = input(f"Lớp mới ({sv.lop}): ").strip() or sv.lop
                email = input(f"Email mới ({sv.email}): ").strip() or sv.email

                ok, msg = validate_ho_ten(ho_ten)
                if not ok:
                    print(f"Lỗi: {msg}")
                else:
                    ok, msg = validate_ngay_sinh(ngay_sinh)
                    if not ok:
                        print(f"Lỗi: {msg}")
                    else:
                        sv_moi = SinhVien(mssv, ho_ten, ngay_sinh, gioi_tinh, lop, email)
                        ok, msg = manager.sua(mssv, sv_moi)
                        print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "4":
            mssv = input("Nhập MSSV cần xóa: ").strip()
            ok, msg = manager.xoa(mssv)
            print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "0":
            break


def quan_ly_mon_hoc(manager, diem_manager):
    while True:
        clear_screen()
        print("--- QUẢN LÝ DANH MỤC HỌC PHẦN (MH.bin) ---")
        print(" 1. Xem danh sách học phần")
        print(" 2. Thêm học phần mới")
        print(" 3. Sửa thông tin học phần")
        print(" 4. Xóa học phần")
        print(" 0. Quay lại menu chính")
        choice = input("Lựa chọn của bạn: ").strip()

        if choice == "1":
            print(f"\nDanh mục học phần ({manager.so_luong()} học phần):")
            print(f"{'STT':<4} | {'Mã học phần':<11} | {'Tên học phần':<30} | {'Số tín chỉ'}")
            print("-" * 60)
            for idx, mh in enumerate(manager.ds_mon_hoc, 1):
                print(f"{idx:<4} | {mh.ma_mon:<10} | {mh.ten_mon:<30} | {mh.so_tin_chi}")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "2":
            ma_mon = input("Nhập Mã học phần: ").strip()
            ten_mon = input("Nhập Tên học phần: ").strip()
            so_tc_str = input("Nhập Số tín chỉ: ").strip()
            
            ok, msg = validate_ma_mon(ma_mon)
            if not ok:
                print(f"Lỗi: {msg}")
            else:
                ok, so_tc, msg = validate_so_tin_chi(so_tc_str)
                if not ok:
                    print(f"Lỗi: {msg}")
                else:
                    if not ten_mon:
                        print("Lỗi: Tên học phần không được để trống!")
                    else:
                        mh = MonHoc(ma_mon, ten_mon, so_tc)
                        ok, msg = manager.them(mh)
                        print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "3":
            ma_mon = input("Nhập Mã học phần cần sửa: ").strip()
            mh = manager.tim_theo_ma(ma_mon)
            if not mh:
                print(f"Lỗi: Học phần với mã '{ma_mon}' không tồn tại trong hệ thống!")
            else:
                ten_mon = input(f"Tên học phần mới ({mh.ten_mon}): ").strip() or mh.ten_mon
                so_tc_str = input(f"Số tín chỉ mới ({mh.so_tin_chi}): ").strip()
                
                ok, so_tc, msg = validate_so_tin_chi(so_tc_str) if so_tc_str else (True, mh.so_tin_chi, "")
                if not ok:
                    print(f"Lỗi: {msg}")
                else:
                    if not ten_mon:
                        print("Lỗi: Tên học phần không được để trống!")
                    else:
                        mh_moi = MonHoc(ma_mon, ten_mon, so_tc)
                        ok, msg = manager.sua(ma_mon, mh_moi)
                        print(msg)

            input("\nNhấn Enter để tiếp tục...")
        elif choice == "4":
            ma_mon = input("Nhập Mã học phần cần xóa: ").strip()
            mh_xoa = manager.tim_theo_ma(ma_mon)
            if not mh_xoa:
                print(f"Lỗi: Học phần với mã '{ma_mon}' không tồn tại trong hệ thống!")
                input("\nNhấn Enter để tiếp tục...")
                continue
            diem_lien_quan = diem_manager.lay_diem_mon(ma_mon)
            if diem_lien_quan:
                print(f"\n⚠️ Cảnh báo: Môn học này có {len(diem_lien_quan)} bản ghi điểm của sinh viên!")
                xac_nhan = input("Bạn có chắc chắn muốn xóa môn học và toàn bộ điểm của sinh viên về môn này? (yes/no): ").strip().lower()
                if xac_nhan != "yes":
                    print("Hủy bỏ xóa.")
                else:
                    so_diem_xoa = diem_manager.xoa_toan_bo_diem_mon(ma_mon)
                    ok, msg = manager.xoa(ma_mon)
                    print(msg)
                    if ok:
                        print(f"✓ Đã xóa {so_diem_xoa} bản ghi điểm của sinh viên.")
            else:
                ok, msg = manager.xoa(ma_mon)
                print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "0":
            break


def quan_ly_diem(diem_manager, sv_manager, mh_manager):
    while True:
        clear_screen()
        print("--- QUẢN LÝ NHẬP ĐIỂM (Diem.bin) ---")
        print(" 1. Xem toàn bộ bảng điểm lưu trữ")
        print(" 2. Nhập/Cập nhật điểm cho sinh viên")
        print(" 3. Xóa điểm học phần của sinh viên")
        print(" 0. Quay lại menu chính")
        choice = input("Lựa chọn của bạn: ").strip()

        if choice == "1":
            print(f"\nDanh sách điểm số ({diem_manager.so_luong()} bản ghi):")
            print(f"{'STT':<4} | {'MSSV':<10} | {'Họ tên':<20} | {'Mã HP':<8} | {'QT':<4} | {'Thi':<4} | {'T.Kết':<5} | {'Xếp loại'}")
            print("-" * 80)
            for idx, bd in enumerate(diem_manager.ds_diem, 1):
                sv = sv_manager.tim_theo_mssv(bd.mssv)
                ten_sv = sv.ho_ten if sv else bd.mssv
                print(f"{idx:<4} | {bd.mssv:<10} | {ten_sv:<20} | {bd.ma_mon:<8} | {bd.diem_qua_trinh:<4.1f} | {bd.diem_thi:<4.1f} | {bd.diem_tong_ket:<5.1f} | {bd.xep_loai}")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "2":
            mssv = input("Nhập MSSV sinh viên: ").strip()
            ma_mon = input("Nhập Mã học phần: ").strip()
            
            sv = sv_manager.tim_theo_mssv(mssv)
            mh = mh_manager.tim_theo_ma(ma_mon)
            
            if not sv:
                print("Lỗi: Mã sinh viên không tồn tại trong hệ thống!")
            elif not mh:
                print("Lỗi: Mã học phần không tồn tại trong hệ thống!")
            else:
                try:
                    diem_qt = float(input("Nhập Điểm quá trình (0-10): ").strip())
                    diem_thi = float(input("Nhập Điểm thi cuối kỳ (0-10): ").strip())
                    
                    if 0 <= diem_qt <= 10 and 0 <= diem_thi <= 10:
                        bd = BangDiem(mssv, ma_mon, diem_qt, diem_thi)
                        ok, msg = diem_manager.nhap_diem(bd)
                        print(msg)
                    else:
                        print("Lỗi: Điểm phải nằm trong thang điểm từ 0 đến 10!")
                except ValueError:
                    print("Lỗi: Điểm nhập vào phải là số!")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "3":
            mssv = input("Nhập MSSV: ").strip()
            ma_mon = input("Nhập Mã môn: ").strip()
            ok, msg = diem_manager.xoa_diem(mssv, ma_mon)
            print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "0":
            break


def in_bang_diem_sv(diem_manager, sv_manager, mh_manager):
    clear_screen()
    print("--- IN BẢNG ĐIỂM CHI TIẾT RA MÀN HÌNH ---")
    mssv = input("Nhập mã số sinh viên cần tra cứu: ").strip()
    
    sv = sv_manager.tim_theo_mssv(mssv)
    if not sv:
        print("Không tìm thấy sinh viên có MSSV này!")
        input("\nNhấn Enter để quay lại...")
        return
        
    ds_bd = diem_manager.lay_diem_sv(mssv)
    if not ds_bd:
        print(f"Sinh viên {sv.ho_ten} ({sv.mssv}) chưa có bản ghi điểm nào.")
        input("\nNhấn Enter để quay lại...")
        return
        
    gpa4 = diem_manager.tinh_gpa_he4(mssv, mh_manager.ds_mon_hoc)
    gpa10 = diem_manager.tinh_gpa_he10(mssv, mh_manager.ds_mon_hoc)
    xl = diem_manager.xep_loai_sv(mssv, mh_manager.ds_mon_hoc)
    
    print("\n" + "="*70)
    print(f" BẢNG ĐIỂM CHI TIẾT - SINH VIÊN: {sv.ho_ten.upper()} ({sv.mssv})")
    print(f" Lớp: {sv.lop} | Email: {sv.email}")
    print("="*70)
    print(f"{'Mã HP':<8} | {'Tên học phần':<25} | {'TC':<3} | {'Đ.QT':<4} | {'Đ.Thi':<5} | {'TK10':<5} | {'Hệ 4':<4} | {'Chữ'}")
    print("-" * 70)
    for bd in ds_bd:
        mh = mh_manager.tim_theo_ma(bd.ma_mon)
        ten_mon = mh.ten_mon if mh else bd.ma_mon
        tin_chi = mh.so_tin_chi if mh else 0
        print(f"{bd.ma_mon:<8} | {ten_mon:<25} | {tin_chi:<3} | {bd.diem_qua_trinh:<4.1f} | {bd.diem_thi:<5.1f} | {bd.diem_tong_ket:<5.1f} | {bd.diem_he4:<4.1f} | {bd.diem_chu}")
    print("-" * 70)
    print(f" GPA Tích lũy (Hệ 10): {gpa10:.2f}  |  GPA Tích lũy (Hệ 4): {gpa4:.2f}")
    print(f" Xếp loại học lực: {xl}")
    print("="*70)
    input("\nNhấn Enter để quay lại...")


def quan_ly_lhp(lhp_manager, sv_manager, mh_manager):
    while True:
        clear_screen()
        print("--- QUẢN LÝ LỚP HỌC PHẦN (LopHP.bin) ---")
        print(" 1. Xem danh sách Lớp học phần")
        print(" 2. Xem chi tiết sinh viên trong Lớp học phần")
        print(" 3. Khởi tạo Lớp học phần mới")
        print(" 4. Thêm sinh viên vào Lớp học phần")
        print(" 5. Xóa sinh viên khỏi Lớp học phần")
        print(" 0. Quay lại menu chính")
        choice = input("Lựa chọn của bạn: ").strip()

        if choice == "1":
            print(f"\nDanh sách Lớp Học Phần ({lhp_manager.so_luong()} lớp):")
            print(f"{'STT':<4} | {'Mã LHP':<10} | {'Mã HP':<8} | {'Học kỳ':<6} | {'Năm học':<10} | {'Số SV'}")
            print("-" * 60)
            for idx, lhp in enumerate(lhp_manager.ds_lop_hp, 1):
                print(f"{idx:<4} | {lhp.ma_lhp:<10} | {lhp.ma_mon:<8} | {lhp.hoc_ky:<6} | {lhp.nam_hoc:<10} | {lhp.so_luong_sv()}")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "2":
            ma_lhp = input("Nhập Mã lớp HP để xem chi tiết: ").strip()
            lhp = lhp_manager.tim_theo_ma(ma_lhp)
            if not lhp:
                print("Lỗi: Lớp học phần không tồn tại!")
            else:
                print(f"\nDanh sách thành viên lớp {ma_lhp}:")
                print(f"{'STT':<4} | {'MSSV':<10} | {'Họ tên':<25} | {'Lớp SH'}")
                print("-" * 50)
                for idx, mssv in enumerate(lhp.ds_mssv, 1):
                    sv = sv_manager.tim_theo_mssv(mssv)
                    ten = sv.ho_ten if sv else "N/A"
                    lop_sh = sv.lop if sv else "N/A"
                    print(f"{idx:<4} | {mssv:<10} | {ten:<25} | {lop_sh}")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "3":
            ma_lhp = input("Nhập Mã lớp HP: ").strip()
            ma_mon = input("Nhập Mã học phần: ").strip()
            hoc_ky = input("Nhập Học kỳ (ví dụ: 2025.1, 2025.2, 2025.3): ").strip()
            nam_hoc = input("Nhập Năm học (VD: 2025-2026): ").strip()
            
            mh = mh_manager.tim_theo_ma(ma_mon)
            ok_lhp, msg_lhp = validate_ma_lhp(ma_lhp)
            if not mh:
                print("Lỗi: Mã học phần không tồn tại trong hệ thống!")
            elif not ok_lhp:
                print(f"Lỗi: {msg_lhp}")
            else:
                lhp = LopHocPhan(ma_lhp, ma_mon, hoc_ky, nam_hoc)
                ok, msg = lhp_manager.them(lhp)
                print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "4":
            ma_lhp = input("Nhập Mã lớp HP: ").strip()
            mssv = input("Nhập MSSV cần thêm: ").strip()
            
            sv = sv_manager.tim_theo_mssv(mssv)
            if not sv:
                print("Lỗi: Mã sinh viên không tồn tại!")
            else:
                ok, msg = lhp_manager.them_sv_vao_lop(ma_lhp, mssv)
                print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "5":
            ma_lhp = input("Nhập Mã lớp HP: ").strip()
            mssv = input("Nhập MSSV cần xóa: ").strip()
            ok, msg = lhp_manager.xoa_sv_khoi_lop(ma_lhp, mssv)
            print(msg)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "0":
            break


def main():
    ds_sv, ds_mh, ds_lhp, ds_diem = load_all()

    sv_manager = SinhVienManager(ds_sv)
    mh_manager = MonHocManager(ds_mh)
    lhp_manager = LopHocPhanManager(ds_lhp)
    diem_manager = DiemManager(ds_diem)

    while True:
        clear_screen()
        show_menu()
        choice = input("Nhập lựa chọn của bạn (0-6): ").strip()

        if choice == "1":
            quan_ly_sinh_vien(sv_manager)
        elif choice == "2":
            quan_ly_mon_hoc(mh_manager, diem_manager)
        elif choice == "3":
            quan_ly_lhp(lhp_manager, sv_manager, mh_manager)
        elif choice == "4":
            quan_ly_diem(diem_manager, sv_manager, mh_manager)
        elif choice == "5":
            in_bang_diem_sv(diem_manager, sv_manager, mh_manager)
        elif choice == "6":
            clear_screen()
            print("--- THỐNG KÊ KẾT QUẢ HỌC TẬP ---")
            tk = diem_manager.thong_ke_xep_loai(sv_manager.ds_sinh_vien, mh_manager.ds_mon_hoc)
            for key, val in tk.items():
                print(f" • Xếp loại {key:<15}: {val} sinh viên")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "0":
            print("\nĐang lưu dữ liệu vào các tệp nhị phân...")
            save_all(
                sv_manager.ds_sinh_vien,
                mh_manager.ds_mon_hoc,
                lhp_manager.ds_lop_hp,
                diem_manager.ds_diem
            )
            print("Lưu thành công! Kết thúc chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại!")
            input("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    main()
