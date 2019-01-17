from time import gmtime, strftime
import csv
import os

def write_to_coe(output_file, message, hash=''):
    print(output_file)
    with open(output_file, 'a') as file:
        filewriter = csv.writer(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([str(strftime("%Y-%m-%d %H:%M:%S", gmtime())), message, hash])

def get_coe_output(casedir):
    temp = os.path.join(casedir)
    if not os.path.exists(temp):
        os.makedirs(temp)


    coe_output_file = os.path.join(temp, 'coe.csv')
    print(coe_output_file)
    return coe_output_file
