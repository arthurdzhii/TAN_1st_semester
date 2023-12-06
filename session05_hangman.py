# HANGMAN
# source: https://github.com/prateekiiest/Code-Sleep-Python/tree/master/Code-Sleep-Python/Hangman

from hangman_class import Hangman       # importing the Hangman class and methods from a module without an alias
from userdata_class import UserData as ud     # importing UserData class with an alias
import time     # for time used to guess to be stored in userdata
import datetime     # for current timestamp

exam_hangman = Hangman()        # instantiating an object of the Hangman class
current_player = ud()       # instantiating an object of the UserData class

WORD = exam_hangman.pick_random_word()      # a method for the object is called and the return value is saved in a variable

# creates a set containing the letters of WORD
letters_to_guess = set(WORD)        # built-in function that creates a set from the letters in the variable that is used as an argument
# tuple doesnt work here, because letters cant be removed from it (immutable) and lists can have duplicate items, so they are more difficult to remove later

# creates an empty set
correct_letters_guessed = set()     # same built-in function as earlier
incorrect_letters_guessed = set()
# since the classic order for hangman game takes 8 lost chances to hang the man
num_guesses = 8     # counter to be modified later


print("Welcome to Hangman!")
username = input("Pick a username: ")       # ask the player to choose a username, to be stored later
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")     # stores the current time in a datetime object, except seconds and milliseconds with the .strftime() method
start_time = time.time()        # timestamp when the game was started, used to calculate how long it took the player

while (len(letters_to_guess) > 0) and num_guesses > 0:      # while loop will run until this condition is True
    guess = exam_hangman.ask_user_for_next_letter()     # method from the module is called and returned value stored in variable

    # check if we already guessed that
    # letter
    if guess in correct_letters_guessed or guess in incorrect_letters_guessed:
            # print out a message
        print("You already guessed that letter.")
        continue        # statement continue skips the rest of the code in the loop for the current iteration

    # if the guess was correct
    if guess in letters_to_guess:
        # update the letters_to_guess
        letters_to_guess.remove(guess)      # removes letter from the set. remove() method removes the first item with the specified value
        # update the correct letters guessed
        correct_letters_guessed.add(guess)      # .add() method adds an element to the set
    else:
        incorrect_letters_guessed.add(guess)
        # only update the number of guesses
        # if you guess incorrectly
        num_guesses -= 1        # 1 is subtracted from the counter

    word_string = exam_hangman.generate_word_string(WORD, correct_letters_guessed)      # a method is called, with the arguments of the random word and correct letters
    print(word_string)      # variable is printed, showing correctly guessed letters and blank spaces
    print("You have {} guesses left".format(num_guesses))       # .format() method inserts the value in the {} within the string
    exam_hangman.draw_hangman(num_guesses)      # method is called with the number of guesses as an argument

# tell the user whether they have won or lost
# while loop has ended
stop_time = time.time()     # timestamp for when the game was completed
time_used = int(stop_time-start_time)        # calculation of how long the game took, rounded to full seconds
guesses_used = 8-num_guesses        # calculation of how many guesses the player used

if num_guesses > 0:     # no more letters to guess
    print("Congratulations! You correctly guessed the word {}".format(WORD))
    result = "W"
else:       # no more guesses
    print("Sorry, you lost! Your word was {}".format(WORD))
    result = "L"

current_player.save_data(username, timestamp, guesses_used, time_used, result)      # method of the UserData class is called and statistics are saved in a file

see_stats = input("Would you like to see the statistics from your games? Y/N: ").upper()        # ask if the player wants to see their stats
if see_stats == "Y":        # condition from previous input has to be met
    current_player.read_data(username)      # method is called to read and display data
else:
    print("Thank you for playing the hangman!")     # exit message