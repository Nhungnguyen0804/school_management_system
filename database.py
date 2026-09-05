from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+psycopg://school_user:123456@localhost:5432/school_db"

engine = create_engine(DATABASE_URL)
class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)

# Dependency dùng cho FastAPI: tạo session mới mỗi request, đóng lại sau khi xong
def get_db():
    db = SessionLocal() # Khởi tạo session mới ngay khi có request gửi tới.
    try:
        yield db # Cung cấp session đó cho API endpoint sử dụng để truy vấn/thao tác dữ liệu.
        # cơ chế yield (Context Manager)
    finally:
        db.close() # Ngay sau khi API trả về kết quả cho client (hoặc xảy ra lỗi trong quá trình xử lý), đoạn mã sau yield sẽ luôn được gọi để đóng session.