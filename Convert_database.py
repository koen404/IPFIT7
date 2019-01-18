import os
import main
from resources import list_dir
import subprocess


class database_analysis:
    def __init__(self, extract_path, casedir):
        self.casedir = casedir
        self.database_name = None
        self.Log = main.Main().Log()
        self.extract_path = extract_path

    # function to let the user select the database that needs to be converted and loaded in the SQLite browser
    def select_database(self):

        input_question = 'Select the backup of which you want to restore the database'

        first = list_dir.listdir(self.extract_path, input_question, files=True)

        while not first.endswith('.sql'):
            first = list_dir.listdir(first, input_question, files=True)
        if first.endswith('.sql'):
            self.convert_database(first)

    # this function will convert the specified database dump to SQLite format
    def convert_database(self, database_name):

        output_database = os.path.basename(database_name)

        temp_path = os.path.abspath(self.casedir)

        outpath = os.path.join(temp_path, "/output/database")
        os.chdir(os.path.abspath(os.path.join(temp_path, '../', '../')))
        print(outpath)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
            self.Log.info('Creating directory : ' + outpath)

        output_database = os.path.join(outpath, output_database.replace('.sql', '.db'))
        subprocess.call("./resources/mysql2sqlite", database_name, '|', output_database)
        self.run_sqliteBrowser(output_database)
        # passwd= input('please enter the password of the IPFIT7 user')
        # try:
        #     self.con = pymysql.connect(host, user, passwd)
        # except (pymysql.OperationalError) as e:
        #     self.Log.error('An error occurred while connecting to the database:' + e)
        #
        # self.Log.info('Connecting to Local database')
        # try:
        #     mycursor =self.con.cursor()
        #
        # except (pymysql.MySQLError, pymysql.Warning) as e:
        #     print(e)
        #     self.Log.error('MySQL connection error: ' + e)
        #     return None
        #
        # mycursor.execute("CREATE DATABASE IF NOT EXISTS " + output_database)
        # subprocess.call(["mysql", "-u", user, "-p",passwd, output_database , '<', database_name])

    # this function will open the specified SQLite database in the SQLite browser
    def run_sqliteBrowser(self, database):
        subprocess.call(['sqlitebrowser', '-R', database])

