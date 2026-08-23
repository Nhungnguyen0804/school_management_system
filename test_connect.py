from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://school_user:123456@localhost:5432/school_db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Kết nối thành công!")