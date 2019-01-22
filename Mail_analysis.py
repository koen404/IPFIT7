import mailbox
import os
import main
import csv
import tkinter
from resources import uniquify
from tkinter.filedialog import askdirectory

class Mail_analysis:

    def __init__(self, casedir_path):
        self.casedir_path = casedir_path
        self.mailbak_path = os.path.join(casedir_path)
        self.log = main.Main().Log()
        self.output_path = os.path.join(self.casedir_path, '..', 'output', 'mails')

    # let the user select the correct maildir
    def load_maildir(self):
        root = tkinter.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()
        if os.path.exists(self.mailbak_path):
            if os.listdir(self.mailbak_path):
                # open tkinter file browser to select the maildir
                self.maildir = askdirectory(initialdir=self.mailbak_path, parent=root)
                # if the file selection has been cancelled by the user.
                if not self.maildir:
                    print('User cancelled folder selection returning to main')
                    self.log.info('User cancelled folder selection returning to main')
                # Check if the folder maildir exist in the selected folder
                elif 'Maildir' in os.listdir(self.maildir):
                    self.output_name=os.path.basename(self.maildir)
                    self.log.info('Selecting maildir folder' + self.maildir)
                    self.show_mail(self.maildir)
                # If there is no 'Maildir' in the selected folder
                elif 'Maildir' not in os.listdir(self.maildir):
                    print('That\'s not a Maildir.')

                    self.log.warning('None valid Maildir folder selected')

                root.destroy()
        else:
            print('The back-up file hasn\'t been extracted, please run the extraction option (3)')
            self.log.warning('Back-up file hasn\'t been extracted')

    # Write the mail to an csv file. And still needs some kind of analysis.
    def show_mail(self, maildir):

        # open the sent maildir



        index_input = False
        val = self.get_input('1. Filter out sent mails','2. Filter out received mails','Filter out sent or received?')

        sent = False
        if val == 1:
            sent = True
        elif val == 2:
            sent = False
        self.analyse_mails(maildir, sent)


    # Write the mail to a CSV file
    def write_mail(self, message, message_nr, output_name):
        content = ''
        temp = self.output_name + output_name
        # create a unique output file
        with open(uniquify.uniquify(os.path.join(self.output_path, temp+'.csv')), 'a') as csv_file:
            writer = csv.writer(csv_file)
            # write the row diversions
            writer.writerow(['-------------------------------------'])
            # write the message number
            writer.writerow(['Message Nr', message_nr])
            for key, value in message.items():
                writer.writerow([key, value])
            if message.is_multipart():
                content = message.get_payload()[0]
                temp2 = str(content)
                for char in temp2:
                    temp = temp + char

                    if "\n" in temp:

                        print(temp)
                        writer.writerow([temp])
                        temp = ''

                writer.writerow(['-------------------------------------'])

            else:
                content = message.get_payload(decode=True)
                temp = ''
                for char in str(content):
                    temp = temp +char

                    if "\\n" in temp:
                        temp = temp.replace('\\n', '')
                        # print(temp)
                        writer.writerow([temp])
                        temp = ''
                    elif "\\" in temp:
                        continue
                writer.writerow(['-------------------------------------'])

    def analyse_mails(self, maildir, sent=False):
        if sent==True:
            mbox = mailbox.Maildir(os.path.join(maildir, 'Maildir', '.Sent'))
            output_name = 'Sent'
        else:
            mbox = mailbox.Maildir(os.path.join(maildir, 'Maildir'))
            output_name = 'received'

        self.attachment_output = os.path.join(self.output_path, 'attachments')
        # create the attachment output folder.
        if not os.path.exists(self.attachment_output):
            os.makedirs(self.attachment_output)

        mbox.lock()
        val = self.get_input('1. Filter out all  mails', '2. Filter only mails with attachments.', 'Extract all sent mails or only with attachment?')

        i = 1
        counter = 1
        for message in mbox:
            if val == 1:

                if message is not None:
                    self.write_mail(message, counter, output_name)
                    counter += 1
                else:
                    print("No e-mails found")
                    self.log.info("No e-mail messages found")
            # Check if the message is mulitpart/mixed otherwise it would cause false positives
            if message.get_content_type() == 'multipart/mixed' and val == 2:
                finaloutput = output_name+'_at'
                self.write_mail(message, counter, finaloutput)
                counter += 1

                for part in message.walk():
                    print(part.get_content_maintype())
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    print(filename)
                    fb = open(os.path.join(self.attachment_output, str(i) + filename), 'wb')
                    i += 1
                    fb.write(part.get_payload(decode=True))
                    fb.close()

    def get_input(self, question, question2, input_question):
        index_input = False
        val = 0
        while index_input is False:
            # select if all sent mails must be written to the csv file or only the mails with attachments
            print(question)
            print(question2)
            print('')
            attachment = input(input_question)
            try:
                val = int(attachment)
                if val > 2 or val <= 0:
                    raise ValueError
                else:
                    return val
            except ValueError:
                print('This is not a correct input please try again')

                index_input = False
