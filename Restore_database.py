import pymysql
import os
import main


class database_analysis:
    def __init__(self):
        self.database_name = None
        self.Log =  main.Main.Log()

    def import_database(self, database_name):
        host = '127.0.0.1'
        user = 'IPFIT7'
        output_database = os.path.basename(database_name)
        output_database = output_database.replace('.sql', '')
        passwd= input('please enter the password of the root user')
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
