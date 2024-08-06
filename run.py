import os
import paramiko
import requests
import json
from datetime import datetime, timezone, timedelta

def ssh_multiple_connections(hosts_info, command):
    users = []
    for host_info in hosts_info:
        hostname = host_info['hostname']
        username = host_info['username']
        password = host_info['password']
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=22, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command)
            user = stdout.read().decode().strip()
            users.append(user)
            ssh.close()
        except Exception as e:
            print(f"连接 {hostname} 时出错: {str(e)}")
    return users

hosts_info = []
ssh_info_str = os.getenv('SSH_INFO', '[]')
hosts_info = json.loads(ssh_info_str)

command = 'whoami'
user_list = ssh_multiple_connections(hosts_info, command)

beijing_timezone = timezone(timedelta(hours=8))

time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')

loginip = requests.get('https://api.ipify.org?format=json').json()['ip']

pushplus_token = os.getenv('PUSHPLUS_TOKEN')

title = 'serv00 服务器登录提醒'
content = f"<style> body { margin: 0; height: 100vh; background: linear-gradient(135deg, rgba(255, 182, 193, 0.5), rgba(255, 105, 180, 0.5), rgba(255, 255, 255, 0.5), rgba(135, 206, 250, 0.5), rgba(173, 216, 230, 0.5), rgba(240, 128, 128, 0.5), rgba(221, 160, 221, 0.5)); background-size: 300% 300%; animation: gradient 10s ease infinite; font-family: Arial, sans-serif; display: flex; flex-direction: column; justify-content: space-between; } @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } } .container { text-align: center; margin-top: 50px; } .button { display: block; width: 80%; margin: 10px auto; padding: 15px; color: black; text-align: center; text-decoration: none; border-radius: 10px; background: rgba(255, 255, 255, 0.3); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px); transition: background 0.3s, box-shadow 0.3s; } .button:hover { background: rgba(255, 255, 255, 0.5); box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); } footer { text-align: center; padding: 20px; background-color: rgba(255, 255, 255, 0.5); border-top: 1px solid #ddd; backdrop-filter: blur(10px); } footer img { vertical-align: middle; } footer a { text-decoration: none; color: #007BFF; } footer a:hover { text-decoration: underline; } </style>"
url = 'http://www.pushplus.plus/send'
data = {
    "token": pushplus_token,
    "title": title,
    "content": content,
    "channel":"mail"
    "template":"html"
    
}
body = json.dumps(data).encode(encoding='utf-8')
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=body, headers=headers)
if response.status_code == 200:
    print("推送成功")
else:
    print(f"推送失败，状态码: {response.status_code}")
