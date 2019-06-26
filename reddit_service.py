import praw

import responses_constants as const

def getReddit():
    return praw.Reddit(client_id=const.APP_ID, client_secret=const.APP_SECRET, user_agent=const.APP_AGENT)

def getSub():
    return getReddit().subreddit(const.SUBREDDIT)