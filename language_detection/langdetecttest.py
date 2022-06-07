
import json
import emoji
import re
from langdetect import detect
from langdetect import detect_langs

RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

def strip_emoji(text):
    return RE_EMOJI.sub(r'', text)

def strip_emoji2(text):
    #r'[^A-Za-z0-9 ]+'
    #return re.sub('\W', '', text)
    return re.sub(r'[^A-Za-z0-9 ]+', '', text)

def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False

# Opening JSON file
with open('Bot/SCRAPED_DATA/CaYDo6rqqrI_COMMENTS.txt', 'r', encoding='utf-8') as fh:
    data = json.load(fh)

# Iterating through the json
# list

errorList = 0
languagesList = list()

print(len(data))

for i in data:
    
    comment =  i["COMMENTS"]
    
    try:
        testing = detect(comment)
        if testing=="fr":
           print(testing + " : " + comment)
        languagesList.append(testing)
    except:
        #print("comment : " + comment)
        #print(i["ID"], data.index(i), "emoji(s)", i["COMMENTS"])
        errorList = errorList + 1
        languagesList.append("emoji")

print(errorList)
print(languagesList)
print(len(languagesList))

languagesOccurences = list()
uniqueLanguages = set(languagesList)

for language in uniqueLanguages:
    languagesOccurences.append((language + " : ", languagesList.count(language)))

print(sorted(languagesOccurences, key=lambda language: language[1]))



    



  

  
# Closing file
fh.close()