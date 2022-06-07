import json
import os


userList = list()

commentsFiles = os.listdir("Bot/SCRAPED_DATA_ONLY")

for file in commentsFiles:
    # Opening JSON file
    with open('Bot/SCRAPED_DATA/'+file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        comment =  i["USERNAME"]
        userList.append(comment)
    
    # Closing file
    fh.close()
    print(file)


print(len(userList))
userOccurences = list()
uniqueUsers = set(userList)
print(len(uniqueUsers))

for user in uniqueUsers:
    #print(user)
    userOccurences.append((user, userList.count(user)))

print(file + "\n")
print(sorted(userOccurences, key=lambda language: language[1]))
print("\n")

    