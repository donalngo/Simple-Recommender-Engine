from . import init
from .HardRules import HardMatching
from .SoftRules import SoftMatching
from time import mktime
# from .event_log import insert_row, sql_connection
from datetime import datetime
import os
import logging
import sys


def ToRecommendationEngine(hard_requirements, soft_requirements, *kwarg):
    f = open("Recommendation/Logs/IO.log", "a+")
    current_time = datetime.now()
    date_time = current_time.strftime("%m/%d/%Y, %H:%M:%S")
    f.write(f"{date_time}   INPUT: HARD: {hard_requirements}, SOFT: {soft_requirements}\n")

    logging.basicConfig(filename='Recommendation/Logs/errorlog.log')
    logger = logging.getLogger('mylogger')

    def my_handler(type, value, tb):
        current_time = datetime.now()
        date_time = current_time.strftime("%m/%d/%Y, %H:%M:%S")
        logger.exception(f"{date_time} Uncaught exception: {format(str(type))}, {format(str(value))}")

    sys.excepthook = my_handler
    init.number_of_match = 3
    init.path = os.getcwd()

    eligible_matches = HardMatching(hard_requirements)
    sorted_results = SoftMatching(eligible_matches, soft_requirements)

    print(sorted_results)
    current_time = datetime.now()
    date_time = current_time.strftime("%m/%d/%Y, %H:%M:%S")
    f.write(f"{date_time}   ALL RESULTS: {sorted_results}\n")
    sorted_results = sorted_results[:3]
    best_results = sorted_results
    current_time = datetime.now()
    date_time = current_time.strftime("%m/%d/%Y, %H:%M:%S")
    f.write(f"{date_time}   OUT: {best_results}\n")

    return best_results
