import json
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv


userList = list()

commentsFiles = os.listdir("Bot/SCRAPED_DATA_ONLY")

for file in commentsFiles:
    print(file)
    # Opening JSON file
    with open('Bot/SCRAPED_DATA/'+file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        comment =  i["COMMENTS"]
        likes = i["LIKES"]
        #print(likes)
        result = re.search(r'[a-zA-Z]', str(likes))
        if result:
            print("Letters in string")
        else:
            likes2 = re.sub("[^0-9]", "", str(likes))
            if likes2 != "":
                userList.append([i, int(likes2), file])
            else:
                print("Error" + " : " + likes)
    # Closing file
    fh.close()
    print(file)


print(len(userList))

listNo = sorted(userList, key=lambda language: language[1])
#print(userList)
toptwenty = listNo[-20:]
print(toptwenty)
print("\n")

headers = ['Rank','USERNAME', 'DATE','TIME','LIKES','REPLIES','COMMENT','TAGS','HASHTAGS','ACCOUNT_STATUS',]
#data = map(lambda x: [x["USERNAME"], x["DATE"], x["TIME"], x["LIKES"], x["REPLIES"], x["COMMENTS"], x["TAGS"], x["HASHTAGS"], x["ACCOUNT_STATUS"]], toptwenty)
data1 = map(lambda x: x[0], toptwenty)
data1 = list(data1)
dataFinal = list()
for object in data1:
    ind = 20-data1.index(object)
    dataFinal.append([ind,object["USERNAME"], object["DATE"], object["TIME"], object["LIKES"], object["REPLIES"], object["COMMENTS"], object["TAGS"], object["HASHTAGS"], object["ACCOUNT_STATUS"]])

dataFinal = sorted(dataFinal, key=lambda language: language[0])
print(dataFinal)


a = dataFinal
my_df = pd.DataFrame(a)

my_df.to_csv('my_csv.csv', index=False, header=False)