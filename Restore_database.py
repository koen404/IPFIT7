import pymysql
import os
import main
from resources import list_dir

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
            self.import_database(first)

    def import_database(self, database_name):
        host = '127.0.0.1'
        user = 'IPFIT7'
        output_database = os.path.basename(database_name)
        output_database = output_database.replace('.sql', '')
        passwd= input('please enter the password of the IPFIT7 user')
        self.con = pymysql.connect(host, user, passwd)
        self.Log.info('Connecting to Local database')
        try:
            mycursor =self.con.cursor()
        except (pymysql.MySQLError, pymysql.Warning) as e:
            print(e)
            self.Log.error('MySQL connection error: ' + e)
            return None

        mycursor.execute("CREATE DATABASE IF NOT EXISTS" + output_database)
        with mycursor as cursor:
            for line in open(database_name, 'r'):
                if line.strip():
                    cursor.execute(line)
                    self.Log.info('Executing Database query:' + line)


    def run_mysqlWB(self):
        os.system('mysql-workbench')
