# ============================================================
# 第 3 课：调用 DeepSeek API
# ============================================================
# 把"对接 AI"拆开来看，本质就是一次 POST 请求
# 和你刚才学的一模一样，只是多发两个东西：headers（身份验证）和 messages（对话内容）

import json
import requests

# 1. 读取 API Key（不写死在代码里，防止泄露）
with open('secmentor_web/settings.local.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 2. 准备请求
# ===== headers：告诉服务器"我是谁" =====
headers = {
    'Authorization': f'Bearer {config["deepseek_key"]}',
    'Content-Type': 'application/json',
}

# ===== data：你要发给 AI 的内容 =====
data = {
    'model': 'deepseek-chat',
    'messages': [
        {
            'role': 'system',
            'content': '你是一个Web安全专家，擅长分析漏洞。回答要简洁，不超过3句话。'
        },
        {
            'role': 'user',
            'content': '什么是SQL注入？'
        }
    ]
}

# 3. 发 POST 请求 —— 和之前学的完全一样！
print('正在调用 DeepSeek...')
resp = requests.post(
    'https://api.deepseek.com/v1/chat/completions',
    headers=headers,
    json=data
)

print('状态码:', resp.status_code)

# 4. 拿回 AI 的回答
result = resp.json()
ai_reply = result['choices'][0]['message']['content']
print('\nAI 回复:', ai_reply)
