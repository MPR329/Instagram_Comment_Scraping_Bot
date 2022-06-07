import json
import os
import re
import pandas as pd


userList = list()

commentsFiles = os.listdir("Bot/SCRAPED_DATA_ONLY")

for file in commentsFiles:
    print(file)
    # Opening JSON file
    with open('Bot/SCRAPED_DATA/'+file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        comment =  i["COMMENTS"]
        replies = i["REPLIES"]
        #print(likes)
        replies2 = re.sub("[^0-9]", "", str(replies))
        #print(likes)
        if replies != "":
            userList.append([i, int(replies2), file])
        else:
            print("Error" + " : " + likes)
    # Closing file
    fh.close()
    print(file)


print(len(userList))

listNo = sorted(userList, key=lambda language: language[1])
#print(userList)
topTwenty = listNo[-20:]
print(topTwenty)

data1 = map(lambda x: x[0], topTwenty)
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