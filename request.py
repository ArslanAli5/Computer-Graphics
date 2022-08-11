import re
import requests
from html.parser import HTMLParser
s = requests.Session()
r = s.get('http://socialclub.rockstargames.com')
print(s.headers)
data = r.text
data1 = data.split('<')
token = data1[73]
token = token[61:153]
payload={'login': "arsxlanali@gmail.com",'password': "SQ786nQ@z",'__RequestVerificationToken':token}
req = s.post('http://socialclub.rockstargames.com',data = payload)
print(token)
