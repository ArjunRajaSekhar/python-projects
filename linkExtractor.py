from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('MASTER.xlsx', sheetname='360 Company Profiles')
print("Column headings:")
print(df.columns)
for i in df.index:
    print(df['Website'][i])
    url=df['Website'][i]
    ##url=input("enter the full url")  # To input the url address
    resp = requests.get(url)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content,"lxml", from_encoding=encoding)


    #promts the user for the file which the links needs to be stored
    saveToFile1=str(df['Updated Company Name'][i])+'.txt'
    openFile = open('output.txt','w')

    #write links to the file
    for link in soup.find_all('a', href=True):
        openFile.write(link['href'])
        openFile.write('\n')
    ##    print(link['href'])
    openFile.close()


    #To remove any thing other than links.
    openFile3 = open('output.txt','r')
    lines =openFile3.readlines()
    openFile3.close()
    openFile3 = open('output.txt','w')
    for line in lines:
        if line!='#'+'\n':
            if line.startswith('http'):
                openFile3.write(line)
    openFile3.close()



    lines_seen = set() # holds lines already seen
    openFile2 = open(saveToFile1, 'w')
    for line in open("output.txt", 'r'):
        if line not in lines_seen: # not a duplicate
            openFile2.write(line)
            lines_seen.add(line)
    openFile2.close()




    #To print cleane text file
    openFile4 =open(saveToFile1,'r')
    for line in openFile4:
         print(line)
    openFile4.close()
