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
        self.mailbak_path = os.path.join(casedir_path, 'imap')
        dir_list = os.listdir(self.mailbak_path)
        i = 0
        for file in dir_list:
            if os.path.isdir(file):
                i+=1
                print(str(i) + ':' + file)


        index_input = False
        while index_input is False:
            folder_index = input('Select of what domain you want to analyse the maildir:')
            try:
                val = int(folder_index)

            except ValueError:
                print('This is not a correct index please try again')

            # index_input = False
            # while index_input is False:
            #     download_index = input("What file do you want to download?")
            #     try:
            #         val = int(download_index)
            #         download_index = val
            #         index_input = True
            #     except ValueError:
            #         self.Log.error("Wrong Index number")
            #
            # if download_index == 0:
            #     continue
        print('')

    def showmail(self):
        print('')
