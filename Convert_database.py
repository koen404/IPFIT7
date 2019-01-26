import os
import main
from resources import list_dir
import subprocess
import tkinter
from resources import Write_to_coe
from tkinter.filedialog import askopenfilename


class database_analysis:
    def __init__(self, extract_path, casedir):
        self.casedir = casedir
        self.database_name = None
        self.Log = main.Main().Log()
        self.extract_path = extract_path
        self.coe_output_file = Write_to_coe.get_coe_output(casedir)


    # function to let the user select the database that needs to be converted and loaded in the SQLite browser
    def select_database(self):
        root = tkinter.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()
        database_location = os.path.join(self.casedir, 'extract')
        first = askopenfilename(initialdir=database_location, filetypes=[('Sql files', '*.sql')], parent = root)
        print(first)

        if first is None or not os.path.exists(first):
            print('Selection cancelled by user')
            self.Log.warning('Selection of database cancelled by user')
        if first.endswith('.sql'):
            self.Log.info('Selected database:' + first)
            self.convert_database(first)
        else:
            print('Selection of database failed.')
        root.destroy()

    # this function will convert the specified database dump to SQLite format
    def convert_database(self, database_name):

        Write_to_coe.write_to_coe(self.coe_output_file, 'Converting database to sqlite:' + database_name)
        output_database = os.path.basename(database_name)

        temp_path = os.path.abspath(self.casedir)

        outpath = os.path.join(temp_path, "output", "database")
        Write_to_coe.write_to_coe(self.coe_output_file, 'Writing sqlite database to:' + outpath)
        os.chdir(os.path.abspath(os.path.join(temp_path, '..', '..', 'resources')))
        if not os.path.exists(outpath):
            os.makedirs(outpath)
            self.Log.info('Creating directory : ' + outpath)

        temp = os.path.join(outpath, output_database.replace('.sql', '.db')).replace(' ', '\\ ')

        os.system("./mysql2sqlite " + output_database.replace(' ', '\\ ') + ' | sqlite3' + temp)
        self.run_sqliteBrowser(output_database)


    # this function will open the specified SQLite database in the SQLite browser
    def run_sqliteBrowser(self, database):
        subprocess.call(['sqlitebrowser', '-R', database])

