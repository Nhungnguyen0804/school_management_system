from langchain_core.tools import tool
from sqlalchemy import inspect, text
from database import SessionLocal, engine

'''
Docstring ("""...""") không phải comment thường — LLM đọc chính đoạn này
để quyết định có nên gọi tool này không. Viết docstring mơ hồ → LLM chọn sai tool.

Ý tưởng: query trực tiếp vào Postgres system catalog (information_schema) để lấy danh sách bảng + cột
— không hard-code tay, vì schema có thể đổi ( như thêm schema Division)
'''
@tool
def get_database_schema() -> str:
    """Trả về thông tin schema của database: tên bảng, các cột, kiểu dữ liệu."""

    # đây là đọc trực tiếp Postgres, đảm bảo luôn khớp với DB thật, kể cả nếu ai đó sửa DB không qua Alembic).
    inspector = inspect(engine) # công cụ SQLAlchemy để đọc ngược schema thật từ DB (khác với đọc models.py
    schema_info = []

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_descriptions = []
        for col in columns:
            column_descriptions.append(f"{col['name']} ({col['type']})")

        schema_info.append(f"Table {table_name}: {', '.join(column_descriptions)}")

    return "\n".join(schema_info)



'''
startswith("select") --> Chưa đủ 100%, đây chỉ là lớp chặn đầu tiên (basic)
Ví dụ LLM vẫn có thể viết: SELECT * FROM students; DROP TABLE students; (multiple statements)

check này đủ để hiểu nguyên tắc "phải validate trước khi execute"
nó chưa production-ready.

Cách production thật thường dùng:

User DB riêng cho Agent, chỉ có quyền SELECT ở tầng Postgres (GRANT SELECT ONLY) — đây là an toàn thật sự, không dựa vào check string dễ bị qua mặt.
Không cho phép chạy nhiều statement trong 1 lần gọi.

an toàn không nằm ở 1 lớp check, mà nằm ở nhiều lớp phòng thủ (defense in depth).


Test riêng (chưa cần LLM), gọi thử bằng tay:
print(get_database_schema.invoke({}))
print(query_database.invoke({"sql_query": "SELECT * FROM students"}))


'''
@tool
def query_database(sql_query: str) -> str:
    """
    Chạy 1 câu SQL SELECT để đọc dữ liệu từ database.
    Chỉ được dùng cho câu lệnh SELECT, không dùng để thêm/sửa/xoá dữ liệu.
    """
    # Validation: chặn ngay từ đầu nếu không phải SELECT
    normalized = sql_query.strip().lower()
    if not normalized.startswith("select"):
        return "Lỗi: chỉ được phép chạy câu lệnh SELECT."

    db = SessionLocal()
    try:
        result = db.execute(text(sql_query))
        rows = result.fetchall()
        return str(rows)
    except Exception as e:
        return f"Lỗi khi chạy query: {str(e)}"
    finally:
        db.close()