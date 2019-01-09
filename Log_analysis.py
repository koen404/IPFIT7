import re
import os
import csv
# TODO: extract the IP-adressess from the log files. Check what IP's have logged in successfully
def analyse_log(logfile):
    abs_path = os.path.abspath(os.path.dirname(logfile))
    output_path = os.path.join(abs_path, '../output')

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    failed_ip = []
    successfull_ip = []
    if 'secure' in logfile:
        print('analyzing auth.log')
        with open(logfile, 'r') as file:
            for line in file:
                if 'Accepted' in line:
                    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop()
                    successfull_ip.append(ip)
                    output_line = line.replace(ip, '')
                    # (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                    # (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                    #
                    # ([0-2][0-9]|(3)[0-1])(\/)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\/)\d{4}:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                    print(output_line)
                if 'Failed' in line:
                    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop()
                    failed_ip.append(ip)

        print(failed_ip)
        print(successfull_ip)

def output_log(file, log_message, log_message2 = '', log_message3=''):
    filewriter = csv.writer(file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
