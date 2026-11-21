@echo off
chcp 65001 >nul
echo ============================================================
echo   SMART DINING - KHOI CHAY TU DONG BACKEND & FRONTEND
echo ============================================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [LOI] Khong tim thay Python. Vui long cai dat Python 3.10+ truoc!
    pause
    exit /b 1
)

if not exist ".env" (
    echo [1/5] Tao file .env tu .env.example...
    copy .env.example .env >nul
) else (
    echo [1/5] Da co file .env, giu nguyen cau hinh hien tai.
)

if not exist "venv" (
    echo [2/5] Tao moi truong ao Python venv...
    python -m venv venv
)

echo [3/5] Kich hoat venv va cai dat thu vien...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

if not exist "food_recommendation.db" (
    echo [4/5] Khoi tao du lieu mau nha hang lan dau...
    python database\seed_restaurants.py 2>nul
) else (
    echo [4/5] Da co CSDL cuc bo, bo qua buoc seed.
)

echo [5/5] Khoi dong may chu tai http://127.0.0.1:8000 ...
echo   - Giao dien Web:   http://127.0.0.1:8000/frontend/index.html
echo   - Trang Admin:     http://127.0.0.1:8000/frontend/admin-restaurants.html
echo   - Tai lieu API:    http://127.0.0.1:8000/docs
python run.py
pause