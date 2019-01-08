import os
import sys
from datetime import date
import logging
import datetime
import hashlib as hash
import DA_backup
import File_extraction
import csv
import Mail_analysis
import getpass


class Main:
    BUFFERSIZE = 65536
    extract_path = None
    def __init__(self):
        log_path = os.path.join(sys.path[0], "log")
        self.sha256hash = hash.sha256()
        self.examiner = None
        self.casenumber = None
        self.casename = None
        self.casedir = None
        self.coepath = os.path.join(sys.path[0], '.coe')
        self.case_path = os.path.join(sys.path[0], 'cases')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if not os.path.exists(self.case_path):
            os.makedirs(self.case_path)

        self.log_location = os.path.join(sys.path[0], 'log', 'Main_log_' + str(date.today()) + '.log')
        self.choices_main = {
                "1": self.create_back_up,
                "2": self.download_back_up,
                "3": self.file_extraction,
                "4": self.mail_analysis,
                "5": self.download_logs,
                "6": self.quit

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
        4. Mail_analysis
        5. Download_logs
        6. Quit
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

        self.coe()

        self.download_path = os.path.join(self.casedir, 'download')
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        self.extract_path = os.path.join(self.casedir, 'extract')
        self.server_log_path = os.path.join(self.casedir, 'server_logs')
        if not os.path.exists(self.server_log_path):
            os.makedirs(self.server_log_path)

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
        try:
            if self.sshpassword is not None:
                self.DA.back_up(self.host, self.sshusername, self.sshpassword, self.coe_output_file, self.backupuser)
        except AttributeError as e:
            self.sshusername = 'koen'
            self.host = input('please enter the DirectAdmin host: ')
            self.sshpassword = input('Please enter the SSH password: ')
            self.backupuser = input('Please enter the user of which you want to create the back-up from:')
            self.DA.back_up(self.host, self.sshusername, self.sshpassword,  self.coe_output_file, self.backupuser)

    def download_back_up(self):
        username = 'admin'
        ftppassword = input('FTP_password:')
        host = input('please enter host')
        self.DA.download_backup(username, ftppassword, host, self.download_path, self.coe_output_file)

    def download_logs(self):
        try:
            if self.sshpassword is not None:
                self.DA.download_log(self.sshusername, self.sshpassword, self.host, self.server_log_path)
        except AttributeError as e:
            self.sshusername = 'koen'
            self.host = input('please enter the DirectAdmin host: ')
            self.sshpassword = input('Please enter the SSH password: ')
            self.DA.download_log(self.sshusername, self.sshpassword, self.host, self.server_log_path)

    def file_extraction(self):
        filename = input("please enter the tar.gz file you want to extract (press * for all):")
        print(self.extract_path)
        print(self.download_path)
        File_extraction.FileExtraction().extract(filename, self.extract_path, self.download_path, self.coe_output_file)

    def coe(self):
        self.examiner = input('Please enter your name:')
        self.casenumber = input('Please enter the casenumber:')
        self.casename = input('please enter a case name (press enter if none):')
        self.casedir = os.path.join(self.case_path, self.casenumber + '_' + self.casename)
        if not os.path.exists(self.casedir):
            os.makedirs(self.casedir)
        self.coe_output_file = os.path.join(self.casedir, 'coe.csv')
        if not os.path.exists(self.coe_output_file):
            with open(self.coe_output_file, 'w') as file:
                filewriter = csv.writer(file, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['Examiner', self.examiner])
                filewriter.writerow(['Case number', self.casenumber])
                filewriter.writerow(['Case Name', self.casename])
                filewriter.writerow(['When', 'What', 'Hash'])
        else:
            print('Using existing coe file: ' + self.coe_output_file)

    # TODO: create a maildir analysis script
    def mail_analysis(self):
        print('mail analysis')
        Mail_analysis.Mail_analysis().load_maildir(self.extract_path)


    #TODO: create a script to analyse .sql files
    def database_analysis(self):
        print('Database analysis')

    def quit(self):
        self.Log().info("Exiting script")
        sys.exit(0)


if __name__ == "__main__":
    Main().run()
