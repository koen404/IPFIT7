import re
import os
import csv
from resources import Write_to_coe
import main
from collections import Counter
from resources import uniquify

class Log:
    def __init__(self):
        self.Log = main.Main().Log()
    # function to analyse the log files
    def analyse_log( self, logfile, filename, auth=False):
        # set the output path
        abs_path = os.path.abspath(os.path.dirname(logfile))
        os.chdir(abs_path)
        output_path = os.path.abspath('../output/Logs')

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            self.Log.info('Creating directory: ' + output_path)

        failed_ip = []
        successfull_ip = []
        output_file = os.path.join(output_path, filename)
        if os.path.exists(output_file) and auth is False:
            output_file = uniquify.uniquify(output_file)
            self.Log.info('Set output file to' + output_file)

        with open(logfile, 'r') as file:
            if 'secure' in logfile:
                for line in file:
                    if 'Accepted' in line:
                        print (line)
                        ip = self.getIP(line)
                        successfull_ip.append(ip)
                        line = line.replace(ip, 'IP')
                        # (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                        # (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                        #([0-2][0-9]|(3)[0-1])(\/)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\/)\d{4}:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                        date = re.search('((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d))',line).group()
                        line = line.replace(date, '')
                        self.output_log(output_file, ip, date, line)
                    if 'Failed' in line:
                        ip = self.getIP(line)
                        failed_ip.append(ip)
                        line = line.replace(ip, 'IP')
                        date = re.search('((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d))',line).group()
                        line = line.replace(date, '')
                        self.output_log(output_file, ip, date, line)
                self.write_ip(successfull_ip, output_file, 'Succesfull_logged_in_IP\'s')
                self.write_ip(failed_ip, output_file, 'Failed_logged_in_IP\'s')
            elif 'access' in logfile:
                for line in file:
                    if 'POST /phpmyadmin/ajax.php' in line:
                        ip = self.getIP(line, pop_index=0)
                        print(ip)
                        line = line.replace(ip, '')
                        date = re.search('(([0-2][0-9]|(3)[0-1])(\/)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\/)\d{4}:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d))', line).group()
                        line = line.replace(date, '')
                        self.output_log(output_file, ip, date, line)
                        successfull_ip.append(ip)
                self.write_ip(successfull_ip, output_file, 'Successful IP')
            elif 'auth' in logfile:
                for line in file:
                    ip = self.getIP(line)
                    failed_ip.append(ip)
                    line = line.replace(ip, '')
                    date = re.search('((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d))', line).group()
                    line = line.replace(date, '')
                self.write_ip(failed_ip, output_file, 'Failed IP')


    def output_log(self, file,  IP, date='', log_message='', log_message3=''):
        if not os.path.exists(file):
            output = open(file, 'w')
            filewriter = csv.writer(output, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Timestamp', 'IP', 'Logmessage'])
            output.close()

        with open(file, 'a') as file:
            filewriter = csv.writer(file, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([date, IP, log_message, log_message3])

    def getIP(self, line, pop_index=None):
        if pop_index is None :
            ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop()
        else:
            ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop(pop_index)
        return ip

    def getdate(self, line):
        date = re.search(
            '((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d))',
            line).group()
        return date

    def write_ip(self, ip_list, output, message):

        ip_oc = Counter(ip_list)

        self.output_log(output, message, date='', log_message='Amount')
        for k, v in ip_oc.most_common():
            self.output_log(output, k, date='', log_message=str(v))
