import logging
import os
class logger:
    def __init__(self):
        temp_path = os.path.join(sys.path[0], "log")
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        self.log_location = os.path.join(sys.path[0], 'log', 'Main_log_' + str(date.today()) + '.log')

    def log(self):

        logger = logging.getLogger(__name__)

        # check if there already is a loggin handler, if not create one
        if not len(logger.handlers):
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(self.log_location)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger