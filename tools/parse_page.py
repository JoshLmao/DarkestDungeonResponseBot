# Parses Narrator voice lines (https://darkestdungeon.gamepedia.com/Narrator) and creates json database for use

from bs4 import BeautifulSoup as beautifulSoup
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
import json

def stripString(string):
    return string.replace("\n", "").replace("“", "").replace("„", "")

def main():
    url = "https://darkestdungeon.gamepedia.com/Narrator"
    soup = beautifulSoup(urlopen(url))
    # Get all <table> and <audio> tags
    allElements = soup.find_all([ "table", "audio" ])
    responseDict = { 
        'responses': [ ]
    }

    length = len(allElements)
    for i in range(0, length):
        element = allElements[i]
        # Only parse if current element is a <table> tag, which means <audio> follows
        if element.name == "table" and i < length - 3:
            text = stripString(element.text)
            firstAudio = ""
            altAudio = ""
            # Parse first audio source
            if allElements[i + 1].name == 'audio':
                audio = allElements[i + 1]
                firstAudio = audio.contents[0]['src']
            # Check for alt audio and parse that
            if firstAudio != "" and allElements[i + 2].name == 'audio':
                audio = allElements[i + 2]
                altAudio = audio.contents[0]['src']
            # If no url parsed, skip
            if firstAudio == "" and altAudio == "":
                print("Ignoring description of index " + str(i))
                continue

            responseDict['responses'].append({
                "text": text,
                "audio": firstAudio,
                "altAudio": altAudio,
            })

    # Dump JSON to file, pretty printed
    with open('responses.json', 'w') as f:
        json.dump(responseDict, f, ensure_ascii=False, indent=4, sort_keys=True)
    
if __name__ == '__main__':
    main()