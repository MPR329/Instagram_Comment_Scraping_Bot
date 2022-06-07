import fasttext
import json
import os

import numpy as np
import matplotlib.pyplot as plt



PRETRAINED_MODEL_PATH = "fasttext/lid.176.bin"
model = fasttext.load_model(PRETRAINED_MODEL_PATH)

commentsFiles = os.listdir("Bot/SCRAPED_DATA_ONLY")

globalLang = list()
globalLang_and_perMatch = [[],[]]

for file in commentsFiles:
    # Opening JSON file
    with open('Bot/SCRAPED_DATA/'+file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    languagesList = list()

    for i in data:
        comment =  i["COMMENTS"]
        testing = model.predict(comment)
        #print(i["COMMENTS"], testing)
        #if testing[1][0] >= 0.80:
         #   languagesList.append(testing[0][0])
        #else:
        #    languagesList.append("unsure")
        languagesList.append(testing[0][0])
        globalLang.append(testing[0][0])


    languagesOccurences = list()
    uniqueLanguages = set(languagesList)

    for language in uniqueLanguages:
        languagesOccurences.append((language + " : ", languagesList.count(language)))
    print(file + "\n")
    globalLang_and_perMatch[1].append([file, sorted(languagesOccurences, key=lambda language: language[1])])
    print(sorted(languagesOccurences, key=lambda language: language[1]))
    print("\n")

    # Closing file
    fh.close()

languagesOccurencesGlobal = list()
uniqueLanguagesGlobal = set(globalLang)

for language in uniqueLanguagesGlobal:
    languagesOccurencesGlobal.append((language + " : ", globalLang.count(language)))

globalLang_and_perMatch[0].append(sorted(languagesOccurencesGlobal, key=lambda language: language[1]))

print(file + "\n")
print(sorted(languagesOccurencesGlobal, key=lambda language: language[1]))
print("\n")

print(globalLang_and_perMatch)


# creating the dataset


labels = map(lambda x: x[0], globalLang_and_perMatch[0][0][-10:])
valuesT = map(lambda x: x[1], globalLang_and_perMatch[0][0][-10:])

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
plt.xticks(rotation = 45)
ax.spines['left'].set_color(colorBar)        # setting up Y-axis tick color to red
ax.spines['top'].set_color(colorBar)
ax.spines['right'].set_color(colorBar)        # setting up Y-axis tick color to red
ax.spines['bottom'].set_color(colorBar)






#fig.set_xticklabels(fig.get_xticks(), rotation = 90)
 
# creating the bar plot

plt.bar(courses, values, color =colorBar,
        width = 0.4)


plt.xlabel("Langues", color = colorBar)
plt.ylabel("Nombre de commentaires", color = colorBar)
plt.title("Top 10 des langues en utilisant FastText", color = colorBar)
plt.show()
