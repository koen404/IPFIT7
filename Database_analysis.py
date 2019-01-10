import pymysql
import os
class database_analysis:
    def __init__(self):
        self.database_name = None

    def import_database(self, database_name):
        host = '127.0.0.1'
        user = 'root'
        output_database = os.path.basename(database_name)
        output_database = output_database.replace('.sql', '')
        passwd= input('please enter the password of the root user')
        self.con = pymysql.connect(host,user,passwd)
        mycursor =self.con.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS" + output_database)
        with mycursor as cursor:
            for line in open(database_name, 'r'):
                if line.strip():
                    cursor.execute(line)

    def run_mysqlWB(self):
        os.system('mysql-workbench')
