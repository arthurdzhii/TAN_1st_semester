# Class with methods to play hangman

import random       # random package imported, randint method used in one of the class methods here


class Hangman():
    """Modeling a hangman game"""
    def __init__(self):     # self parameter refers to the object of the class itself
        """Initializes an object in the hangman class"""
        # not necessary to define any parameters for the class in this case

    def draw_hangman(self, i):      # method has one parameter besides the self
        # method to draw hangman
        graphics = ('''_____\n|/  |\n|   O\n|  /|\\\n|  / \\\n|''',
                        '''_____\n|/  |\n|   O\n|  /|\\\n|  / \\\n|''',
                        '''_____\n|/  |\n|   O\n|  /|\\\n|  /\n|''',
                        '''_____\n|/  |\n|   O\n|  /|\\\n|\n|''',
                        '''_____\n|/  |\n|   O\n|  /|\n|\n|''',
                        '''_____\n|/  |\n|   O\n|   |\n|\n|''',
                        '''_____\n|/  |\n|   O\n|\n|\n|''',
                        '''_____\n|/  |\n|\n|\n|\n|''',
                        '')       # a list of strings to draw the gallows
        print(graphics[i])      # number of guesses is an index that determines which string is printed

    def pick_random_word(self):
            # This method picks a random word from the SOWPODS dictionary.
            # open the sowpods dictionary as a text file in readable format

        with open("sowpods.txt", 'r') as f:     # sowpods.txt file is opened in reading mode and an object f is instantiated
            words = f.readlines()       # each line of the file is read and stored as an item on the list called words

            # generate a random index with the help of the random package method randint
            # -1 because len(words) is not a valid index into the list `words`, because index starts from 0
        index = random.randint(0, len(words)-1)

            # print out the word at that index
            # the .strip() function removes all trailing spaces before and after the word
        word = words[index].strip()     # no spaces in the sowpods file, but this is a good safety measure
        return word     # value is returned to the program that called the method

    def ask_user_for_next_letter(self):
        """Asks user to input their next guess"""
        letter = input("Guess your letter: ")       # built-in input function
        while len(letter) != 1:     # adding this loop so players cant enter multiple letters in the same guess
            print("One letter at a time!")
            letter = input("Guess your letter: ")       # built-in input function
        return letter.strip().upper()       # value is returned stripped and capitalized, because sowpods file is all caps

    def generate_word_string(self, word, letters_guessed):      # method has 2 parameters
        """Generates a string with correctly guessed letters and blank spaces"""
        output = []     # empty list, could also use a string and append the whitespace with each loop
        for letter in word:     # for loop iterates through a string in this case
            if letter in letters_guessed:       # see if letters in the word have already been guessed correctly
                output.append(letter.upper())      # append list with a letter that has been correctly guessed
            else:
                output.append("_")      # append list with a blank space (underscore) if letter has not been guessed yet

            # creates a string from the members of the list by using whitespace as a separator
        return " ".join(output)     # .join() method joins items of an iterable (list in this case) into a string, with a seperator


