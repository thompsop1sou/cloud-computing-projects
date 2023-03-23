class Model():

    def select(self, username=None, date=None):
        """
        Gets all entries from the database
        :param username: string
        :param date: string
        :return: List containing all rows of database
        """
        pass

    def insert(self, username, date, exercises):
        """
        Inserts entry into database
        :param username: string
        :param date: string
        :param exercises: list (of dictionaries)
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass
