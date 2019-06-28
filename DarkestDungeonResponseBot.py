import logging
import sys
import traceback

import response_bot as bot
import responses_constants as const

if __name__ == '__main__':
    # Output a log or console, depends if FILE_NAME is blank
    if const.LOG_FILE_NAME:
        logging.basicConfig(filename=const.LOG_FILE_NAME, level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s | %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s | %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    logging.info("Starting program")
    
    try:
        bot.begin()
    except KeyboardInterrupt as keyEx:
        logging.info("Stopped program because of keyboard interruption")
    except Exception as ex:
        logging.exception("Unknown exception - " + traceback.format_exc())