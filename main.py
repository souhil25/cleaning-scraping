from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import defaultdict

def cleanInput(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('[[0-9]*]', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(input, n):
    input = cleanInput(input)    
    output = []
    for i in range(len(input)-n+1):
        output.append(tuple((input[i:i+n])))
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, features="lxml")
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
ngrams_list = ngrams(content, 2)
ngrams_counts = defaultdict(int)
for ng in ngrams_list :
    ngrams_counts[ng] += 1

sorted_ngrams = dict(sorted(ngrams_counts.items(), key=lambda item: item[1], reverse=True))
print(sorted_ngrams)
print("2-grams count is: ", len(sorted_ngrams))

