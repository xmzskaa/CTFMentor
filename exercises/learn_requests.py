# ============================================================
# 第 2 课：POST 请求 —— 带着数据发给服务器
# ============================================================
# 前置条件：先启动 Flask —— cd secmentor_web && python app.py

import requests

# ===== GET：只拿数据，不发送 =====
print('=== GET 请求（拿数据）===')
resp = requests.get('http://127.0.0.1:5000/api/test')
print('返回:', resp.json())

print()

# ===== POST：把数据发过去 =====
print('=== POST 请求（发数据）===')

# 你要发给服务器的数据
my_data = {"vuln": "SQL注入漏洞"}

# requests.post(url, json=数据) — 把数据打包成 JSON 发过去
resp = requests.post('http://127.0.0.1:5000/api/analyze', json=my_data)

print('状态码:', resp.status_code)
print('服务器返回:', resp.json())
