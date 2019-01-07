import mailbox
import email.utils
import os


class Mail_analysis:

    def __init__(self):
        self.output = None
        self.casedir_path = None
        self.mailbak_path = None

    def load_maildir(self, casedir_path):
        self.casedir_path = casedir_path
        self.mailbak_path = os.path.join(casedir_path)
        nextfolder = self.listdir(self.mailbak_path, 'Please enter the index of the back-up of which you want to analyse the maildir')
        nextfolder = os.path.join(nextfolder, 'imap')
        print(nextfolder)
        thirdfolder = self.listdir(nextfolder, 'Please enter the index of the domain you want to analyse the mail from')
        self.maildir = self.listdir(thirdfolder, 'Please enter the index of the maildir you want to analyse')
        print(self.maildir)


    def showmail(self):
        print('')

    def listdir(self, path, input_question):
        dir_list = os.listdir(path)
        print(path)
        print (len(dir_list))
        i = 0
        for file in dir_list:

            if os.path.isdir(os.path.join(path,file)):
                i += 1
                print(str(i) + " " + file)

        index_input = False
        while index_input is False:
            folder_index = input(input_question)
            try:
                val = int(folder_index)
                index_input = True
                if val > len(dir_list):

                    index_input = False
                    raise ValueError
            except ValueError:
                print('This is not a correct index please try again')
        nextfolder = os.path.join(path, dir_list[val -1])
        return nextfolder