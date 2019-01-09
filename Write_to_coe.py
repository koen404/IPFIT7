from time import gmtime, strftime
import csv


def write_to_coe(coe_output_file, message, hash=''):
    with open(coe_output_file, 'a') as file:
        filewriter = csv.writer(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([str(strftime("%Y-%m-%d %H:%M:%S", gmtime())), message, hash])
