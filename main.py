import logger
import os
import DA_backup
class Main:

    def __init__(self):
        self.Log = logger.logger.log()

        self.choices_main = {
                "1": self.DA_backup,
                "2": self.File_analysis,
                "3": self.quit

                }
    def display_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
        Menu
        1. DA_backup
        2. File_analysis
        3. Quit
        """)

    def run(self):
        self.Log().info("Starting Main_Script")
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices_main.get(choice)
            self.Log().info("User input: %s", choice)
            if action:
                action()
            else:
                self.Log().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    def DA_backup(self):
        username = 'admin'
        password = input('please enter password')
        host = input('please enter host')


if __name__ == "__main__":
    Main().run()
