import mailbox
import email.utils
import os
import main
from resources import list_dir

# todo : make maildir filter out all mails with attachements.
class Mail_analysis:

    def __init__(self, casedir_path):
        self.casedir_path = casedir_path
        self.mailbak_path = os.path.join(casedir_path)
        self.log = main.Main().Log()
    # let the user select the correct maildir
    def load_maildir(self):
        if os.listdir(self.mailbak_path):
            nextfolder = list_dir.listdir(self.mailbak_path, 'Please enter the index of the back-up of which you want to analyse the maildir')
            nextfolder = os.path.join(nextfolder, 'imap')
            print(nextfolder)
            thirdfolder = list_dir.listdir(nextfolder, 'Please enter the index of the domain you want to analyse the mail from')

            self.maildir = list_dir.listdir(thirdfolder, 'Please enter the index of the maildir you want to analyse')
            self.log.info('Selecting maildir folder' + self.maildir)
            print(self.maildir)
            self.showmail(self.maildir)
        else:
            print('The extraction folder is empty, please download and extract the back-up first')
            self.log.warning('The extraction folder doesn\'t contain any files')


    # TODO test this function with a know good maildir,because it looks like this function doesn't work as it suposed to
    # Write the mail to an csv file. And still needs some kind of analysis.
    def showmail(self, maildir):
        mbox = mailbox.Maildir(os.path.join(maildir, 'Maildir'))
        mbox.lock()
        for message in mbox:
            if message.get_content_maintype() == 'multipart':
                print(message['subject'])
                print(message['To'])
                print(message['From'])
                print(message['Date'])

                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    print(filename)

            print(message)
        print('')

    # list the content of a selected dir.
    # This function will be used to loop through the different back-up folders to finally select the maildir.
