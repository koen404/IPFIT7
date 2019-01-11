from time import gmtime, strftime
import csv
import os

def write_to_coe(output_file, message, hash=''):
    with open(output_file, 'a') as file:
        filewriter = csv.writer(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([str(strftime("%Y-%m-%d %H:%M:%S", gmtime())), message, hash])

def get_coe_output(casedir):
    abs_path = os.path.abspath(os.path.dirname(casedir))
    os.chdir(abs_path)
    coe_output_file = os.path.abspath('output')
    return coe_output_file
