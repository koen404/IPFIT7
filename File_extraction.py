import main
import tarfile
import os
import sys
import csv
from time import gmtime, strftime

class FileExtraction:
    def __init__(self):
        self.filename = None
        self.Log = main.Main().Log()
        self.downloadPath = main.Main().download_path
        self.extractPath = os.path.join(sys.path[0], "extract")
        if os.path.exists(self.extractPath):
            self.warning_bool = True
        elif not os.path.exists(self.extractPath):
            os.makedirs(self.extractPath)
            self.warning_bool = False

    def extract(self, filename):
        if self.warning_bool is True:
            print('Warning output folder already hold files either remove them or rename the folder')
            print('Exiting script')
            self.Log.warning('Output folder:' + self.extractPath + 'already hold files')

        elif self.warning_bool is False:
            if filename == '*':
                self.extractAll()
            else:
                print(os.path.join(self.downloadPath, filename))
                self.extractFile(os.path.join(self.downloadPath, filename))

    def extractFile(self, file):
        if os.path.exists(file) and self.warning_bool is False:
            if file.endswith('tar.gz'):
                self.Log.info("Opening tar.gz file:" + file)
                tar = tarfile.open(file, 'r:gz')
                print('extracting tar file:' + file)
                temp = os.path.basename(file)
                dirname = os.path.splitext(os.path.splitext(temp)[0])[0]
                finalPath = os.path.join(self.extractPath, dirname)

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


    def extractAll(self):
        listOfFile = os.listdir(self.downloadPath)
        for entry in listOfFile:
            fullPath = os.path.join(self.downloadPath, entry)
            if os.path.isdir(fullPath):
                print('dir')
            elif fullPath.endswith('tar.gz'):
                self.extractFile(fullPath)
            else:
                print('this is not a tar.gz file, skipping')

    def calculateHash(self, path, dirname):
        hashFile = os.path.join(path, dirname + '.csv')
        with open(hashFile, 'w') as file:
            filewriter = csv.writer(file,delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Date', 'Filename', 'Hash'])
            for path, subdirs, files in os.walk(path):
                for name in files:
                    print(os.path.join(path, name))
                    hash = main.Main().bereken_hash(os.path.join(path, name))
                    filewriter.writerow([str(strftime("%Y-%m-%d %H:%M:%S", gmtime())), os.path.join(path, name), str(hash)])
            # filewriter.close()

