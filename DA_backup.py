import paramiko
import ftplib
import os
import main
from contextlib import closing
import Write_to_coe
import Log_analysis
import uniquify
class DA_backup:
    def __init__(self, casedir):
        self.casedir = casedir
        self.client = None
        self.Log = main.Main().Log()
        self.main = main.Main()
        self.shell = None
        self.coe_output_file = Write_to_coe.get_coe_output(self.casedir)
    # function to create an back-up on the DA server. Will need the username hostname and password
    def back_up(self, host, username, password, backupuser=None):
        # instantiate the paramiko ssh client
        self.client = paramiko.SSHClient()
        # this will automatically add the host keys of the server.
        # If the keys aren't present paramiko will raise an error
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # write COE info to the coe output file
            message = 'Connecting via ssh to:' + host
            Write_to_coe.write_to_coe(self.coe_output_file, message)
            self.Log.info(message)
            # connect with the SSH host
            self.client.connect(hostname=host, port=13370, username=username, password=password)
            # TODO: move all input to main class
            # ask for root pass should be moved to the main class
            root_pass = input('Please enter the root password of the server:')
            if backupuser != '':
                message = 'Creating back-up for user: ' + backupuser
                Write_to_coe.write_to_coe(self.coe_output_file, message)
                # This command will create a back-up for a specific user.
                backupcommand = 'echo \'action=backup&append%5Fto%5Fpath=nothing&database%5Fdata%5Faware=yes&email%5Fdata%5Faware=yes&local%5Fpath=%2Fhome%2Fadmin%2Fadmin%5Fbackups&owner=admin&select%30='+ backupuser +'&type=admin&value=multiple&when=now&where=local\' >> /usr/local/directadmin/data/task.queue'
            else:
                message = 'Creating back-up for all users'
                Write_to_coe.write_to_coe(self.coe_output_file, message)
                # This command will create a back-up for all the users.
                backupcommand = 'echo \'action=backup&append%5Fto%5Fpath=nothing&database%5Fdata%5Faware=yes&email%5Fdata%5Faware=yes&local%5Fpath=%2Fhome%2Fadmin%2Fadmin%5Fbackups&owner=admin&type=admin&value=multiple&when=now&where=local&who=all\'>> /usr/local/directadmin/data/task.queue'
            # run the back-up command as the root user.
            self.Log.info("Running back-up command on " + host)
            stdin, stdout, stderr = self.client.exec_command('su -c \"' + backupcommand + '\"')
            # input the root password
            stdin.write(root_pass+'\n')
            stdin.flush()
            print(stdout.readlines())
            # this command will force the back-up command to run.
            self.Log.info('Forcing back-up command')
            checkcommand = '/usr/local/directadmin/dataskq d200'
            # run the force command
            stdin, stdout, stderr = self.client.exec_command('su -c \"' + checkcommand + '\"')
            stdin.write(root_pass+'\n')
            stdin.flush()
        except paramiko.ssh_exception.SSHException as e:
            print('Connection failed')
            self.Log.error('Connecting to host Failed: ' + str(e))
            print(e)

    # this function will connect via ftp and download the created back-up file
    def download_backup(self, username, password, host, download_path):

        # TODO: calculate hash of downloaded file and write it to a file
        with closing(ftplib.FTP()) as ftp:
            try:
                message = 'Connecting via ftp to: ' + host
                Write_to_coe.write_to_coe(self.coe_output_file, message)
                self.Log.info(message)
                ftp.connect(host,)

                ftp.login(username, password)
                ftp.set_pasv(True)
                # change the directory to the the back-up folder
                self.Log.info('Change FTP dir to: /admin_backups')
                ftp.cwd('/admin_backups')
                files = ftp.nlst()
                download_index = None
                # list all files in the back-up folder
                while download_index != 0:
                    i = 0
                    for file in files[2:]:
                        i += 1
                        print(str(i) + " " + file)
                    print('0 Exit')
                    index_input = False
                    # will loop until a correct index has been input
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
                    # instantiate the filename of the back-up file
                    filename = files[download_index+1].lstrip()
                    print("Downloading File:" + filename)
                    message = 'Downloading File: ' + filename
                    Write_to_coe.write_to_coe(self.coe_output_file, message)
                    self.Log.info("Downloading File: " + filename)
                    localfile = os.path.join(download_path, filename)
                    # download the back-up file
                    ftp.retrbinary("RETR " + filename, open(localfile, 'wb').write, 8*1024)
                    message = 'Calculating hash of file: ' + filename
                    # calculate the hash value of the file and write it to the COE file.
                    hash = self.main.bereken_hash(localfile)
                    Write_to_coe.write_to_coe(self.coe_output_file, message, hash)
                    self.Log.info(message + str(hash))

                    print("Downloading complete")
                # close the FTP connection
                ftp.quit()
            except ftplib.error_perm as e:
                print(e)
                self.Log.error('Error occurred while download: ' + str(e))

    # function to download the log files from the server.
    def download_log(self, username, password, host, server_log_path):

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=host, port=13370, username=username, password=password)
            self.Log.info('Connecting via SSH to: ' + host)

            rootPass = input('Please enter the root password of the server:')
            stdin, stdout, stderr = self.client.exec_command('su -c \" cat /var/www/html/phpMyAdmin/log/auth.log* \"')
            stdin.write(rootPass+'\n')
            auth_log = uniquify.uniquify(os.path.join(server_log_path, 'auth.log'))
            self.Log.info('Writing phpMyadmin auth.log to file: '+ auth_log)

            with open(auth_log, 'w') as file:
                for line in stdout.readlines():
                    file.write(line)
            # use cat to get the log files, because to access them you need root access.
            stdin, stdout, stderr = self.client.exec_command('su -c \" cat /var/log/secure* \"')
            stdin.write(rootPass + '\n')
            # TODO: make the output filename variable and build in a check to detect if the filename already exist.
            secure_log = uniquify.uniquify(os.path.join(server_log_path, 'secure.log'))

            with open(secure_log, 'w') as file:
                for line in stdout.readlines():
                    # Write the output to the log file.
                    file.write(line)

            stdin, stdout, stderr = self.client.exec_command('su -c \" cat /var/log/httpd/access_log* \"')
            stdin.write(rootPass + '\n')
            http_access_log = uniquify.uniquify(os.path.join(server_log_path, 'httpaccess.log'))
            with open(http_access_log, 'w') as file:
                for line in stdout.readlines():
                    print(line)
                    file.write(line)
            Log_analysis.analyse_log(secure_log, 'SSH_logins')
            Log_analysis.analyse_log(http_access_log, 'PHP_MyADMin_logins')
            Log_analysis.analyse_log(auth_log, 'PHP_MyADMin_logins', auth=True)
        # except all ssh exceptions.
        except paramiko.ssh_exception.SSHException as e:
            print(e)
