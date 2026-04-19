'''
Date         : 2026-04-19 23:35:27 星期0
Author       : xut
Description  : 
'''
from urllib.parse import urlsplit

from urllib.parse import urlsplit

url = "https://admin:secret@www.example.com:8080/path/to/file?query=1#top"
result = urlsplit(url)

print("--- 核心字段 ---")
print(f"scheme  : {result.scheme}")   # https
print(f"netloc  : {result.netloc}")   # admin:secret@www.example.com:8080
print(f"path    : {result.path}")     # /path/to/file
print(f"query   : {result.query}")    # query=1
print(f"fragment: {result.fragment}") # top

print("\n--- 辅助属性 ---")
print(f"username: {result.username}") # admin
print(f"password: {result.password}") # secret
print(f"hostname: {result.hostname}") # www.example.com
print(f"port    : {result.port}")     # 8080

print("\n--- 获取原始 URL ---")
print(result.geturl()) 
# https://admin:secret@www.example.com:8080/path/to/file?query=1#top