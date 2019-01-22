import os
import sys
from datetime import date
import hashlib as hash
import DA_backup
import File_extraction
import csv
import Mail_analysis
import Convert_database
from resources import Log
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
        # this variable will contain the log location
        self.log_location = os.path.join(sys.path[0], 'log', 'Main_log_' + str(date.today()) + '.log')
        # this will map the choices made by the user to the corresponding function
        self.choices_main = {
                "1": self.create_back_up,
                "2": self.download_back_up,
                "3": self.file_extraction,
                "4": self.mail_analysis,
                "5": self.download_logs,
                "6": self.database_analysis,
                "7": self.quit

                }

    # move the log function to a separate file/class
    def Log(self):
        return Log.Log(self.log_location)

    # this function will display the tekst based userinterface
    def display_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
        Menu
        1. Create_back-up
        2. Download_Back-up
        3. File_extraction
        4. Mail_analysis
        5. Log_analysis
        6. Database_analysis
        7. Quit
        """)
    # This function will calculate the hash of a file (can be moved to an separate file/class)
    def bereken_hash(self, file):
        if os.path.isfile(file) and os.access(file, os.R_OK):
            with open(file, 'rb') as file:
                file_buffer = file.read(self.BUFFERSIZE)
                while len(file_buffer) > 0:
                    self.sha256hash.update(file_buffer)
                    file_buffer = file.read(self.BUFFERSIZE)
        else:
            self.Log().info(file + ": File does not exist or is not accessible, will not calculate hash")
        # return the sha256 hash of the file
        return str(self.sha256hash.hexdigest())
    # This function will be executed once the main script is run.
    def run(self):
        # ask for the COE info on startup
        self.coe()
        # Set the download path
        self.download_path = os.path.join(self.casedir, 'download')
        # if the path doesn't exist create it
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        print(os.path.abspath(os.path.join(self.casedir, '..', '..')))
        # set the extract path
        self.extract_path = os.path.join(self.casedir, 'extract')
        # set the log path
        self.server_log_path = os.path.join(self.casedir, 'server_logs')
        if not os.path.exists(self.server_log_path):
            os.makedirs(self.server_log_path)

        self.Log().info("Starting Main_Script")
        self.DA = DA_backup.DA_backup(self.casedir)
        # keep looping through the menu
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices_main.get(choice)
            self.Log().info("User input: %s", choice)

            if action:
                action()
            else:
                # give feedback when a wrong input has been given
                self.Log().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    # This function will call the back-up function from the DA_back-up class.
    def create_back_up(self):
        # check if the host, userneme and password already have been set if not set them
        try:
            if self.sshpassword is not None:
                self.DA.back_up(self.host, self.sshusername, self.sshpassword, self.backupuser)
        except AttributeError:
            self.sshusername = input('Please enter the SSH username: ')
            self.host = input('please enter the DirectAdmin host: ')
            self.sshpassword = getpass.getpass('Please enter the SSH password: ')
            self.backupuser = input('Please enter the user of which the back-up needs to be created, press enter for full back-up:')
            self.DA.back_up(self.host, self.sshusername, self.sshpassword, self.backupuser)
            if self.DA.back_up(self.host, self.sshusername, self.sshpassword, self.backupuser) is None:
                self.sshpassword = None


    # This function will call the download function from the DA_back-up class
    def download_back_up(self):
        try:
            if self.host is not None:

                username = input('Please enter the FTP user: ')
                ftppassword = getpass.getpass('FTP_password: ')
        except AttributeError:

            self.host = input('please enter host: ')
            username = input('Please enter the FTP user: ')
            ftppassword = getpass.getpass('FTP_password: ')

        self.DA.download_backup(username, ftppassword, self.host, self.download_path)

    # This function will call the download log function from the DA_Back-up class
    def download_logs(self):
        # check if the password, host username or logpath have been set if not set them
        try:
            if self.sshpassword is not None:
                self.DA.download_log(self.sshusername, self.sshpassword, self.host, self.server_log_path)
        except AttributeError as e:
            self.sshusername = input('Please enter the SSH username')
            self.host = input('please enter the DirectAdmin host: ')
            self.sshpassword = getpass.getpass('Please enter the SSH password: ')
            self.DA.download_log(self.sshusername, self.sshpassword, self.host, self.server_log_path)

    # this function will start the extraction class
    def file_extraction(self):
        # should change this so it's less prone to user error
        print(self.extract_path)
        print(self.download_path)
        File_extraction.FileExtraction(self.casedir).extract(self.extract_path, self.download_path)

    # This function will create the COE file. If it already exists it will use the existing file.
    def coe(self):
        self.examiner = input('Please enter your name: ')
        self.casenumber = input('Please enter the casenumber: ')
        self.casename = input('please enter a case name (press enter if none): ')

        self.casedir = os.path.join(self.case_path, self.casenumber + '_' + self.casename)
        if not os.path.exists(self.casedir):
            self.Log().info('Create casedir: ' + self.casedir)
            os.makedirs(self.casedir)

        self.coe_output_file = os.path.join(self.casedir, 'coe.csv')
        if not os.path.exists(self.coe_output_file):
            with open(self.coe_output_file, 'a') as file:
                filewriter = csv.writer(file, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['Examiner:', self.examiner])
                filewriter.writerow(['Case number:', self.casenumber])
                filewriter.writerow(['Case Name:', self.casename])
                filewriter.writerow([])
                filewriter.writerow(['When', 'What', 'Hash'])
        else:
            i = 0
            with open(self.coe_output_file, 'r') as file:
                readCSV = csv.reader(file, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in readCSV:
                    if i == 0:
                        temp_name = row[1]
                        print(temp_name)

                    i += 1
            temp_name = str(temp_name).upper()
            if self.examiner.upper() == temp_name:
                self.Log().info('COE file already exist')
            else:
                with open(self.coe_output_file, 'a') as file:
                    filewriter = csv.writer(file, delimiter=',',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    # filewriter.writerow()
                    filewriter.writerow(['New Examiner', self.examiner])

    # This function will run the mail analysis class
    def mail_analysis(self):
        print('mail analysis')
        Mail_analysis.Mail_analysis(self.extract_path).load_maildir()

    # This function will run the database restore and analysis function from the restore_database class
    def database_analysis(self):
        Convert_database.database_analysis(self.extract_path, self.casedir).select_database()

    # This function will stop the program from running
    def quit(self):
        self.Log().info("Exiting script")
        sys.exit(0)

# This if statement will cause the run function to keep running
if __name__ == "__main__":
    Main().run()
