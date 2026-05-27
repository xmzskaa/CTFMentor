from flask import Flask, render_template, request, session, redirect, url_for
import json
import requests
import base64

app = Flask(__name__)
app.secret_key = 'secmentor-secret-2026'


def load_config():
    with open('settings.local.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def build_prompt(mode):
    """根据模式生成提示词"""
    if mode == 'answer':
        return (
            '你是一个CTF竞赛教练。用户会贴一段CTF题目，你需要给出完整答案。'
            '返回一个JSON对象，格式必须为：'
            '{"category":"题目类型(Web/Crypto/Reverse/Pwn/Misc)",'
            '"technique":"考察的技术点",'
            '"difficulty":"难度评估(入门/简单/中等/困难)",'
            '"solution":"完整解题步骤(用序号列出，包含具体命令和代码)",'
            '"payload":"关键攻击载荷或exp代码",'
            '"flag":"flag值(如果题目没给具体flag，写推导过程和flag格式)",'
            '"pitfalls":"常见踩坑点"}'
            '只返回JSON，不要加```标记或其他文字。'
        )
    else:
        return (
            '你是一个CTF竞赛教练，擅长引导新手解题。'
            '用户会贴一段CTF题目描述或代码，你需要分析并返回一个JSON对象。'
            '格式必须为：'
            '{"category":"题目类型(Web/Crypto/Reverse/Pwn/Misc)",'
            '"technique":"考察的技术点",'
            '"difficulty":"难度评估(入门/简单/中等/困难)",'
            '"hints":"分步解题思路(用序号列出，每步不超过一句话，最后一步不要给出最终flag，只给提示)",'
            '"payload":"关键攻击载荷或代码模板(如果没有则为空)",'
            '"pitfalls":"常见踩坑点"}'
            '风格要求：不直接给答案，引导用户自己思考。只返回JSON，不要加```标记或其他文字。'
        )


def analyze_ctf(description, mode='hint'):
    """DeepSeek 分析文字题目"""
    config = load_config()

    headers = {
        'Authorization': f'Bearer {config["deepseek_key"]}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': build_prompt(mode)},
            {'role': 'user', 'content': description},
        ],
    }

    resp = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=60,
    )

    result = resp.json()

    if 'choices' not in result:
        raise Exception(f'API返回异常: {result}')

    ai_text = result['choices'][0]['message']['content'].strip()

    if ai_text.startswith('```'):
        ai_text = ai_text.split('\n', 1)[1]
    if ai_text.endswith('```'):
        ai_text = ai_text[:-3]

    parsed = json.loads(ai_text)
    parsed['mode'] = mode
    return parsed


def analyze_image(image_bytes, description, mode='hint'):
    """SiliconFlow 视觉模型分析图片题目"""
    config = load_config()

    image_b64 = base64.b64encode(image_bytes).decode('utf-8')

    headers = {
        'Authorization': f'Bearer {config["siliconflow_key"]}',
        'Content-Type': 'application/json',
    }

    prompt = build_prompt(mode)
    if description:
        prompt += f'\n用户的补充描述：{description}'

    data = {
        'model': 'Qwen/Qwen3-VL-8B-Instruct',
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/png;base64,{image_b64}'},
                    },
                    {'type': 'text', 'text': prompt},
                ],
            }
        ],
    }

    resp = requests.post(
        'https://api.siliconflow.cn/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=90,
    )

    result = resp.json()
    ai_text = result['choices'][0]['message']['content'].strip()

    if ai_text.startswith('```'):
        ai_text = ai_text.split('\n', 1)[1]
    if ai_text.endswith('```'):
        ai_text = ai_text[:-3]

    parsed = json.loads(ai_text)
    parsed['mode'] = mode
    return parsed


history = []


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action', 'analyze')

        if action == 'analyze':
            description = request.form.get('description', '')
            mode = request.form.get('mode', 'hint')
            uploaded_file = request.files.get('file')

            try:
                if uploaded_file and uploaded_file.filename:
                    filename = uploaded_file.filename.lower()
                    image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

                    if filename.endswith(image_exts):
                        image_bytes = uploaded_file.read()
                        result = analyze_image(image_bytes, description, mode)
                        title = f'[图片] {description[:40]}' if description else '[图片题目]'
                    else:
                        file_content = uploaded_file.read().decode('utf-8', errors='ignore')
                        full_text = f'文件：{uploaded_file.filename}\n内容：\n{file_content}'
                        if description:
                            full_text = description + '\n' + full_text
                        result = analyze_ctf(full_text, mode)
                        title = f'[{uploaded_file.filename}] {description[:30]}' if description else f'[{uploaded_file.filename}]'
                elif description.strip():
                    result = analyze_ctf(description, mode)
                    title = description[:50] + ('...' if len(description) > 50 else '')
                else:
                    session['result'] = ""
                    return redirect(url_for('home'))
            except Exception as e:
                result = {
                    'category': '错误',
                    'technique': str(e)[:100],
                    'difficulty': '--',
                    'hints': f'分析出错：{e}',
                    'payload': '',
                    'pitfalls': '请尝试缩短输入内容或稍后重试',
                    'mode': mode,
                }
                title = f'[出错] {description[:30]}' if description else '[分析出错]'

            history.append((title, result))
            session['result'] = result
            session['just_cleared'] = False
        elif action == 'clear':
            history.clear()
            session['result'] = ""
            session['just_cleared'] = True

        return redirect(url_for('home'))

    result = session.pop('result', "")
    just_cleared = session.pop('just_cleared', False)

    return render_template('index.html', result=result, history=history)


if __name__ == '__main__':
    app.run(debug=True)
