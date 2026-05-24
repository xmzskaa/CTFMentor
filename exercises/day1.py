#练习1
name="Alice"
print(name)

for i in range(5):
    print(i)

age=20
if age>=18:
    print("You are an adult.")

def hello():
    print("Hello, SeMentor")

hello()


#练习2
def say_hi():
    print("hello,你好呀！")

say_hi()


def hello(name):
    print("欢迎你",name)

hello("Alice")


def add(a,b):
    return a+b

result=add(3,6)
print(result)


def hack():
    print("开始学习网安知识")

hack()


def a():
    print("1")

def b():
    print("2")

a()
b()
a()

def sql():
    print("检测SQL注入中...")

sql()


#练习3
'''def analyze(vuln):
    print("正在分析",vuln)

analyze("SQL注入")
analyze("XSS")
analyze("文件上传")'''


def learn(topic):
    print("正在学习",topic)

learn("Web安全")
learn("Python")
learn("Flask")


#练习4
def scan(vuln):
    return "检测到："+vuln

result1=scan("SQL注入")
result2=scan("XSS")

print(result1)
print(result2)


def level(score):
    if score>=90:
        return "优秀"
    elif score>=60:
        return "及格"
    else:
        return "继续努力"
    
print(level(95))
print(level(75))
print(level(40))


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
    
print(analyze("SQL注入"))
print(analyze("XSS"))
print(analyze("文件上传"))
print(analyze("CSRF"))