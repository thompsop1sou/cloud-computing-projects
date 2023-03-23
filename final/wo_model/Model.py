class Model():

    def select_user(self, username=None):
        """
        Returns user info
        :param username: string
        :return: dictionary
        """
        pass

    def select_workout(self, username=None, date=None):
        """
        Returns workout entries matching parameters
        Each dictionary in entries contains: username, date, exercises
        Will filter returned entries based on params username and date
        :param username: string
        :param date: string
        :return: List of dictionaries
        """
        pass

    def insert(self, username, date, exercises):
        """
        Inserts entry into database
        :param username: string
        :param date: string
        :param exercises: list (of dictionaries)
        :return: True
        :raises: Database errors on connection and insertion
        """
        pass

    def delete_user(self, username):
        """
        Deletes all entries with username
        :param username: string
        :return: True
        """
        pass

    def delete_workout(self, username, date):
        """
        Deletes all matching entries from the database
        :param username: string
        :param date: string
        :return: True
        """
        pass

    def update_user(self, old_username, new_username, new_created_date):
        """
        Updates username and the date that user was created
        :param old_username: string
        :param new_username: string
        :param new_created_date: string
        :return: True
        """
        pass

    def update_workout(self, username, old_date, new_date, new_exercises):
        """
        Updates entries matching username and old_date with the new info
        :param username: string
        :param date: string
        :param new_username: string
        :param new_date: string
        :param new_exercises: list (of dictionaries)
        :return: True
        """
        pass