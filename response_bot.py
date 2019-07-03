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

def contains(list, checkItem):
    for item in list:
        if item == checkItem:
            return True

# Check to see if the bot already replied to the comment
def hasReplied(repliesArray):
    for reply in repliesArray:
        if reply.author != None and reply.author.name == const.BOT_NAME:
            return True

# Checks a post comments for a match
def checkComments(respDatabase, post, repliedIds):
    for comment in post.comments:
        # Check if already posted a response
        # Shorten comment to 5 words for display purposes
        commentShort = " ".join(comment.body.split()[:5])
        commentAuthor = "Unknown"
        if comment.author:
            commentAuthor = comment.author.name
        if hasReplied(comment.replies) or contains(repliedIds, comment.id):
            logging.debug("Already replied to comment '%s' by '%s' on post '%s'" % (commentShort, commentAuthor, post.title))
            continue
            
        commentClean = cleanString(comment.body)
        dbMatch = checkDatabase(respDatabase, commentClean)
        if dbMatch != None:
            result = reddit.reply(comment, dbMatch)
            repliedIds.append(comment.id)
            if result:
                logging.info("Replying to comment '%s' - '%s'" % (commentAuthor, commentShort))

# Scans /new/ and then /hot/ for matching comments
def scan(respDatabase):
    # Store array of replied to comment id's this scan to not reply more than once
    repliedCommentIds = [ ]

    subreddit = reddit.getSub(const.SUBREDDIT)
    for post in subreddit.new(limit=const.NEW_POST_LIMIT):
        checkComments(respDatabase, post, repliedCommentIds)

    for post in subreddit.hot(limit=const.HOT_POST_LIMIT):
        checkComments(respDatabase, post, repliedCommentIds)

# Reads the db file name and returns the db
def loadDatabase():
    with open(const.DATABASE_FILE_NAME) as jsonFile:
        return json.load(jsonFile)

def begin():
    if not const.APP_ID or not const.APP_SECRET:
        logging.error("Unable to start bot. APP_ID or APP_SECRET is requires")
        return

    # Post to profile with info
    profileSub = reddit.getRedditActive().subreddit("u_%s" % const.BOT_NAME)
    debugPost = profileSub.submit("Live on subreddit /r/%s" % const.SUBREDDIT, "Live on '%s' \n\nHot post count: '%s'\n\nNew post count: '%s'" % (const.SUBREDDIT, const.HOT_POST_LIMIT, const.NEW_POST_LIMIT))
    debugPost.mod.sticky()
    logging.debug("Created and stickied debug post on self subreddit")

    # Load database into memory
    responseDatabase = loadDatabase()
    while True:
        logging.info("Beginning to scan comments...")
        scan(responseDatabase)

        # Complete scan and sleep for X minutes
        logging.info("Completed scanning comments. Sleeping for %d minute(s)" % const.SLEEP_MINUTES)
        time.sleep(const.SLEEP_MINUTES * 60)

def dispose():
    profileSub = reddit.getRedditActive().subreddit("u_%s" % const.BOT_NAME)
    posts = profileSub.new(limit=3)
    for post in posts:
        if "Live on subreddit" in post.title:
            logging.debug("Removing info post on own subreddit")
            post.delete()