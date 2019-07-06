# Reddit API information - Can be found at https://www.reddit.com/prefs/apps
APP_ID = ''
APP_SECRET = ''
APP_AGENT = 'Darkest Dungeon Response Bot v0.1.1 - /u/JoshLmao'

# Username and password of the Reddit bot
BOT_NAME = 'dd_responses_bot'
BOT_PASSWORD = ''
# Message should contain 2 strings to add at runtime in this order: Description, Audio Url
BOT_MESSAGE = '''[%s](%s)\n\n------\n\n[^(Source)](https://github.com/JoshLmao/DarkestDungeonResponseBot) ^(|) [^(Issues)](https://github.com/JoshLmao/DarkestDungeonResponseBot/Issues) ^(|) [^(Support ☕)](https://ko-fi.com/joshlmao)'''

# Relevant file name of the JSON database file (same folder as .py)
DATABASE_FILE_NAME = "voice_lines.json"
# Key value of database, value holds array of data
DATABASE_MASTER_KEY = "voice-lines"

# Subreddit to check over
SUBREDDIT = 'darkestdungeon'
# Amount of new & hot posts to check comments on
NEW_POST_LIMIT = 15
HOT_POST_LIMIT = 30

# How many minutes should the bot sleep for before scanning for comments again
SLEEP_MINUTES = 1

# Debug/Log information - Leave FILE_NAME blank for outputting to console instead of file
LOG_FILE_NAME = ''
# Should the bot create a post on it's profile page when it's live, will remove if crash or stopped
DEBUG_PROFILE_POST = True