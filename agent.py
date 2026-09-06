# agent.py
# pip install langchain-google-genai
# pip install python-dotenv

# pip install --upgrade langchain-core langchain-google-genai langgraph langgraph-prebuilt langchain-openai
# cập nhật các gói lên bản mới hơn mà hỗ trợ langchain-core 0.3.x hoặc điều chỉnh lại các thư viện tương thích với nhau mà không làm hỏng venv.
# vẫn conflict nên kệ luôn :))
# pip check: đảm bảo không còn venv bị xung đột dependencies nào khác

# sai hết r
# version mới thì
#pip install langchain (khác langchain core) + from langchain.agents import create_agent

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from agent_tools import get_database_schema, query_database
import os
from dotenv import load_dotenv
# Tải các biến môi trường từ file .env
load_dotenv()

# Nhận API Key tự động từ file .env
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

tools = [get_database_schema, query_database]

agent = create_agent(llm, tools)
# create_react_agent(llm, tools) → LangGraph tự dựng sẵn graph ReAct loop ở trên,
#  không cần tự vẽ node/edge ở bước học này.
# Nó tự biết: khi nào gọi tool, khi nào dừng và trả lời cuối.

# pip install -U langgraph langchain-core langchain ==> ko giải quyet đc

# pip uninstall -y langchain langgraph langgraph-prebuilt langgraph-checkpoint langgraph-sdk langchain-core
# tải lại bằng:
# pip install langchain langgraph

# pip show langchain

# pip show langgraph

# output
'''
content='Hiện có bao nhiêu học sinh trong database?' additional_kwargs={} response_metadata={} id='75b805bc-1656-4cf0-a44a-3b16a3b7c7af'
content=[] additional_kwargs={'function_call': {'name': 'get_database_schema', 'arguments': '{}'}, '__gemini_function_call_thought_signatures__': {'call_3090809': 'ErwDCrkDARFNMg/mf9wnX9g4UNsJ6HzDoCtzVNOgxgaOgxhHL09ImyULrmY9/YivIu1S95ZNyKXvzGkRPQMX4xqImZx53tG5haOTcQVsyyLV1bvmSObNfPf2WlfbYKOKITcMCrEPLbBlywZmDYWg2nsLxmHZAji8oRAXwUuqmAYmDMEc7hUSmuLtFWOpoLDqSK8z+liD/dYIJ5T9AidJEj6o0LCp3Z7gCjaLS72Oj4R7HSWTuIrcX1m2jmeEN68jsC+YeKVs2Xk2WV+oHPxdSlBy21jIBXMc7Af3MZiTdA4qV4Z5RA549uOvs6BUgPCf9tCgE8tg+lNqgKLDiDWIPyzI1CwkPLtHCU/7B1pm3QeANHzpoQuO7uAO9VheaGN0oVIQMamJPzNo88ItOkp8Ja2J2A8oTVz2cIdBo4INH786kkpB4sMJ3+Z3uS0ZtPVsttIDmba4R/UcGaqPdwQwjfdfWa2g8n53MNfH0RmPUFnP7wOx+epFbv0pPPGQhc6c0bvreTIe+gSO3wsUU/qGo9RdlgBD8fv1D9qPSeVff7/hxP/sVYpEIFB3hEk+24jAq8Qo7pctffcwB5xhP40E'}} response_metadata={'finish_reason': 'STOP', 'model_name': 'gemini-3.5-flash', 'safety_ratings': [], 'model_provider': 'google_genai'} id='lc_run--01a077d3-afe8-76c3-af3a-e9a1344c119d-0' tool_calls=[{'name': 'get_database_schema', 'args': {}, 'id': 'call_3090809', 'type': 'tool_call'}] invalid_tool_calls=[] usage_metadata={'input_tokens': 121, 'output_tokens': 93, 'total_tokens': 214, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 81}}
content='Table alembic_version: version_num (VARCHAR(32))\nTable divisions: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP)\nTable classes: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP)\nTable enrollments: id (UUID), student_id (UUID), class_id (UUID), created_at (TIMESTAMP), updated_at (TIMESTAMP)\nTable students: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP)\nTable teach: id (UUID), teacher_id (UUID), class_id (UUID), created_at (TIMESTAMP), updated_at (TIMESTAMP)\nTable teachers: id (UUID), name (VARCHAR(100)), created_at (TIMESTAMP), updated_at (TIMESTAMP), division_id (UUID)' name='get_database_schema' id='db094c89-53ae-4d2a-982c-6ebff58cedbf' tool_call_id='call_3090809'
content=[] additional_kwargs={'function_call': {'name': 'query_database', 'arguments': '{"sql_query": "SELECT COUNT(*) AS total_students FROM students;"}'}, '__gemini_function_call_thought_signatures__': {'call_2359609': 'Ep4ECpsEARFNMg96LKsdlO/kUmfNaKue3AmzduUc4HtenZJFbsqM7jGVapSDoCZndkBGW3ecepstxAHJniSStsi/UXBRxNz333SysB2rehirkHWu0b79elawUlMMPfPjA6SAkowwlGOdK32uygNDolX5M13xyjt6SFsUNHCpzxpVFj7c/Vr3wtZ5D64gJutfIIq2enzNX2ymxJVYrceFKeNtPBAzDxbizIsm+bgezHoLhw/n8PmoSRZaXnLi9NxcJc3H/bOIxFR+fZJNrGrZrX4iurtnx/zahB6GYf6MC2S2xEvaED7y8Mitl/E8K/rzafRRr+SvezADTDnMzlnegniMO+PE9whe+LxKycPsm1xZyjP8hNnPlIpD+Acu57IJ5utJZM89WKxx8OpnWIV73aBhE1ymul5gGHkruUOm7CdcUggdMGcfIIxnCSJHWkaUdi9VfH0oOGIqpgD2HIa22Q5fivi2hyx9u8W+0njJRVFYJGnZ4baSXBJ6hccDR1jw1YoB1GoRDVejIJ/ihy1eSsMA3dSO+IwqeNpcbQ34G+5AktfCcLkgWYLUQJRAt8u7otmYhHICxlAIZ1DTre5znPwl3agHDw+8PItL+rGRIlwxxRoevPcyhKtX91Ytu7ca6dg8Y+QjeeIm+rx9T+Ocaea6zopbpd3gqfX6buQZSqqN0x3LUb3p+UBadPPgARGAsI9fEDIDHnXeTlpw96B+evo='}} response_metadata={'finish_reason': 'STOP', 'model_name': 'gemini-3.5-flash', 'safety_ratings': [], 'model_provider': 'google_genai'} id='lc_run--01a077d3-caa6-7341-9395-7d8d1f08de40-0' tool_calls=[{'name': 'query_database', 'args': {'sql_query': 'SELECT COUNT(*) AS total_students FROM students;'}, 'id': 'call_2359609', 'type': 'tool_call'}] invalid_tool_calls=[] usage_metadata={'input_tokens': 427, 'output_tokens': 144, 'total_tokens': 571, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 117}}
content='[(0,)]' name='query_database' id='8cf4ba49-a032-480f-b62c-37c1ac662593' tool_call_id='call_2359609'
content=[{'type': 'text', 'text': 'Hiện tại không có học sinh nào trong cơ sở dữ liệu (số lượng là 0).', 'extras': {'signature': 'EucDCuQDARFNMg/4BAaQaSYj579AELR5n6BttcIVkQOs1KrtT2IRfpOfCWT3eDKSStVZ25HerLI4NfoEVW01oam5b7pkYwxLWeYAAm6L3uDznHA3XA/4VdDQt7Qb6uvNdKhN6tvWE8ZFCRW81VJO5bNUYgure6vjrPEZay3tptlq22DUl/MNKaKJ9GMwxEusCdZ3BuTLseOJMMO1TZvVuSKV4ielUihnylSjvSJGPH9PEUxoFZ36VCwv5C1AzOxYsNStlh2jaZT6Gc2cUjhkztedgDwL6Qs0pRlBAwSnvW/pPrs1WQzZwxPnJ/BOhfuAaHxgVDoozv6PAY6Li5VWRLgogfAVYSJ8bi9EvGKgBvJIRKSATwQKL358WWsGQml7GYyF5uYK52ndQJSTe861B2Mi871V/oU4VsrourTGYgpayCV9TSykJ9Yd+Tes95jtLsOYFkK62ZFzuJ+2xdP3s8BzIyLXhRisjkIVWFuuf3bfC7EwbA6DL36RGLe3BtN1RgPd7nr3OAzb1VenSqS3DhD65GE3JmZSUuzJEpD8LdOBk8npddcVX5m4mmhZL6MNBKy0J8wtTySJWGDzeBELvq9LS65dHvBv2K3bZt4PAH/hq/z0eCRcpt/KyfhuB01RcPE7AcOtAD6etA=='}}] additional_kwargs={} response_metadata={'finish_reason': 'STOP', 'model_name': 'gemini-3.5-flash', 'safety_ratings': [], 'model_provider': 'google_genai'} id='lc_run--01a077d3-e3e6-7141-9d10-9d062f0c9840-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 588, 'output_tokens': 125, 'total_tokens': 713, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 106}}

'''