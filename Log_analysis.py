import re


# TODO: extract the IP-adressess from the log files. Check what IP's have logged in successfully
def analyse_log(logfile):
    failed_ip = []
    succesfull_ip = []
    if 'secure' in logfile:
        print('analyzing auth.log')
        with open(logfile, 'r') as file:
            for line in file:
                if 'Accepted' in line:
                    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop()
                    succesfull_ip.append(ip)

                if 'Failed' in line:
                    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line).pop()
                    failed_ip.append(ip)
    print(failed_ip)
    print(succesfull_ip)
    for line in succesfull_ip:
        print(line)
    print('test')