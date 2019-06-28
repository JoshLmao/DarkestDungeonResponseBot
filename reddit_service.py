import praw
import logging

import responses_constants as const

def getRedditActive():
    return praw.Reddit(client_id=const.APP_ID, client_secret=const.APP_SECRET, user_agent=const.APP_AGENT, username=const.BOT_NAME, password=const.BOT_PASSWORD)

def getReddit():
    return praw.Reddit(client_id=const.APP_ID, client_secret=const.APP_SECRET, user_agent=const.APP_AGENT)

def getSub(subredditName):
    return getRedditActive().subreddit(subredditName)

def reply(comment, dbValue):
    try:
        comment.reply(const.BOT_MESSAGE % (dbValue['text'], dbValue['audio']))
        return True
    except praw.exceptions.APIException as e:
        logging.error("Couldn't reply to comment - " + e.message)
        return False