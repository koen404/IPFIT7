
# import os
# os.chdir('cases')
# output_path = os.path.abspath('./output')
# print(output_path)

# print('Please enter the username of the SSH user: ')
import logging

def Log(log_location):
    logger = logging.getLogger(__name__)

    # check if there already is a loggin handler, if not create one
    if not len(logger.handlers):
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_location)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger