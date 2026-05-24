from flask import Flask, render_template, request

app = Flask(__name__)

import json

with open('rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

def analyze(vuln):
    vuln = vuln.lower()
    for rule in rules:
        for kw in rule["keyword"]:
            if kw in vuln:
                return {
                    "type": rule["type"],
                    "risk": rule["risk"],
                    "evidence": rule["evidence"],
                    "suggest": rule["suggest"],
                }
    return {
        "type": "未知漏洞",
        "risk": "未知",
        "evidence": "未识别漏洞类型",
        "suggest": "请提供更多信息进行分析"
    }


history = []
@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""

    if request.method == 'POST':
        action =request.form.get('action', 'analyze')
        
        if action == 'analyze':
            vuln = request.form['vuln']
            result = analyze(vuln)
            history.append((vuln, result))
        elif action == 'clear':
            history.clear()
            result = ""

    return render_template('index.html', result=result, history=history)


if __name__ == '__main__':
    app.run(debug=True)