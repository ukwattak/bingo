import numpy as np
from termcolor import colored  # to produce the colored text in the terminal
from PIL import Image, ImageDraw  # to generate the image of a board


class Board:
    def __init__(self, board, _id, shape):
        self.board = board
        self.id = _id
        self.shape = shape

    def draw_indexes(self, draws):
        """
        All the elements in the board will be mapped to draws array and extract
         the element index of the draws array. Extracted element indexes are filled
        to a array size of the board. This process has been graphically explained in
        the Step 3 and 4 in the figure which explains the solution
        :param draws: all the draws as 1D numpy array
        :return: 2D numpy array
        """

        board_shape = np.shape(self.board)
        # Flatten the board in to a 1D array for easy handling
        board = self.board.reshape(-1)
        # Build an array with indexes of draws which matches the numbers of the board
        # Every cell contains a array indexes and the original number from the board
        indexes = [[np.where(draws == number)[0], number] for number in board]
        output = []
        for index in indexes:
            # Check if numbers in the board exists in the draw
            # If not produces a invalid number message
            if len(index[0]) > 0:
                # It is assumed that all the draws are unique and no duplicates
                # Therefore, there will be only one index for a given board number.
                output.append(index[0][0])
            else:
                # Boards are already shaped to 5 x 5 during load
                # If any number was skipped here it will produces an error during
                # re-shaping and entire program will fail
                # This condition has not been address here.
                print("Invalid number :", index[1], " does not exist in the draws. This board will never win")

        # Reshape the indexes array into the shape of the board
        return np.reshape(np.array(output), board_shape)

    def wining_draw(self, draws):
        """
        1. Get the maximum of every row and column
        2. Then get the minimum of those maximums which would be the
        wining draw for the given board
        3. Step 5, 6 and 7 in the schematic given in the solution section
        are done here
        :param draws: 1D array
        :return: Scaler ; the wining draw
        """
        # print(draws)
        rows, cols = self.shape
        # Flatten the board in to a 1D array for easy handling
        board = self.board.reshape(-1)
        # Build an array with indexes of draws which matches the numbers of the board
        # Every cell contains a array indexes and the original number from the board
        indexes = [[np.where(draws == number)[0], number] for number in board]
        output = []
        for index in indexes:
            output.append(index[0][0])

        # Reshape the indexes array into the shape of the board
        indexes = np.reshape(np.array(output), (rows, cols))
        # print(indexes)
        # get the maximum of the rows
        # find the minimum of those maximums
        row_win = min([max(indexes[index, :]) for index in range(rows)])
        # get the maximum of the columns
        # find the minimum of those maximums
        col_win = min([max(indexes[:, index]) for index in range(cols)])
        # get the minimum of above two minimums which represent the wining
        # draw of the board.
        return min([row_win, col_win])

    def diagonals(self):
        """
        this method returns both diagonals of the board.
        This method is not needed for the standard solution provided
        However, This method will be used for the extended solution.
        if assume that we have access to full board configuration.

        :return: return both diagonal of the board
        """
        ax1 = np.diagonal(self.board)
        ax2 = np.diagonal(np.fliplr(self.board))
        return ax1, ax2

    def board_score(self, draws, wining_draw):
        """

        :param draws: Full set of draws ; 1D array
        :param wining_draw: The index of the draws array for the wining
        draw of the board
        :return: Scaler; the score of the board after the wining draw
        """

        # Flatten the board for easy handling
        board = self.board.reshape(-1)
        # Actual value of the wining draws
        last_number = draws[wining_draw]
        # At all the numbers drawn until the wining draw include the wining draw
        # These numbers represent the marked numbers of the bord
        drawn_numbers = draws[:wining_draw+1]
        # Extract all unmarked numbers from the board
        remaining_numbers = board[~np.isin(board, drawn_numbers)]
        # print(remaining_numbers)
        # Add all the unmarked numbers together and multiply by the last draw
        # The score of the board
        return np.sum(remaining_numbers)*last_number

    def print(self, draws, wining_draw):
        """
        This method will print the board in the terminal with

        :param draws: Full set of draws ; 1D array
        :param wining_draw: The index of the draws array for the wining
        draw of the board
        :return: Nothing will be returned
        """

        # The last drawn number
        last_number = draws[wining_draw]
        # All the drawn numbers till the board wins including the wining draw
        drawn_numbers = draws[:wining_draw + 1]
        rows, cols = self.shape
        print("------------------")
        print('Board Id :', self.id)
        for row in range(rows):
            print("|", end="")
            for col in range(cols):
                # All the numbers will be padded with 0 in the left if it is single digit
                # for visual clarity
                # If the value equal to the last draw, text will be colored green
                if self.board[row, col] == last_number:
                    print(colored(str(self.board[row, col]).zfill(2), 'green'), "|", end=" ")
                # If the value is drawn, text will be colored red
                elif self.board[row, col] in drawn_numbers:
                    print(colored(str(self.board[row, col]).zfill(2), 'red'), "|", end=" ")
                else:
                    print(colored(str(self.board[row, col]).zfill(2), 'white'), "|", end=" ")
            print()

        print("Legend ...")
        print("Color ", colored("green", 'green'), " represent the last drawn number")
        print("Color ", colored("red", 'red'), " represent the previously drawn numbers")
        print("Color ", colored("white", 'white'), " represent the remaining numbers")
        print("------------------")

    def print_card(self,  draws, wining_draw, total_boards, title):
        """
        Generate the card as a .png file
        :param draws: 1D array of draws
        :param wining_draw:  the wining draw (count) as int
        :param total_boards: Total numbers of boards loaded ats in
        :param title:  Title of the image generated as string
        :return:
        """

        min_width = 400
        rows, cols = self.shape
        offset_left, offset_top, offset_right, offset_bottom = (20, 20, 20, 20)
        row_height = 40
        col_width = 40
        text_width = 200
        texts = [
            "Total Draws: " + str(len(draws)),
            "Total boards: " + str(total_boards),
            "Board Id (This) : " + str(self.id),
            "Board Score : " + str(self.board_score(draws, wining_draw)),
            "The Wining Draw : " + str(wining_draw) + " Draw",
            "",
           ]

        legends = [
            ['blue', 'Last Drawn Number'],
            ['orange', 'Previously Drawn Numbers'],
            ['gray', 'Remaining Numbers'],
        ]

        line_height = 20
        title_height = 20
        min_height = offset_top+line_height * (len(texts) + len(legends))+offset_bottom
        width = offset_left + col_width*rows + offset_right + text_width
        width = width if width > min_width else min_width
        height = offset_top + row_height*cols + offset_bottom + title_height
        height = height if height > min_height else min_height
        img = Image.new('RGB', (width, height), color='white')
        img1 = ImageDraw.Draw(img)

        text_xy = (50, 10)
        img1.text(text_xy, title, fill="black", font=None, anchor=None, spacing=0, align="center")

        text_offset_x = offset_left + col_width * rows + 20
        text_offset_y = offset_top + title_height

        for index, text in enumerate(texts):
            text_xy = (text_offset_x, text_offset_y + line_height * index)
            img1.text(text_xy, text, fill="black", font=None, anchor=None, spacing=0, align="left")

        for index, legend in enumerate(legends):
            x1, y1 = (text_offset_x, text_offset_y + line_height*len(texts)+line_height * index)
            x2, y2 = (x1+20, y1)
            xy = [(x1, y1), (x2, y2)]
            img1.line(xy, fill=legend[0], width=5)

            text_xy = (x2 + 10, y2)
            img1.text(text_xy, legend[1], fill="black", font=None, anchor=None, spacing=0, align="left")

        # The last drawn number
        last_number = draws[wining_draw]
        # All the drawn numbers till the board wins including the wining draw
        drawn_numbers = draws[:wining_draw + 1]

        for row in range(4, -1, -1):
            for col in range(cols):
                x1 = offset_left + col_width * row
                y1 = offset_top + row_height * col + title_height
                x2 = x1 + col_width
                y2 = y1 + row_height
                img1.rectangle([(x1, y1), (x2, y2)], fill=None, outline="black")
                text_xy = (x1 + 10, y1 + 10)
                text = str(self.board[col, row]).zfill(2)
                if self.board[col, row] == last_number:
                    text_color = "blue"
                elif self.board[col, row] in drawn_numbers:
                    text_color = "orange"
                else:
                    text_color = "gray"

                img1.text(text_xy, text, fill=text_color, font=None, anchor=None, spacing=0, align="left")
        img_name = str(self.id)+'.png'
        img.save('output/board/'+str(self.id)+'.png')
        return img_name
