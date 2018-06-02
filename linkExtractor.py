from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests 
url=input("enter the full url")
resp = requests.get(url)
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, from_encoding=encoding)

saveToFile1=input('enter the file name')
openFile = open(saveToFile1,'a')
for link in soup.find_all('a', href=True):
    openFile.write(link['href'])
    openFile.write('\n')
    print(link['href'])
openFile.close()

