import main
import tarfile
import os
import sys
import csv
from time import gmtime, strftime


class FileExtraction:
    def __init__(self):

        self.extract_path = None
        self.Log = main.Main().Log()


    # TODO: Add more logging to this section also add data to the coe file.
    def extract(self, filename, extract_path, download_path, coe_output_file):
        self.download_path = download_path
        self.extract_path = extract_path
        self.coe_output_file = coe_output_file

        if filename == '*':
            self.extractAll()
        else:
            print(os.path.join(self.download_path, filename))
            self.extractFile(os.path.join(self.download_path, filename))

    def extractFile(self, file):
        if os.path.exists(file) :
            if file.endswith('tar.gz'):
                self.Log.info("Opening tar.gz file:" + file)
                tar = tarfile.open(file, 'r:gz')
                print('extracting tar file:' + file)
                temp = os.path.basename(file)
                dirname = os.path.splitext(os.path.splitext(temp)[0])[0]
                finalPath = os.path.join(self.extract_path, dirname)

                if not os.path.exists(finalPath):
                    self.Log.info('Creating directory:' + finalPath)
                    os.makedirs(finalPath)
                    self.Log.info('Extracting tar.gz to:' + finalPath)
                    tar.extractall(finalPath)
                    self.Log.info('Extraction complete')
                    print('Extraction complete')
                    tar.close()
                    print('Calculating hashes of extracted files')
                    self.calculateHash(finalPath, dirname)
                elif os.path.exists(finalPath):
                    print('Warning the extraction folder already exists: ' + finalPath )
                    print('Rename or move the folder and restart the script to extract the files')
                    self.Log.warning('Folder:' + finalPath + 'exists')
                    self.Log.warning('Stopping extraction script.')

    def extractAll(self):
        listOfFile = os.listdir(self.download_path)
        for entry in listOfFile:
            fullPath = os.path.join(self.download_path, entry)
            if os.path.isdir(fullPath):
                print('dir')
            elif fullPath.endswith('tar.gz'):
                self.extractFile(fullPath)
            else:
                print('this is not a tar.gz file, skipping')

    def calculateHash(self, path, dirname):
        hashFile = os.path.join(path, dirname + 'hashes.csv')
        with open(hashFile, 'w') as file:
            filewriter = csv.writer(file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Date', 'Filename', 'Hash'])
            for path, subdirs, files in os.walk(path):
                for name in files:
                    print(os.path.join(path, name))
                    hash = main.Main().bereken_hash(os.path.join(path, name))
                    filewriter.writerow([str(strftime("%Y-%m-%d %H:%M:%S", gmtime())), os.path.join(path, name), str(hash)])

