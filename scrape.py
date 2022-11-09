## Given an input, gets the associated discount codes

import re
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import *

def search(target, text, context=2):
    # It's easier to use re.findall to split the string, 
    # as we get rid of the punctuation
    words = re.findall(r'\w+', text)
    if len(words) == 0: return
    
    matches = (i for (i,w) in enumerate(words) if w.lower() == target)
    for index in matches:
        if index < context //2:
            yield words[0:context+1]
        elif index > len(words) - context//2 - 1:
            yield words[-(context+1):]
        else:
            yield words[index - context//2:index + context//2 + 1]
            

## TODO: replace with vars
numLimit = 10
videosSearch = CustomSearch('Princess Polly', VideoSortOrder.uploadDate, limit = numLimit)
result = videosSearch.result()

# get urls of videos
urls = []
for x in result["result"]:
    try:
        link = x["link"]
        urls.append(link)
    except: 
        print("error, no youtube link")

# grab all the descriptions
# TODO: make this more legible, rename vars
codes = []
codes2 = {}
for link in urls: 
    soup = BeautifulSoup(requests.get(link).content, features="html.parser")
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    description = pattern.findall(str(soup))[0].replace('\\n','\n')
    
    # find the word "code" in the youtube video description, get the surrounding words
    codeWordList = list(search('code', description))
    
    # if "code" exists, add it to the list of codes
    if len(codeWordList) > 0:
        codes.append(codeWordList)
        codes2[link] = codeWordList
        
# print everything out
# youtubeURL : code phrase
for code in codes2:
    print(code, ":", codes2[code][0])

