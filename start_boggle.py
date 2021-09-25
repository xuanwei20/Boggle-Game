import random


def start_boggle():
    # Step 1 create a grid
    board = make_grid()

    # Step 2 get words from user
    input_words = get_words()

    # Step 3 check words
    total_score = check_words(input_words, board)

    # Calculate total score
    print(f"\nYour total score is {total_score} points!")


def make_grid():
    letters_on_dices = {
        1: ['A', 'E', 'A', 'N', 'E', 'G'],
        2: ['A', 'H', 'S', 'P', 'C', 'O'],
        3: ['A', 'S', 'P', 'F', 'F', 'K'],
        4: ['O', 'B', 'J', 'O', 'A', 'B'],
        5: ['I', 'O', 'T', 'M', 'U', 'C'],
        6: ['R', 'Y', 'V', 'D', 'E', 'L'],
        7: ['L', 'R', 'E', 'I', 'X', 'D'],
        8: ['E', 'I', 'U', 'N', 'E', 'S'],
        9: ['W', 'N', 'G', 'E', 'E', 'H'],
        10: ['L', 'N', 'H', 'N', 'R', 'Z'],
        11: ['T', 'S', 'T', 'I', 'Y', 'D'],
        12: ['O', 'W', 'T', 'O', 'A', 'T'],
        13: ['E', 'R', 'T', 'T', 'Y', 'L'],
        14: ['T', 'O', 'E', 'S', 'S', 'I'],
        15: ['T', 'E', 'R', 'W', 'H', 'V'],
        16: ['N', 'U', 'I', 'H', 'M', 'Qu'],
        }

    grid = []
    for value in letters_on_dices.values():
        grid.append(random.choice(value))

    print(f"$ python boggle.py\n"
          f"[{grid[0]}] [{grid[1]}] [{grid[2]}] [{grid[3]}]\n"
          f"[{grid[4]}] [{grid[5]}] [{grid[6]}] [{grid[7]}]\n"
          f"[{grid[8]}] [{grid[9]}] [{grid[10]}] [{grid[11]}]\n"
          f"[{grid[12]}] [{grid[13]}] [{grid[14]}] [{grid[15]}]\n"
          f"Start typing your words! (press enter after each word and enter 'X' when done):")

    return grid


def get_words():
    words = []
    while True:
        word = input("> ").upper()
        if word == 'X':
            break
        else:
            words.append(word)
    return words


def check_words(input_words, board):
    scored_words = []
    total_score = 0

    for word in input_words:

        # Step 1 check words that have already been scored
        if word in scored_words:
            print(f"The word {word} has already been used.")
            continue

        # Step 2 check words at least three letters long
        if len(word) <= 2:
            print(f"The word {word} is too short.")
            continue

        # Step 3 check words in English
        with open('words.txt') as file:
            contents = file.read()
            if word not in contents.upper():
                print(f"The word {word} is not a word.")
                continue

        # Step 4 check words present in 4 * 4 grid
        if 'QU' in word:
            li = word.split('QU')
            if word.index('Q') == 0:
                li.remove('')
                sub_list = list(li[0])
            else:
                sub_list = list(li[0] + li[1])

            sub_list.append('QU')
            set1 = set(sub_list)
            board[15] = board[15].replace('Qu', 'QU')
            set2 = set(board)

        else:
            set1 = set(list(word))
            set2 = set(board)

        is_subset = set1.issubset(set2)
        if not is_subset:
            print(f"The word {word} is not present.")
            continue

        # Step 5  check not to use the same letter cube more than once per word
        result = check_grid_rules(board, word)
        if result is True:
            scored_words.append(word)
            word_score = calculate_points(word)
            total_score += word_score
        else:
            print(f"The word {word} is not present in the grid.")

    return total_score


def check_grid_rules(board, word):
    i = 0
    for letter in board:
        if letter == "QU":
            if letter == word[0:2]:
                result = check_adjacent(word[2:], i, [i], board)
                if result is True:
                    return True
        else:
            if letter == word[0]:
                result = check_adjacent(word[1:], i, [i], board)
                if result is True:
                    return True
        i += 1
    return False


def check_border(board_index):
    left_border = [0, 4, 8, 12]
    top_border = [0, 1, 2, 3]
    right_border = [3, 7, 11, 15]
    bottom_border = [12, 13, 14, 15]
    neighbor = ['tl', 'tc', 'tr', 'lc', 'rc', 'bl', 'bc', 'br']

    if board_index in left_border:
        neighbor.remove('tl')
        neighbor.remove('lc')
        neighbor.remove('bl')
    if board_index in top_border:
        if 'tl' in neighbor:
            neighbor.remove('tl')
        neighbor.remove('tc')
        neighbor.remove('tr')
    if board_index in right_border:
        if 'tr' in neighbor:
            neighbor.remove('tr')
        neighbor.remove('rc')
        neighbor.remove('br')
    if board_index in bottom_border:
        if 'bl' in neighbor:
            neighbor.remove('bl')
        neighbor.remove('bc')
        if 'br' in neighbor:
            neighbor.remove('br')

    return neighbor


def find_neighbor_indexes(neighbor, board_index):
    neighbor_indexes = []
    for n in neighbor:
        if n == 'tl':
            neighbor_indexes.append(board_index - 5)
        elif n == 'tc':
            neighbor_indexes.append(board_index - 4)
        elif n == 'tr':
            neighbor_indexes.append(board_index - 3)
        elif n == 'rc':
            neighbor_indexes.append(board_index + 1)
        elif n == 'lc':
            neighbor_indexes.append(board_index - 1)
        elif n == 'bl':
            neighbor_indexes.append(board_index + 3)
        elif n == 'bc':
            neighbor_indexes.append(board_index + 4)
        elif n == 'br':
            neighbor_indexes.append(board_index + 5)

    return neighbor_indexes


def check_adjacent(word_rest, board_index, used_indexes, board):
    # 1 check if the letter is on the border
    neighbor = check_border(board_index)

    # 2 find out the index of the neighbors
    neighbor_indexes = find_neighbor_indexes(neighbor, board_index)

    # 3 remove neighbors that have already been used
    for used_index in used_indexes:
        if used_index in neighbor_indexes:
            neighbor_indexes.remove(used_index)

    # 4 check if a neighbor matches first letter of word_rest
    for neighbor in neighbor_indexes:
        if board[neighbor] == "QU":
            if board[neighbor] == word_rest[0:2]:
                if len(word_rest) == 2:
                    return True
                used_indexes.append(neighbor)
                result_candidate = check_adjacent(word_rest[2:], neighbor, used_indexes, board)
                if result_candidate is True:
                    return True
        else:
            if board[neighbor] == word_rest[0]:
                if len(word_rest) == 1:
                    return True
                used_indexes.append(neighbor)
                result_candidate = check_adjacent(word_rest[1:], neighbor, used_indexes, board)
                if result_candidate is True:
                    return True

    return False


def calculate_points(word):
    if len(word) == 3 or len(word) == 4:
        score = 1
        print(f"The word {word} is worth 1 point.")
    elif len(word) == 5:
        score = 2
        print(f"The word {word} is worth 2 point.")
    elif len(word) == 6:
        score = 3
        print(f"The word {word} is worth 3 point.")
    elif len(word) == 7:
        score = 5
        print(f"The word {word} is worth 5 point.")
    else:
        score = 11
        print(f"The word {word} is worth 11 point.")

    return score


start_boggle()
