import paramiko
import sys
import ftplib
import os
import main
import time
from contextlib import closing


class DA_backup:
    def __init__(self):
        self.client = None
        self.Log = main.Main().Log()
        self.main = main.Main()
        self.shell = None
    def back_up(self, host, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=host, port=13370, username=username, password=password)
            rootPass = input('Please enter the root password of the server:')
            print(rootPass)
            # command = "echo \"action=backup&append%5Fto%5Fpath=nothing&database%5Fdata%5Faware=yes&email%5Fdata%5Faware=yes&local%5Fpath=%2Fhome%2Fadmin%2Fadmin%5Fbackups&owner=admin&type=admin&value=multiple&when=now&where=local&who=all\" >> /usr/local/directadmin/data/task.queue"
            command = 'echo \'Hallo test\'>> test1'
            stdin, stdout, stderr = self.client.exec_command('su -c \"' + command + '\"')
            stdin.write(rootPass+'\n')
            stdin.flush()
            print(stdout.readlines())

        except Exception as e:
            print('Connection failed')
            print(e)
    #
    # def sendcommand(self, command):
    #     time.sleep(1)
    #     self.shell.recv(1024)
    #     self.shell.send(command + '\n')
    #     while not self.shell.recv_ready():  # Wait for the server to read and respond
    #         time.sleep(0.1)
    #     time.sleep(0.3)
    #     output = self.shell.recv(1024)  # read in
    #     # print(output)
    #     time.sleep(0.1)

    def download(self,username,password, host):
        with closing(ftplib.FTP()) as ftp:
            try:
                ftp.connect(host,)
                ftp.login(username,password)
                ftp.set_pasv(True)
                ftp.cwd('/backups')
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
                            index_input = True
                        except ValueError:
                            self.Log.error("Wrong Index number")

                    if download_index == 0:
                        continue
                    filename = files[download_index+1].lstrip()
                    print("Downloading File:"+filename)
                    self.Log.info("Downloading File: " + filename)
                    localfile = os.path.join(sys.path[0], 'download', filename)

                    ftp.retrbinary("RETR " + filename, open(localfile, 'wb').write, 8*1024)
                    print(self.main.bereken_hash(localfile))
                    print("Downloading complete")

                ftp.quit()
            except ftplib.error_perm:
                print("error")


