FROM python:3.10.11

WORKDIR /app

# Copy các file yêu cầu
COPY requirements.txt requirements.txt
COPY . .

# Cài đặt các phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Cấu hình thư mục static/uploads
RUN mkdir -p /app/static/uploads

# Expose port 5000
EXPOSE 5000

CMD ["python", "main.py"]
