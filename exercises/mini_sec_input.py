print("欢迎使用 SecMentor Mini")

def analyze(vuln):
    if vuln=="SQL注入":
        return "检测到数据库查询风险"
    elif vuln=="XSS":
        return "检测到脚本注入风险"
    elif vuln=="文件上传":
        return "检测到恶意文件上传风险"
    elif vuln=="SSRF":
        return "检测到服务端请求伪造风险"
    else:
        return "未知风险"
    
user_input=input("请输入漏洞类型：")

result=analyze(user_input)

print(result)
print("分析完成")