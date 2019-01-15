import os


def listdir(path, input_question, files=False):
    dir_list = os.listdir(path)
    name_list = []
    i = 0
    for file in dir_list:

        if os.path.isdir(os.path.join(path, file)) or file.endswith('.sql'):
            i += 1
            print(str(i) + " " + file)
            name_list.append(file)
        # elif os.path.exists(os.path.join(path, file)) and file.endswith() and files is True:
        #     i += 1
        #     print(str(i) + " " + file)

    index_input = False
    while index_input is False:
        folder_index = input(input_question)
        try:
            val = int(folder_index)
            index_input = True
            if val > len(name_list):
                index_input = False
                raise ValueError
            nextfolder = os.path.join(path, name_list[val - 1])
            index_input = True
        except ValueError:
            print('This is not a correct index please try again')

            index_input = False
            return None

    return nextfolder