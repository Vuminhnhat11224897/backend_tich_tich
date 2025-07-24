# Tích Tích App - PostgreSQL Docker Setup

## Mô tả
Dự án này sử dụng Docker để thiết lập cơ sở dữ liệu PostgreSQL cho ứng dụng Tích Tích - quản lý ví tiền cho trẻ em.

## Cấu trúc Database
- **customers**: Thông tin khách hàng (user_id, phone)
- **children**: Thông tin con cái (child_id, parent_id, name)
- **wallets**: Ví tiền của con (total, savings, charity, spending, bought)

## Cài đặt và Chạy

### 1. Cấu hình Environment Variables
```bash
# Copy file .env.example thành .env
copy .env.example .env

# Chỉnh sửa file .env với thông tin database của bạn
# Tất cả thông tin database đều được lấy từ file .env
```

### 2. Khởi động Database
```bash
docker-compose up -d
```

### 3. Kiểm tra kết nối Database
```bash
python test_db_connection.py
```

### 4. Cài đặt Python dependencies
```bash
docker-compose ps
```

```bash
docker-compose ps
```

### 5. Truy cập Database
- **PostgreSQL**: localhost:5432
  - Database: tich_tich_db
  - Username: admin
  - Password: password123

- **PgAdmin**: http://localhost:8080
  - Email: admin@tichtich.com
  - Password: admin123

### 6. Kết nối từ PgAdmin
1. Mở http://localhost:8080
2. Đăng nhập với thông tin trên
3. Thêm server mới:
   - Host: postgres (tên container)
   - Port: 5432
   - Database: tich_tich_db
   - Username: admin
   - Password: password123

## Lệnh hữu ích

### Xem logs
```bash
docker-compose logs postgres
docker-compose logs pgadmin
```

### Kết nối trực tiếp PostgreSQL
```bash
docker exec -it tich_tich_db psql -U admin -d tich_tich_db
```

### Backup database
```bash
docker exec tich_tich_db pg_dump -U admin -d tich_tich_db > backup.sql
```

### Restore database
```bash
docker exec -i tich_tich_db psql -U admin -d tich_tich_db < backup.sql
```

### Dừng services
```bash
docker-compose down
```

### Dừng và xóa volumes (dữ liệu sẽ mất)
```bash
docker-compose down -v
```

## Cấu trúc Files
```
.
├── docker-compose.yml      # Cấu hình Docker services
├── init-db/               # Scripts khởi tạo database
│   └── 01-init-schema.sql # Schema và dữ liệu mẫu
└── README.md              # Hướng dẫn này
```

## Sử dụng SQLAlchemy

### 1. Cài đặt Python dependencies
```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv
venv\Scripts\activate  # Windows

# Cài đặt packages
pip install -r requirements.txt
```

### 2. Kiểm tra kết nối database
```bash
python test_db_connection.py
```

### 3. Chạy FastAPI server
```bash
python main.py
```

### 4. API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Test API
```bash
python test_api.py
```

## Cấu trúc SQLAlchemy
- **models.py**: Định nghĩa các bảng (Customer, Child, Wallet)
- **schemas.py**: Pydantic schemas cho API
- **crud.py**: Các hàm thao tác database
- **database.py**: Cấu hình kết nối database
- **main.py**: FastAPI application

## API Endpoints
- `POST /customers/`: Tạo khách hàng mới
- `GET /customers/`: Lấy danh sách khách hàng
- `GET /customers/{user_id}`: Lấy thông tin khách hàng và con cái
- `POST /children/`: Tạo con cái mới
- `GET /children/parent/{parent_id}`: Lấy con cái theo parent
- `GET /wallets/{child_id}`: Lấy thông tin ví
- `PUT /wallets/{child_id}`: Cập nhật ví
- `POST /wallets/{child_id}/add-money`: Thêm tiền vào ví
- `POST /wallets/{child_id}/spend`: Chi tiêu từ ví

## Lưu ý Security
- **Không bao giờ commit file .env** vào git
- Tất cả thông tin database được lấy từ environment variables
- Thay đổi SECRET_KEY trong production
- Sử dụng mật khẩu mạnh cho database trong production
- File .env.example chỉ để tham khảo, không chứa thông tin thật

## Lưu ý
- Database schema được tạo tự động từ Docker
- Dữ liệu được thao tác qua SQLAlchemy ORM  
- Trigger PostgreSQL vẫn hoạt động (tự động tạo wallet, tính total)
- API sử dụng FastAPI với Pydantic validation
- Tất cả cấu hình database phải được đặt trong file .env
