import json
import os
import re
import csv
from turtle import pu
from datetime import datetime
import pandas as pd


publicationTime = list()

with open('ArsenalInfo/Copy of Arsenal - Match info (Responses) - 10 April, 16_00 - Form responses 1.csv', 'r') as file:
     reader = csv.reader(file)
     for row in reader:
        href = re.findall(r'https://www.instagram.com/p/(.*?)/', row[15])
        postPubTime = row[18]
        #print(href, postPubTime)
        publicationTime.append([href, postPubTime])

print(publicationTime)
commentsFiles = os.listdir("./Bot/SCRAPED_DATA_ONLY")
print(len(commentsFiles))
hrefDataFile = list()

timeLog = list()

for file in commentsFiles:
    href2 = re.findall(r'(.*?)_COMMENTS.txt', file)
    result = href2[0]
    hrefDataFile.append(result)

    for item in publicationTime:
        href3 = item[0]
        testing = re.findall(rf"{result}", str(href3))
        if testing:
            indexSheet = publicationTime.index(item)
            postPublicationTime = item[1]
            #print(file, result, postPublicationTime, indexSheet)
            with open('Bot/SCRAPED_DATA/'+file, 'r', encoding='utf-8') as fh:
                data = json.load(fh)

            for i in data:
                comment =  i["USERNAME"]
                commentPublication = i["TIME"]
                

                timeComment = datetime.strptime(commentPublication,"%H:%M:%S")
                timePost = datetime.strptime(postPublicationTime,"%H:%M:%S")

                delta = timeComment-timePost
                delta = re.findall(r'\d+:\d+:\d+', str(delta))
                timeLog.append([delta[0],file ,i])
                print(delta[0])

sortedTimeLog = sorted(timeLog,key=lambda timeLogItems: timeLogItems[0] ,reverse=True)
lengthS = len(sortedTimeLog)

topTwenty = sortedTimeLog[-20:]
print(topTwenty)

dataFinal = list()
for element in topTwenty:
    ind = 20-topTwenty.index(element)
    object2 = element[2]
    dataFinal.append([ind,object2["USERNAME"], object2["DATE"], object2["TIME"], object2["LIKES"], object2["REPLIES"], object2["COMMENTS"], object2["TAGS"], object2["HASHTAGS"], object2["ACCOUNT_STATUS"], element[0]])


dataFinal = sorted(dataFinal, key=lambda language: language[0])
print(dataFinal)

a = dataFinal
my_df = pd.DataFrame(a)

my_df.to_csv('my_csv.csv', index=False, header=False)
                
  