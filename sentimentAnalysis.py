import fasttext
import json
import os
import re
from sympy import true
from textblob import TextBlob
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt



PRETRAINED_MODEL_PATH = "fasttext/lid.176.bin"
model = fasttext.load_model(PRETRAINED_MODEL_PATH)

commentsFiles = os.listdir("Bot/SCRAPED_DATA_ONLY")

sentimentAnalList = list()

for file in commentsFiles:
    # Opening JSON file

    polaList = list()
    subjList = list()

    with open('Bot/SCRAPED_DATA/'+file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        comment =  i["COMMENTS"]
        testing = model.predict(comment)
        result = re.findall(r"'__label__(.*?)',", str(testing))
        if result[0] == "en":
            tb = TextBlob(comment)
            #print(tb.sentiment, comment)
            polaList.append(tb.sentiment[0])
            subjList.append(tb.sentiment[1])

    sumPola = 0
    sumSubj = 0
    for polarity in polaList:
        sumPola = sumPola + polarity
    for subjectivity in subjList:
        sumSubj = sumSubj + subjectivity

    print(sumPola/len(polaList), [len(polaList)], sumSubj/len(subjList), file)

    sentimentAnalList.append([sumPola/len(polaList), sumSubj/len(subjList), file])

print(sentimentAnalList)


csvData = list()

with open('ArsenalInfo/Copy of Arsenal - Match info (Responses) - 10 April, 16_00 - Form responses 1.csv', 'r') as file:
     reader = csv.reader(file)
     for row in reader:
        href = row[15]
        gameResult = row[5]
        position = row[25]
        opponent = row[4]
        date = row[2]
        data = [href, gameResult, position, opponent, date]
        print(data)
        csvData.append(data)

newList = list()

for item in sentimentAnalList:
    instaLink = re.findall(r'(.*?)_COMMENTS.txt', item[2])[0]
    print(instaLink)
    #
    for data in csvData:
        instaLink2 = re.findall(r'https://www.instagram.com/p/(.*?)/', str(data[0]))
        if instaLink2:
            print(instaLink2[0])
            if instaLink2[0] == instaLink:
                newList2 = list();
                for element in item:
                    newList2.append(element)
                for element in data:
                    newList2.append(element)
                newList.append(newList2)

newList = sorted(newList, key=lambda x: datetime.strptime(x[7], '%d/%m/%Y'))
print(newList)


colorBar = "#63d297"
colorBG = "#202729"

labels = map(lambda x: x[7]+" - "+x[6]+"\n"+"["+x[4]+"-->"+x[5]+"]", newList)
valuesA = map(lambda x: x[0], newList)
valuesB = map(lambda x: x[1], newList)

a = list(valuesA)
b = list(valuesB)
c = list(labels)

print(c)



plt.figure(facecolor=colorBG) 
ax = plt.axes() 
ax.set_facecolor(colorBG) 
ax.tick_params(axis='x', colors = colorBar)
ax.tick_params(axis='y', colors = colorBar)

plt.xticks(rotation = 45)

ax.spines['left'].set_color(colorBar)        # setting up Y-axis tick color to red
ax.spines['top'].set_color(colorBar)
ax.spines['right'].set_color(colorBar)        # setting up Y-axis tick color to red
ax.spines['bottom'].set_color(colorBar)

#plt.xticks(a, c, rotation ='vertical')

  

# naming the x-axis
#plt.xlabel('Commentaire sous chaque Post Instagram de chaque match', color = colorBar)
  
# naming the y-axis
#plt.ylabel('Polarité/Subjectivité', color = colorBar)
  
# gives a title to the Graph
plt.title('Moyenne de la polarité & subjectivité pour les commentaires sous chaque Post Instagram de chaque match', color = colorBar)

#ax = plt.gca()
#ax.legend(['polarité ', 'subjectivité '])
#plt.legend(labelcolor=colorBar)

plt.plot(c, a, label='polarité ')
plt.plot(b, label='subjectivité ')
plt.legend(loc="upper right")
#plt.legend(facecolor=colorBG)
plt.legend(labelcolor=colorBar, frameon=False)
  
plt.show()