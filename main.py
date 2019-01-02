import os
import sys
from datetime import date
import logging
import datetime
import hashlib as hash
import DA_backup
import File_extraction
import csv
import getpass


class Main:
    BUFFERSIZE = 65536
    download_path = os.path.join(sys.path[0], "download")

    def __init__(self):
        log_path = os.path.join(sys.path[0], "log")

        self.sha256hash = hash.sha256()
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        self.log_location = os.path.join(sys.path[0], 'log', 'Main_log_' + str(date.today()) + '.log')
        self.choices_main = {
                "1": self.create_back_up,
                "2": self.download_back_up,
                "3": self.file_extraction,
                "4": self.quit

                }

    def Log(self):

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

    def display_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
        Menu
        1. Create_back-up
        2. Download_Back-up
        3. File_extraction
        4. Quit
        """)

    def bereken_hash(self, file):
        if os.path.isfile(file) and os.access(file, os.R_OK):
            with open(file, 'rb') as file:
                file_buffer = file.read(self.BUFFERSIZE)
                while len(file_buffer) > 0:
                    self.sha256hash.update(file_buffer)
                    file_buffer = file.read(self.BUFFERSIZE)
        else:
            self.Log().info(file + ": File does not exist or is not accessible, will not calculate hash")

        return str(self.sha256hash.hexdigest())

    def run(self):

        self.Log().info("Starting Main_Script")

        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices_main.get(choice)
            self.Log().info("User input: %s", choice)
            self.DA = DA_backup.DA_backup()
            if action:
                action()
            else:
                self.Log().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    def create_back_up(self):
        username = 'koen'
        sshpassword = input('Please enter the SSH password: ')
        host = input('please enter host')
        user = input('please enter the user which you want to creat the back-up from')
        self.DA.back_up(host, username, sshpassword)

    def download_back_up(self):
        username = 'admin'
        ftppassword = input('FTP_password:')
        host = input('please enter host')
        self.DA.download(username, ftppassword, host)

    def file_extraction(self):
        filename = input("please enter the tar.gz file you want to extract (press * for all):")
        File_extraction.FileExtraction().extract(filename)

    def quit(self):
        self.Log().info("Exiting script")
        sys.exit(0)


if __name__ == "__main__":
    Main().run()
