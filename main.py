from fastapi import FastAPI
from database import engine
import models

# Tạo bảng nếu chưa có
models.Base.metadata.create_all(bind=engine)

from routers import customer, child, wallet  # import các router đã tạo

app = FastAPI(title="Tích Tích App API", version="1.0.0")

# Thêm các router vào app
app.include_router(customer.router)
app.include_router(child.router)
app.include_router(wallet.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)