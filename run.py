import uvicorn

if __name__ == "__main__":
    # Chạy ứng dụng FastAPI thông qua Uvicorn server
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
