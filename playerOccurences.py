from sympy import per
from ArsenalInfo.AFC_players import players
import re
import json
import os
import copy
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt



for player in players:
    regex = r'\b(\w+)\b'
    result = re.findall(regex,player)
    ind = players.index(player)
    #print(result)
    if len(result)>1:
        players[ind] = [player, result[0]+"|"+result[1], 0]
    else:
        players[ind] = [player, result[0], 0]



commentsFiles = os.listdir("./Bot/SCRAPED_DATA_ONLY")




new_playersTotal = copy.deepcopy(players)
perMatchGlobal = list()

for file in commentsFiles:

    new_players = copy.deepcopy(players)
    playerOccurences_perMatch = list()
    
    # Opening JSON file
    with open('Bot/SCRAPED_DATA/'+file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)


    for i in data:
        comment =  i["COMMENTS"]
        for player in new_players:
            ind = new_players.index(player)
            result = re.findall(rf"{player[1]}", comment, re.IGNORECASE)
            if result:
                #print(comment, player)
                new_players[ind][2] = new_players[ind][2] + 1
                new_playersTotal[ind][2] = new_playersTotal[ind][2] + 1
    
    playerOccurences_perMatch.append([file, sorted(new_players, key=lambda player: player[2])[-5:]])
    #print(file + "\n")
    #print(playerOccurences_perMatch)
    perMatchGlobal.append(playerOccurences_perMatch)
    #print("\n")
    # Closing file
    fh.close()

occurencesGlobal = sorted(new_playersTotal, key=lambda player: player[2])
print(occurencesGlobal)
#print(perMatchGlobal)



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
        #print(data)
        csvData.append(data)

newList = list()

for item in perMatchGlobal:
    instaLink = re.findall(r'(.*?)_COMMENTS.txt', item[0][0])[0]
    #print(instaLink)
    #
    for data in csvData:
        instaLink2 = re.findall(r'https://www.instagram.com/p/(.*?)/', str(data[0]))
        if instaLink2:
            #print(instaLink2[0])
            if instaLink2[0] == instaLink:
                for x in data:
                    item[0].append(x)

#print(perMatchGlobal)
#print("\n")
#print("\n")
perMatchGlobal = sorted(perMatchGlobal, key=lambda x: datetime.strptime(x[0][6], '%d/%m/%Y'))
#print(perMatchGlobal)
#print(len(perMatchGlobal))
#print(len(perMatchGlobal[0]))



# creating the dataset

labels = map(lambda x: x[0], occurencesGlobal)
valuesT = map(lambda x: x[2], occurencesGlobal)

courses = list(labels)
values = list(valuesT)

print(courses)
print(values)

colorBar = "#63d297"
  
fig = plt.figure(figsize = (10, 5))


colorBG = "#202729"
plt.figure(facecolor=colorBG) 
ax = plt.axes() 
ax.set_facecolor(colorBG) 
ax.tick_params(axis='x', colors = colorBar)
ax.tick_params(axis='y', colors = colorBar)
plt.xticks(rotation = 90)
ax.spines['left'].set_color(colorBar)        # setting up Y-axis tick color to red
ax.spines['top'].set_color(colorBar)
ax.spines['right'].set_color(colorBar)        # setting up Y-axis tick color to red
ax.spines['bottom'].set_color(colorBar)






#fig.set_xticklabels(fig.get_xticks(), rotation = 90)
 
# creating the bar plot

plt.bar(courses, values, color =colorBar,
        width = 0.4)


#plt.xlabel("Langues", color = colorBar)
plt.ylabel("Occurences", color = colorBar)
plt.title("Nombre d'occurences pour chaque joueur d'AFC et quelques membres du staff", color = colorBar)
plt.show()


    