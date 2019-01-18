import mailbox
import os
import main
from resources import list_dir
import csv


class Mail_analysis:

    def __init__(self, casedir_path):
        self.casedir_path = casedir_path
        self.mailbak_path = os.path.join(casedir_path)
        self.log = main.Main().Log()
        self.output_path = os.path.join(self.casedir_path, '..\output\mails')

    # let the user select the correct maildir
    def load_maildir(self):
        if os.listdir(self.mailbak_path):
            nextfolder = list_dir.listdir(self.mailbak_path, 'Please enter the index of the back-up of which you want to analyse the maildir')
            nextfolder = os.path.join(nextfolder, 'imap')
            print(nextfolder)
            thirdfolder = list_dir.listdir(nextfolder, 'Please enter the index of the domain you want to analyse the mail from')
            # select the maildir
            self.maildir = list_dir.listdir(thirdfolder, 'Please enter the index of the maildir you want to analyse')
            self.output_name = os.path.basename(self.maildir)
            self.log.info('Selecting maildir folder' + self.maildir)
            print(self.maildir)
            self.showmail(self.maildir)
        else:
            # Give warning when the extraction folder is empty
            print('The extraction folder is empty, please download and extract the back-up first')
            self.log.warning('The extraction folder doesn\'t contain any files')

    # Write the mail to an csv file. And still needs some kind of analysis.
    def showmail(self, maildir):
        self.attachment_output = os.path.join(self.output_path, 'attachments')
        # create the attachment output folder.
        if not os.path.exists(self.attachment_output):
            os.makedirs(self.attachment_output)
        # open the sent maildir
        mbox = mailbox.Maildir(os.path.join(maildir, 'Maildir', '.Sent'))
        mbox.lock()

        index_input = False
        val = 0
        while index_input is False:
            # select if all sent mails must be written to the csv file or only the mails with attachments
            print('1. Filter out all sent mails')
            print('2. Filter only sent mails with attachments.')
            print('')
            attachment = input('Extract all sent mails or only with attachment?')
            try:
                val = int(attachment)
                index_input = True
                if val > 2 or val <= 0:
                    index_input = False
                    raise ValueError
                index_input = True
            except ValueError:
                print('This is not a correct input please try again')

                index_input = False
                return None
        i = 1
        counter = 1
        for message in mbox:
            if val == 1:
                if message is not None:
                    self.write_mail(message, counter)
                    counter += 1
                else:
                    print("No e-mails found")
                    self.log.info("No e-mail messages found")

            if message.get_content_maintype() == 'multipart' and val == 2:
                self.write_mail(message, counter)
                counter += 1

                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    print(filename)
                    fb = open(os.path.join(self.attachment_output, i+filename), 'w')
                    i +=1
                    fb.write(part.get_payload(decode=True))
                    fb.close()
            else:
                print("No e-mails found")
                self.log.info("No e-mail message found")

    # Write the mail to a CSV file
    def write_mail(self, message, message_nr):
        with open(os.path.join(self.output_path, self.output_name+'.csv'), 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['-------------------------------------'])
            writer.writerow(['Message Nr', message_nr])
            for key, value in message.items():
                writer.writerow([key, value])
            if message.is_multipart():
                content = ''.join(part.get_payload(decode=True) for part in message.get_payload())
            else:
                content = message.get_payload(decode=True)
            temp = ''
            for char in str(content):
                temp = temp +char

                if "\\n" in temp:
                    temp = temp.replace('\\n', '')
                    print(temp)
                    writer.writerow([temp])
                    temp = ''
                elif "\\" in temp:
                    continue
            writer.writerow(['-------------------------------------'])
