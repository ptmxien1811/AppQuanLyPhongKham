import os

# Tên file kết quả sẽ được tạo ra
OUTPUT_FILE = 'project_full_code.txt'

# Các thư mục cần BỎ QUA (không quét để tránh file rác/thư viện)
IGNORE_DIRS = {'.git', '.idea', '__pycache__', 'venv', '.venv', 'images', 'node_modules', 'dist', 'build'}

# Các đuôi file cần LẤY nội dung (bạn có thể thêm/bớt tùy ý)
INCLUDE_EXTENSIONS = {'.py', '.html', '.css', '.js', '.json', '.sql', '.txt', '.md', '.xml'}


def is_ignored(path):
    """Kiểm tra xem đường dẫn có nằm trong danh sách bỏ qua không"""
    parts = path.split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return True
    return False


def main():
    project_root = os.getcwd()  # Lấy thư mục hiện tại đang chạy script

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
            print(f"Đang quét thư mục: {project_root} ...\n")

            # Duyệt qua tất cả thư mục và file
            for root, dirs, files in os.walk(project_root):

                # Loại bỏ các thư mục không mong muốn để không đi sâu vào
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

                for file in files:
                    file_path = os.path.join(root, file)

                    # Bỏ qua chính file script này và file kết quả để tránh lặp vô tận
                    if file in ['export_code.py', OUTPUT_FILE]:
                        continue

                    # Chỉ lấy các file có đuôi code nằm trong danh sách cho phép
                    _, ext = os.path.splitext(file)
                    if ext.lower() in INCLUDE_EXTENSIONS:

                        # Tính đường dẫn tương đối để dễ đọc (ví dụ: saleapp/index.py)
                        rel_path = os.path.relpath(file_path, project_root)

                        if not is_ignored(rel_path):
                            try:
                                # Đọc nội dung file
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()

                                # Ghi vào file tổng hợp với định dạng rõ ràng
                                outfile.write(f"\n{'=' * 60}\n")
                                outfile.write(f"FILE: {rel_path}\n")
                                outfile.write(f"{'=' * 60}\n")
                                outfile.write(content + "\n")

                                print(f"✅ Đã thêm: {rel_path}")
                            except Exception as e:
                                print(f"❌ Lỗi khi đọc file {rel_path}: {e}")

        print(f"\n🎉 Xong! Toàn bộ code đã được lưu vào file: {OUTPUT_FILE}")
        print("Bạn có thể mở file này hoặc gửi nó đi.")

    except Exception as e:
        print(f"Có lỗi xảy ra khi tạo file: {e}")


if __name__ == '__main__':
    main()