# test_agent.py
from agent import agent

response = agent.invoke({
    "messages": [{"role": "user", "content": "Hiện có bao nhiêu học sinh trong database?"}]
})

for msg in response["messages"]:
    print(msg)