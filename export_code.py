import os
from pathlib import Path

# Thư mục gốc là nơi đặt file script này
ROOT_DIR = Path(__file__).parent
OUTPUT_FILE = ROOT_DIR / "project_code_for_ai.txt"

# Các thư mục sẽ bỏ qua
EXCLUDE_DIRS = {
    ".git", "__pycache__", "venv", ".venv", "env",
    "node_modules", "docs", "tests", ".pytest_cache"
}

# Các file cụ thể sẽ bỏ qua (bảo mật hoặc quá nặng toàn dữ liệu mẫu)
EXCLUDE_FILES = {
    ".env",
    "export_code.py",
    "project_code_for_ai.txt",
    "venues-data.js",
    "seed_restaurants.py",
    "seed_restaurants.sql",
    "init_db.sql",
    "activate.bat",
    "zip_project.py",
}

# Chỉ lấy các file code/cấu hình đọc được
INCLUDE_EXTS = {
    ".py", ".js", ".html", ".css", ".sql",
    ".txt", ".md", ".yml", ".yaml", ".example"
}
INCLUDE_EXACT_NAMES = {"Dockerfile"}

def export_project():
    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
            # Lọc bỏ thư mục không cần thiết
            dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
            
            for filename in sorted(filenames):
                if filename in EXCLUDE_FILES:
                    continue
                
                filepath = Path(dirpath) / filename
                if filepath.suffix.lower() not in INCLUDE_EXTS and filename not in INCLUDE_EXACT_NAMES:
                    continue
                
                rel_path = filepath.relative_to(ROOT_DIR)
                try:
                    content = filepath.read_text(encoding="utf-8", errors="ignore")
                    out.write(f"\n{'='*80}\n")
                    out.write(f"FILE: {rel_path}\n")
                    out.write(f"{'='*80}\n")
                    out.write(content)
                    out.write("\n")
                    count += 1
                except Exception as e:
                    print(f"Bo qua {rel_path}: {e}")

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"Xong! Da gom {count} file vao '{OUTPUT_FILE.name}' ({size_kb:.1f} KB).")

if __name__ == "__main__":
    export_project()