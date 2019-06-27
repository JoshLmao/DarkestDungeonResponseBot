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

# Searches the database for a match to the phrase
def checkDatabase(respDatabase, phrase):
    responses = respDatabase[const.DATABASE_MASTER_KEY]
    for r in responses:
        responseLine = cleanString(r['text'])
        # Criteria: Match completely...
        if phrase == responseLine:
            return r
        # OR users comment has part of full response line
        # Too many false positives, removed for now 
        # if (phrase in responseLine):
        #     return r

# Check to see if the bot already replied to the comment
def hasReplied(repliesArray):
    for reply in repliesArray:
        if reply.author != None and reply.author.name == const.BOT_NAME:
            return True

# Checks a post comments for a match
def checkComments(respDatabase, post):
    for comment in post.comments:
        # Check if already posted a response
        if hasReplied(comment.replies):
            commentFiveWords = comment.body.split()[:5]
            logging.info("Already to replied to comment '%s' by '%s' on post '%s'" % (" ".join(commentFiveWords), comment.author.name, post.title))
            continue
            
        commentClean = cleanString(comment.body)
        dbMatch = checkDatabase(respDatabase, commentClean)
        if dbMatch != None:
            reddit.reply(comment, dbMatch)

# Scans /new/ and then /hot/ for matching comments
def scan(respDatabase):
    subreddit = reddit.getSub(const.SUBREDDIT)
    for post in subreddit.new(limit=const.NEW_POST_LIMIT):
        checkComments(respDatabase, post)

    for post in subreddit.hot(limit=const.HOT_POST_LIMIT):
        checkComments(respDatabase, post)

# Reads the db file name and returns the db
def loadDatabase():
    with open(const.DATABASE_FILE_NAME) as jsonFile:
        return json.load(jsonFile)

def main():
    # Output a log if FILE_NAME isn't blank
    if const.LOG_FILE_NAME != "":
        logging.basicConfig(filename=const.LOG_FILE_NAME, level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s | %(message)s', datefmt='%d-%m-%Y %H:%M:%S',)
    logging.info("Starting program")

    # Load database into memory
    responseDatabase = loadDatabase()
    while True:
        logging.info("Beginning to scan comments...")
        scan(responseDatabase)

        # Complete scan and sleep for X minutes
        logging.info("Completed scanning comments. Sleeping for %d minutes" % const.SLEEP_MINUTES)
        time.sleep(const.SLEEP_MINUTES * 60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as keyEx:
        logging.info("Stopped program because of keyboard interruption")
    except Exception as e:
        logging.error("Unknown exception - " + str(e))