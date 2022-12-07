import numpy as np
from board import Board


def draws(directory, file):
    """
    :param directory: directory where the file is stored <string>
    :param file:  file name with extension to opened <string>
    :return: 1-D numpy array of integers
    """

    # load file
    with open('data/'+directory+'/'+file, 'r') as f:
        numbers = f.read()

    # split string of numbers to array by comma
    numbers = numbers.split(',')
    # Sanitization
    # Remove any non numeric characters from loaded data
    # This step is not necessary for the provided data set
    # However it is a good practice to sanitize data always when import
    numbers = [x for x in numbers if x.isnumeric()]  # remove non numeric entries
    numbers = np.array([int(x) for x in numbers])  # convert to int
    return numbers


def boards(directory, file, board_shape):
    """
    toDo: handle if more than one empty lines were present in the file
    :param directory: directory where the file is stored <string>
    :param file:  file name with extension to opened <string>
    :param board_shape:  number of rows and number cols inboard as tuple
    :return: 3-D numpy array of integers
    """
    with open('data/'+directory+'/'+file) as f:
        collection = f.read()

    rows, cols = board_shape
    # split by new line
    # It was assumed that every single line represent a row of a board
    collection = collection.split("\n")
    # print(collection)
    # detect empty lines
    # It was assumed that boards are separated by a empty line.
    # Therefore content between two empty lines can be considered as a board
    board_separators = [index for index, item in enumerate(collection)
                        if len(item.strip()) == 0]
    # last line of the file also represent a end of board
    board_separators.append(len(collection))
    # print(board_separators)
    start = 0
    all_boards = []
    board_id = 0
    for separator in board_separators:
        # sampling data between boar separators
        temp = collection[start:separator]
        full_board = []
        # sanitization
        # filter line by line for non numeric characters, and correct
        # number of rows and columns
        for line in temp:
            row = line.split()
            row = [x for x in row if x.isnumeric()]  # remove non numeric entries
            row = [int(x) for x in row]  # convert to int
            # skip row if does not comply column count
            if len(row) == cols:
                full_board.append(row)
            else:
                print("invalid row :", row)
        # skip board if does not comply row count
        if len(full_board) == rows:
            all_boards.append(Board(np.array(full_board), board_id, board_shape))
            board_id += 1
        else:
            print('Invalid Board. Row Count does not comply :', len(full_board))

        start = separator+1

    return all_boards
