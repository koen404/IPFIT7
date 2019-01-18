import main
import tarfile
import os
import sys
import csv
from resources import Write_to_coe
from time import gmtime, strftime


class FileExtraction:
    def __init__(self, casedir):
        self.coe_output_file = Write_to_coe.get_coe_output(casedir)
        self.extract_path = None
        self.Log = main.Main().Log()

    # This is the 'main' function of the extract class, this function will either extract all or extract only one file
    def extract(self, filename, extract_path, download_path, ):
        self.download_path = download_path
        self.extract_path = extract_path

        if filename == '*':
            self.extractAll()
            self.Log.info('Extracting all tar.gz files')
        else:
            self.extractFile(os.path.join(self.download_path, filename))

    # This function will extract a single tar.gz file
    def extractFile(self, file):
        if os.path.exists(file):
            # check if the file ends with .tar.gz
            if file.endswith('tar.gz'):
                # log the filename
                self.Log.info("Opening tar.gz file:" + file)
                # write the step to the COE doc
                Write_to_coe.write_to_coe(self.coe_output_file, "Opening tar.gz file:" + file)
                tar = tarfile.open(file, 'r')
                print('extracting tar file:' + file)
                Write_to_coe.write_to_coe(self.coe_output_file, 'extracting tar file:' + file)

                temp = os.path.basename(file)
                dirname = os.path.splitext(os.path.splitext(temp)[0])[0]
                finalPath = os.path.join(self.extract_path, dirname)
                # check if the extraction path exists, if not create it
                if not os.path.exists(finalPath):
                    self.Log.info('Creating directory:' + finalPath)
                    os.makedirs(finalPath)
                    self.Log.info('Extracting tar.gz to:' + finalPath)
                    tar.extractall(finalPath)
                    self.Log.info('Extraction complete')
                    print('Extraction complete')
                    tar.close()
                    print('Calculating hashes of extracted files')
                    Write_to_coe.write_to_coe(self.coe_output_file, 'Writing hashes of file to: ' + dirname + 'Hashes.csv')
                    self.calculateHash(finalPath, dirname)
                # if the extraction path already exist throw a warning and prevent the files from being overwritten.
                elif os.path.exists(finalPath):
                    print('Warning the extraction folder already exists: ' + finalPath)
                    print('Rename or move the folder and restart the script to extract the files')
                    self.Log.warning('Folder:' + finalPath + 'exists')
                    self.Log.warning('Stopping extraction script.')

    # this function will extract all tar.gz file by calling the extractfile function
    def extractAll(self):
        # will list all files in the directory
        listOfFile = os.listdir(self.download_path)
        for entry in listOfFile:
            fullPath = os.path.join(self.download_path, entry)
            if os.path.isdir(fullPath):
                print('dir')
            # simple check to see if the file ends with .tar.gz if so extract the file
            elif fullPath.endswith('tar.gz'):
                self.extractFile(fullPath)
            else:
                print('this is not a tar.gz file, skipping')

    # this function will calculate the hash of the extracted files by calling the hashing function of the main class
    def calculateHash(self, path, dirname):
        hashFile = os.path.join(path, dirname + 'hashes.csv')
        with open(hashFile, 'w') as file:
            filewriter = csv.writer(file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Date', 'Filename', 'Hash'])
            for path, subdirs, files in os.walk(path):
                for name in files:
                    print(os.path.join(path, name))
                    # call the calculate hash function of the main class
                    hash = main.Main().bereken_hash(os.path.join(path, name))
                    filewriter.writerow([str(strftime("%Y-%m-%d %H:%M:%S", gmtime())), os.path.join(path, name), str(hash)])
