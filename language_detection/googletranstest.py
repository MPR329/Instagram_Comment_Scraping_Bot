import googletrans
import json

from googletrans import Translator




# Opening JSON file
with open('Bot/SCRAPED_DATA/CaKqS7zq8Km_COMMENTS.txt', 'r', encoding='utf-8') as fh:
    data = json.load(fh)

# Iterating through the json
# list

translator = Translator()



for i in data:
    try:
        comment =  i["COMMENTS"]
        testing = translator.detect(comment)
        print(i["COMMENTS"], testing)
    except:
        print(error)
    



  

  
# Closing file
fh.close()