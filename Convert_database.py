import os
import main
from resources import list_dir
import subprocess
import tkinter
from tkinter.filedialog import askopenfilename


class database_analysis:
    def __init__(self, extract_path, casedir):
        self.casedir = casedir
        self.database_name = None
        self.Log = main.Main().Log()
        self.extract_path = extract_path

    # function to let the user select the database that needs to be converted and loaded in the SQLite browser
    def select_database(self):
        root = tkinter.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()


        first = askopenfilename(initialdir=self.extract_path, filetypes=[('Sql files', '*.sql')], parent = root)
        print(first)
        if first is None:
            print('Blaat')
        if first.endswith('.sql'):
            self.convert_database(first)
        else:
            print('returning to home')
        root.destroy()

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
        subprocess.check_call(["./resources/mysql2sqlite", database_name, '|', output_database], shell=True)
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

