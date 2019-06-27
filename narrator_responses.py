import logging
import praw
import time
import json
import re
import string

import responses_constants as const
import reddit_service as reddit

# Cleans a string to remove any unwanted punctuation, emojis and/or line endings and converts to lower case, useful for comparing
def cleanString(phraseStr, toLower=True):
    # Remove punc
    phraseStr = phraseStr.translate(str.maketrans('', '', string.punctuation))
    # Remove Emojis 😭
    phraseStr = phraseStr.encode('ascii', 'ignore').decode('ascii')
    # Remove any unwanted white space at beginning or end
    if phraseStr[0] == ' ':
        phraseStr = phraseStr.lstrip()
    if phraseStr[len(phraseStr) - 1] == ' ':
        phraseStr = phraseStr.rstrip()
    if toLower:
        return phraseStr.lower()
    else:
        return phraseStr

def checkDatabase(respDatabase, phrase):
    responses = respDatabase['responses']
    for r in responses:
        responseLine = cleanString(r['text'])
        # Criteria: Match completely...
        if phrase == responseLine:
            return r
        # OR users comment has part of full response line
        # if (phrase in responseLine):
        #     return r

def hasReplied(repliesArray):
    for reply in repliesArray:
        if reply.author != None and reply.author.name == const.BOT_NAME:
            return True

def checkComments(respDatabase, post):
    for comment in post.comments:
        # Check if already posted a response
        if hasReplied(comment.replies):
            logging.debug("Already to replied to comment with id %s" % (comment.id))
            continue
            
        commentClean = cleanString(comment.body)
        dbMatch = checkDatabase(respDatabase, commentClean)
        if dbMatch != None:
            reddit.reply(comment, dbMatch)

def scan(respDatabase):
    subreddit = reddit.getSub(const.SUBREDDIT)
    for post in subreddit.new(limit=const.NEW_POST_LIMIT):
        checkComments(respDatabase, post)

    for post in subreddit.hot(limit=const.HOT_POST_LIMIT):
        checkComments(respDatabase, post)

def loadDatabase():
    with open('responses.json') as jsonFile:
        return json.load(jsonFile)

def main():
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(levelname)s - %(message)s')
    logging.debug("Starting program")
    
    responseDatabase = loadDatabase()

    while True:
        logging.debug("Beginning to scan comments...")
        scan(responseDatabase)

        # Complete scan and sleep for X seconds
        sleepSeconds = 30
        logging.debug("Completed scanning comments. Sleeping for "+str(sleepSeconds)+" seconds")
        time.sleep(sleepSeconds)

if __name__ == '__main__':
    main()