"""
Program to keep track of the elo and rank of everybody in table tennis club through very simple data
manipulation.
:author Cameron Sprowls
:date 9/30/17
"""


class Elo:

    def __init__(self):
        print("Will never be printed")

    @staticmethod
    def main():
        # Read the data
        data = Elo.read_data()

        # Calculate the new elo with the day's matches.txt
        new_data = Elo.calculate(data)

        # Sort the newly calculated data
        sorted_data = Elo.sort_data(new_data)

        # Write the data back to a file
        Elo.wreet_data(sorted_data)

    @staticmethod
    def sort_data(data):
        sorted_data = []
        remember = Person("", 0, 0)

        while_time = len(data)
        while while_time > 0:
            highest_elo = 0
            # Find the highest elo in teh list of people
            for i in data:
                if i.get_elo() >= highest_elo:
                    highest_elo = i.get_elo()

            # Take the highest elo and put it into the new array first
            for i in data:
                if i.get_elo() == highest_elo:
                    remember = i

            sorted_data.append(remember)
            data.remove(remember)
            while_time = while_time - 1

        return sorted_data

    @staticmethod
    def calculate(old_ranking):
        """
        Calculate the new elo of based on the matches.txt of today
        :param old_ranking: data from last week / current standing, dictionary
        :return: new ratings of people
        """
        # Vars for days
        new_ranking = []
        matches = []
        difference = 0

        # Open the matches.txt file and store that into a list we can easily use
        file = open("matches.txt")
        line = file.readline()
        while line is not "":
            matches.append(line[:-1])
            line = file.readline()

        matches = Elo.convert(matches, old_ranking)

        # This... Part
        for i in old_ranking:
            end_rating = int(i.get_elo())

            for j in matches:
                # If the person didn't have a match, skip them
                if str(i.get_id()) not in j[:3] and str(i.get_id()) not in j[3:]:
                    continue

                winner = False
                favorite = False

                # If the person's id matches.txt that of the winner, they won
                if i.check_id(j[:3]):
                    winner = True

                # If beginning rating >= opponents rating, favorite = true
                for k in old_ranking:
                    if winner:
                        if k.get_id() == str(j[3:]):
                            if i.get_elo() >= k.get_elo():
                                favorite = True
                            difference = abs(int(i.get_elo()) - int(k.get_elo()))
                    else:
                        if k.get_id() == str(j[:3]):
                            if i.get_elo() >= k.get_elo():
                                favorite = True
                            difference = abs(int(i.get_elo()) - int(k.get_elo()))

                end_rating = end_rating + int(Elo.match_calculate(favorite, winner, difference))

            new_ranking.append(Person(i.get_name(), end_rating, i.get_id()))

        return new_ranking

    @staticmethod
    def match_calculate(favorite, winner, difference):
        a_index = Elo.index_from_diff(difference)
        points1 = [8,    7,   6,   5,   4,   3,   2,   2,   1,   0,   0]
        points2 = [-8, -10, -13, -16, -20, -25, -30, -35, -40, -45, -50]
        points3 = [-8,  -7,  -6,  -5,  -4,  -3,  -2,  -2,  -1,   0,   0]
        points4 = [8,   10,  13,  16,  20,  25,  30,  35,  40,  45,  50]
        if favorite and winner:
            return points1[a_index]
        if favorite and not winner:
            return points2[a_index]
        if not favorite and not winner:
            return points3[a_index]
        if not favorite and winner:
            return points4[a_index]

    @staticmethod
    def index_from_diff(difference):
        if difference <= 12:
            return 0
        if difference <= 37:
            return 1
        if difference <= 62:
            return 2
        if difference <= 87:
            return 3
        if difference <= 112:
            return 4
        if difference <= 137:
            return 5
        if difference <= 162:
            return 6
        if difference <= 187:
            return 7
        if difference <= 212:
            return 8
        if difference <= 237:
            return 9
        # Default value
        return 10

    @staticmethod
    def read_data():
        """
        Reads the data from past instances and stores it in memory
        :return: data that was read
        """
        data = []
        file = open("standings.txt")
        # Read the data into a file, store it into a Person array
        while file:
            line = file.readline()
            if line == "":
                break
            data.append(Person(line[13:], line[8:12], line[4:7]))

        return data

    @staticmethod
    def wreet_data(data):
        """
        Writes the data calculated to the files for the next run
        :param data: data that will be used to write to the file
        :return: placeholder
        """
        file = open("standings.txt", 'w')
        counter = 1
        # Write to the file, store it as I got it
        for i in data:
            if counter < 10:
                if i.get_elo() < 1000:
                    file.write("0" + str(counter) + ". " + str(i.get_id()) + " 0" + str(i.get_elo()) +
                               " " + i.get_name())
                    continue
                file.write("0" + str(counter) + ". " + str(i.get_id()) + " " + str(i.get_elo()) +
                           " " + i.get_name())
            else:
                if i.get_elo() < 1000:
                    file.write(str(counter) + ". " + str(i.get_id()) + " 0" + str(i.get_elo()) +
                               " " + i.get_name())
                    continue
                file.write(str(counter) + ". " + str(i.get_id()) + " " + str(i.get_elo()) +
                           " " + i.get_name())
            counter += 1
        return

    @staticmethod
    def convert(matches, data_to_compare):
        matches_elo = []
        for i in matches:
            space = i.find(" ")
            for j in data_to_compare:
                for k in data_to_compare:
                    if i[:space] == j.get_name()[:-1] and i[space+1:] == k.get_name()[:-1]:
                        matches_elo.append(str(j.get_id()) + str(k.get_id()))

        return matches_elo


class Person:
    name = ""
    elo = 0
    id = 0

    def __init__(self, new_name, new_elo, new_id):
        self.name = new_name
        self.elo = new_elo
        self.id = new_id

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_elo(self):
        return self.elo

    def check_id(self, id_check):
        """
        Returns true if the id passed in matches.txt the id of the person
        :param id_check: new if
        :return: True if matches.txt, else false
        """
        if self.id == id_check:
            return True
        return False

    def get_elo_by_id(self, id_to_check):
        """
        Gets the elo if the id matches.txt
        :param id_to_check: id check
        :return: elo
        """
        if id_to_check == id:
            return self.elo


Elo.main()
