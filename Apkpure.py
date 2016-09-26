import requests

url = "https://apkpure.com/tools"
proxies = {'https': "socks5://127.0.0.1:1080"}

request = requests.get(url, proxies=proxies, timeout=1)
content = request.text
print content
