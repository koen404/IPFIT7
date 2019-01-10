import re
import os
import csv
from collections import Counter
# TODO: extract the IP-adressess from the log files. Check what IP's have logged in successfully


def analyse_log(logfile, filename):
    abs_path = os.path.abspath(os.path.dirname(logfile))
    output_path = os.path.join(abs_path, '../output')

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    failed_ip = []
    successfull_ip = []

    with open(logfile, 'r') as file:
        i = 0
        output_file = os.path.join(output_path, filename)
        while os.path.exists(output_file):
            i += 1
            filename = filename + str(i)
            output_file = (os.path.join(output_path, filename))
        for line in file:
            if 'Accepted' in line:
                ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop()
                successfull_ip.append(ip)
                output_line = line.replace(ip, '')
                # (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                # (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)
                #
                date = re.findall('([0-2][0-9]|(3)[0-1])(\/)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\/)\d{4}:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)|((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2} (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d))',line).pop()
                output_log(filename, ip, date)
                print(output_line)
            if 'Failed' in line:
                ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop()
                date = re.findall('([0-2][0-9]|(3)[0-1])(\/)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\/)\d{4}:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)',line).pop()
                output_log(filename, ip, date)

                failed_ip.append(ip)
        failed_login_oc = Counter(failed_ip)
        successfull_login_oc = Counter(successfull_ip)
        output_log(output_file, 'Failed_IP:', date='', log_message='Amount')
        for k, v in failed_login_oc.most_common():
            output_log(output_file, k, date='', log_message=str(v))

        output_log(output_file, 'Successful_IP:', date='', log_message='Amount')
        for k, v in successfull_login_oc.most_common():
            output_log(output_file, k, date='', log_message=str(v))


def output_log(file,  IP, date='', log_message='', log_message3=''):
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
