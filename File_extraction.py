import main
import tarfile
import os
import sys

class FileExtraction:
    def __init__(self):
        self.filename = None
        self.Log = main.Main().Log()
        self.downloadPath = main.Main().download_path
        self.extractPath = os.path.join(sys.path[0], "extract")
        if not os.path.exists(self.extractPath):
            os.makedirs(self.extractPath)

    def extract(self, filename):
        if filename == '*':
            self.extractAll()
        else:
            print(os.path.join(self.downloadPath, filename))
            self.extractFile(os.path.join(self.downloadPath, filename))

    def extractFile(self, file):
        if os.path.exists(file):
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
