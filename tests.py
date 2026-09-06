from agent_tools import get_database_schema, query_database

'''
để chạy đc
phải connect postgre đã
mở docker lên
'''
print("--- Schema ---")
print(get_database_schema.invoke({}))
print("\n--- Query test ---")
print(query_database.invoke({"sql_query": "SELECT * FROM students"}))

'''
bấm run file này
output:
--- Schema ---
Table alembic_version: version_num (VARCHAR(32))
Table divisions: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP)
Table classes: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP)
Table enrollments: id (UUID), student_id (UUID), class_id (UUID), created_at (TIMESTAMP), updated_at (TIMESTAMP)
Table students: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP)
Table teach: id (UUID), teacher_id (UUID), class_id (UUID), created_at (TIMESTAMP), updated_at (TIMESTAMP)
Table teachers: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP), division_id (UUID)

--- Query test ---
[]
'''