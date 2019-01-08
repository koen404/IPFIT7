import paramiko
import sys
import ftplib
import os
import main
import csv
from contextlib import closing
from time import gmtime, strftime
import Write_to_coe
from scp import SCPClient
class DA_backup:
    def __init__(self):
        self.client = None
        self.Log = main.Main().Log()
        self.main = main.Main()
        self.shell = None

    def back_up(self, host, username, password,coe_output_file, backupuser = None ):
        self.coe_output_file = coe_output_file
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            message = 'Connecting to:' + host
            Write_to_coe.write_to_coe(self.coe_output_file, message)
            self.client.connect(hostname=host, port=13370, username=username, password=password)
            # TODO: move all input to main class
            rootPass = input('Please enter the root password of the server:')
            print(backupuser)
            if backupuser!= '':
                print('back-up user not empty')
                message = 'Creating back-up for user: ' + backupuser
                Write_to_coe.write_to_coe(self.coe_output_file, message)
                backupcommand = 'echo \'action=backup&append%5Fto%5Fpath=nothing&database%5Fdata%5Faware=yes&email%5Fdata%5Faware=yes&local%5Fpath=%2Fhome%2Fadmin%2Fadmin%5Fbackups&owner=admin&select%30='+ backupuser +'&type=admin&value=multiple&when=now&where=local\' >> /usr/local/directadmin/data/task.queue'
            else:
                message = 'Creating back-up for all users'
                Write_to_coe.write_to_coe(self.coe_output_file, message)
                backupcommand = 'echo \'action=backup&append%5Fto%5Fpath=nothing&database%5Fdata%5Faware=yes&email%5Fdata%5Faware=yes&local%5Fpath=%2Fhome%2Fadmin%2Fadmin%5Fbackups&owner=admin&type=admin&value=multiple&when=now&where=local&who=all\'>> /usr/local/directadmin/data/task.queue'
            stdin, stdout, stderr = self.client.exec_command('su -c \"' + backupcommand + '\"')
            stdin.write(rootPass+'\n')
            stdin.flush()
            print(stdout.readlines())
            checkcommand = '/usr/local/directadmin/dataskq d200'
            stdin, stdout, stderr = self.client.exec_command('su -c \"' + checkcommand + '\"')
            stdin.write(rootPass+'\n')
            stdin.flush()
            print(stdout.readlines())
        except Exception as e:
            print('Connection failed')
            print(e)

    def download_backup(self, username, password, host, download_path, coe_output_file):
        # TODO: calculate hash of downloaded file and write it to a file
        with closing(ftplib.FTP()) as ftp:
            try:
                message = 'Connecting to: ' + host
                Write_to_coe.write_to_coe(self.coe_output_file, message)
                ftp.connect(host,)
                ftp.login(username, password)
                ftp.set_pasv(True)
                ftp.cwd('/admin_backups')
                files = ftp.nlst()
                download_index = None

                while download_index != 0:
                    i = 0
                    for file in files[2:]:
                        i += 1
                        print(str(i) + " " + file)
                    print('0 Exit')
                    index_input = False
                    while index_input is False:
                        download_index = input("What file do you want to download?")
                        try:
                            val = int(download_index)
                            download_index = val
                            if val > len(files):
                                raise ValueError
                            index_input = True
                        except ValueError:
                            self.Log.error("Wrong Index number")

                    if download_index == 0:
                        continue
                    filename = files[download_index+1].lstrip()
                    print("Downloading File:" + filename)
                    message = 'Downloading File: ' + filename
                    Write_to_coe.write_to_coe(self.coe_output_file, message)
                    self.Log.info("Downloading File: " + filename)
                    localfile = os.path.join(download_path, filename)

                    ftp.retrbinary("RETR " + filename, open(localfile, 'wb').write, 8*1024)
                    message = 'Calculating hash of file' + filename

                    hash = self.main.bereken_hash(localfile)
                    Write_to_coe.write_to_coe(self.coe_output_file, message, hash)

                    print("Downloading complete")

                ftp.quit()
            except ftplib.error_perm as e:
                print(e)
                print("error")

    # TODO: download the access logs and the phpadmin log: /var/www/html/phpMyAdmin/log/
    def download_log(self, username, password, host):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=host, port=13370, username=username, password=password)
            rootPass = input('Please enter the root password of the server:')
            stdin, stdout, stderr = self.client.exec_command('su -c \" cat /var/www/html/phpMyAdmin/log/auth.log-20190107 \"')
            stdin.write(rootPass+'\n')
            for line in stdout.readlines():
                print(line)

        except Exception as e:
            print(e)

