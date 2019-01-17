import pymysql
import os
import main
from resources import list_dir
import subprocess

class database_analysis:
    def __init__(self, extract_path):
        self.database_name = None
        self.Log = main.Main().Log()
        self.extract_path = extract_path

    def select_database(self):
        input_question = 'Select the backup of which you want to restore the database'

        first = list_dir.listdir(self.extract_path, input_question, files=True)

        while not first.endswith('.sql'):
            first = list_dir.listdir(first, input_question, files=True)
        if first.endswith('.sql'):
            self.convert_database(first)

    def convert_database(self, database_name):

        output_database = os.path.basename(database_name)

        temp_path = os.path.abspath(self.extract_path)
        outpath = os.path.join(temp_path, "../output/database")
        print(outpath)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
            self.Log.info('Creating directory : ' + outpath)

        output_database = os.path.join(outpath, output_database.replace('.sql', '.db'))
        subprocess.call("./resources/mysql2sqlite", database_name, '|', output_database)
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

    def run_sqliteBrowser(self):
        os.system('')
