from flask import Flask, render_template, request

app = Flask(__name__)


def analyze(vuln):

    vuln = vuln.lower()

    # SQL注入检测
    if "'" in vuln or "union" in vuln or "select" in vuln:
        return """漏洞类型：SQL注入

风险等级：高

检测依据：
发现SQL关键字或单引号注入特征

建议：
1. 使用参数化查询
2. 禁止字符串拼接SQL
3. 做输入过滤"""

    # XSS检测
    elif "<script>" in vuln or "alert(" in vuln:
        return """漏洞类型：XSS

风险等级：中高

检测依据：
发现JavaScript脚本特征

建议：
1. 输出转义
2. 开启 CSP
3. 过滤危险标签"""

    # 文件上传检测
    elif ".php" in vuln or ".jsp" in vuln:
        return """漏洞类型：恶意文件上传

风险等级：高

检测依据：
发现危险脚本文件后缀

建议：
1. 校验文件类型
2. 限制上传目录执行权限
3. 重命名上传文件"""

    else:
        return """未识别漏洞类型

请尝试：
1. SQL注入payload
2. XSS脚本
3. 文件上传文件名"""


@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""

    if request.method == 'POST':
        vuln = request.form['vuln']
        result = analyze(vuln)

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)