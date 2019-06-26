import logging
import praw

import responses_constants as const
import reddit_service as reddit

def checkComments(post):
    for comment in post.comments:
        print(comment.body)

def main():
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(levelname)s - %(message)s')
    logging.debug("Starting program")
    
    subreddit = reddit.getSub()
    for post in subreddit.new(limit=const.NEW_POST_LIMIT):
        checkComments(post)

if __name__ == '__main__':
    main()