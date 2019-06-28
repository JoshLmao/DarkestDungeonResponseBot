import logging

import response_bot as bot
import responses_constants as const

if __name__ == '__main__':
    # Output a log if FILE_NAME isn't blank
    if const.LOG_FILE_NAME != "":
        logging.basicConfig(filename=const.LOG_FILE_NAME, level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s | %(message)s', datefmt='%d-%m-%Y %H:%M:%S',)
    logging.info("Starting program")

    try:
        bot.begin()
    except KeyboardInterrupt as keyEx:
        logging.info("Stopped program because of keyboard interruption")
    except Exception as e:
        logging.error("Unknown exception - " + str(e))