from bs4 import BeautifulSoup,NavigableString, Tag
from bs4.dammit import EncodingDetector
import requests
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import codecs

def html_to_text(html):
    "Creates a formatted text email message as a string from a rendered html template (page)"
    soup = BeautifulSoup(html, 'html.parser')
    # Ignore anything in head
    body, text = soup.body, []
    for element in body.descendants:
        # We use type and not isinstance since comments, cdata, etc are subclasses that we don't want
        if type(element) == NavigableString:
            parent_tags = (t for t in element.parents if type(t) == Tag)
            hidden = False
            for parent_tag in parent_tags:
                # Ignore any text inside a non-displayed tag
                # We also behave is if scripting is enabled (noscript is ignored)
                # The list of non-displayed tags and attributes from the W3C specs:
                if (parent_tag.name in ('area', 'base', 'basefont', 'datalist', 'head', 'link',
                                        'meta', 'noembed', 'noframes', 'param', 'rp', 'script',
                                        'source', 'style', 'template', 'track', 'title', 'noscript') or
                    parent_tag.has_attr('hidden') or
                    (parent_tag.name == 'input' and parent_tag.get('type') == 'hidden')):
                    hidden = True
                    break
            if hidden:
                continue

            # remove any multiple and leading/trailing whitespace
            string = ' '.join(element.string.split())
            if string:
                if element.parent.name == 'a':
                    a_tag = element.parent
                    # replace link text with the link
                    string = a_tag['href']
                    # concatenate with any non-empty immediately previous string
                    if (    type(a_tag.previous_sibling) == NavigableString and
                            a_tag.previous_sibling.string.strip() ):
                        text[-1] = text[-1] + ' ' + string
                        continue
                elif element.previous_sibling and element.previous_sibling.name == 'a':
                    text[-1] = text[-1] + ' ' + string
                    continue
                elif element.parent.name == 'p':
                    # Add extra paragraph formatting newline
                    string = '\n' + string
                text += [string]
    doc = '\n'.join(text)
    return doc

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
    


    openFile5 = open(saveToFile1,'r')
    saveToFile2 = str(df['Updated Company Name'][i])+'Html.html'
    for line in openFile5:
        requestHtml = requests.get(line)
        htm = requestHtml.content
        openFile6 = open(saveToFile2,'a')
        openFile6.write(str(htm))
        saveToFile3= str(df['Updated Company Name'][i])+'Data.txt'
        for contents in saveToFile2:
            openFile7 = open(saveToFile3,'a')
            txt = codecs.open(saveToFile2,'r')
            html = txt.read()
            ouput =html_to_text(html)
            openFile7.close()
    openFile5.close()
    openFile6.close()
    print
