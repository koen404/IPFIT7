import paramiko
import sys
import ftplib
import logger
from contextlib import closing
class DA_backup:
    def __init__(self):
        self.client = None
        self.Log = logger.logger().log()

    def connect( self, host, username, password):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(host, username=username,password=password)

    def back_up(self):
        command = "echo \"action=backup&append%5Fto%5Fpath=nothing&database%5Fdata%5Faware=yes&email%5Fdata%5Faware=yes&local%5Fpath=%2Fhome%2Fadmin%2Fadmin%5Fbackups&owner=admin&type=admin&value=multiple&when=now&where=local&who=all\" >> /usr/local/directadmin/data/task.queue"
        (stdin, stdout, stderr) = self.client.exec_command(command)
        for line in stdout.readlines():
            print(line)
        self.client.close()

    def download(self,username,password, host):
        with closing(ftplib.FTP()) as ftp:
            try:
                ftp.connect(host,)
                ftp.login(username,password)
                ftp.set_pasv(True)
                files = ftp.nlst()
                ftp.cwd('/backups')
                files = ftp.nlst()
                i = 0
                for file in files[2:]:

                    i += 1
                    print(str(i) +" " + file)
                download_index= int(input("What file do you want to download?"))
                filename= files[download_index+1].lstrip()
                print("Downloading File:"+filename)
                self.Log.info("Downloading File: " + filename)
                localfile = filename

                ftp.retrbinary("RETR "+ filename,open(localfile,'wb').write, 8*1024)
                print("Downloading complete")

                ftp.quit()


            except ftplib.error_perm:
                print("error")



