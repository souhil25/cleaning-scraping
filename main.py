from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import random
import pymysql
import re
import socket

MAX_PAGES = 20

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='0215', db='scraping')
cur = conn.cursor()
cur.execute("USE Wikipedia")

random.seed(datetime.now().timestamp())

def insertPageIfNotExists(url):
    cur.execute("SELECT * FROM pages WHERE url = %s", (url,))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO pages (url) VALUES (%s)", (url,))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]
    
def insertLink(fromPageId, toPageId):
    cur.execute("SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s",
    (int(fromPageId), int(toPageId)))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)",
        (int(fromPageId), int(toPageId)))
        conn.commit()
    
pages = set()
def getLinks(pageUrl, recursionLevel):
    global pages
    if recursionLevel > 4:
        return
    print(f"[Lvel {recursionLevel}] Visiting: {pageUrl}")
    if len(pages) >= MAX_PAGES:
        print("Reached max page limit.Stooping crawl.")
        return
    pageId = insertPageIfNotExists(pageUrl)
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html, features="lxml")
    for link in bsObj.find_all("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        insertLink(pageId, insertPageIfNotExists(link.attrs['href']))
        if link.attrs['href'] not in pages:
            newPage = link.attrs['href']
            pages.add(newPage)
            getLinks(newPage, recursionLevel+1)

getLinks("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()