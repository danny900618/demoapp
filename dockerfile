# 使用官方Python映像作為基礎
FROM python:3.9-slim-buster

# 設置工作目錄
WORKDIR /app

# 複製所有Python文件和依賴項到映像中
COPY . .

# 安裝所需的依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 暴露應用程序的端口
EXPOSE 5000

# 執行應用程序
CMD [ "python", "app.py" ]
