# Class that collects and reads user data from a file
import csv      # allows to read and write to csv files


class UserData():
    """Modeling a dataset of player data"""
    def __init__(self):
        """Instantiates an object of userdata"""

    def read_data(self, username):      # parameter because it is used to find data in the file
        """Returns the player's statistics from the file when given a username"""
        results = []        # empty list to later append with results
        with open("userdata.csv", mode="r") as userdata_file:       # opens a specified csv file, mode r means read
            user_data_reader = csv.DictReader(userdata_file)        # creates a DictReader object that can read dictionaries
            for row in user_data_reader:        # row = dictionary in the userdata file
                for key, value in row.items():      # iteration through the dictionaries
                    if value == username:       # find all the games this player has played
                        results.append(row)     # append list of results of the player with all data from those games
        print("Here are the stats for each of your games:")
        for games in results:       # iterates through the results list
            print("\n")
            for key, value in games.items():        # iterates through each item (they are all dictionaries) of the list results
                print(str(key) + " : " + str(value))        # prints the results in a readable manner

    def save_data(self, username, timestamp, num_guesses, time_used, result):       # parameters from the game that need to be stored in file
        """Saves the player's username, timestamp, number of guesses, time used and if they succeeded"""
        with open("userdata.csv", mode="a", newline="") as userdata_file:       # opens the file, mode a means append, so previous data does not get overwritten
            user_data_writer = csv.DictWriter(userdata_file, delimiter=",",
                                              fieldnames=["username", "timestamp", "num_guesses", "time_used",
                                                          "result"])        # creates object of DictWriter class that can create dictionaries in a file. Delimiter is what separates the values in the file. fieldnames = keys
            user_data_writer.writerow({"username": username,
                                       "timestamp": timestamp,
                                       "num_guesses": num_guesses,
                                       "time_used": time_used,
                                       "result": result,
                                       })       # creates key-value pairs for the game data and stores it in one row of the csv file with the .writerow() method
        print("Your username and the statistics of your game have been recorded!")
