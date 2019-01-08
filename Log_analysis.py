
# TODO: extract the IP-adressess from the log files. Check what IP's have logged in successfully
def analyse_log(logfile, http_log=None):
    if 'auth' in logfile:
        print('analyzing auth.log')
        for line in logfile:


    elif 'secure' in logfile:
        print('analyzing secure.log')