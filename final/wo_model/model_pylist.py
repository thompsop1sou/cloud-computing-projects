"""
Python list model
"""
from .Model import Model

class model(Model):

    def __init__(self):
        self.entries = []

    def select_user(self, username=None):
        """
        Returns list of users info
        :param username: string
        :return: list of dictionaries
        """
        users = []
        for entry in self.entries:
            if entry['exercises'] == 'usercreated' and (username == None or entry['username'] == username):
                users.append({'username':entry['username'], 'created_date':entry['date']})
        return users

    def select_workout(self, username=None, date=None):
        """
        Returns workout entries matching parameters
        Each dictionary in entries contains: username, date, exercises
        Will filter returned entries based on params username and date
        :return: List of dictionaries
        """
        selected = [entry for entry in self.entries if entry['exercises'] != 'usercreated']
        if username != None:
            index = 0
            while index < len(selected):
                if selected[index]['username'] != username:
                    selected.pop(index)
                else:
                    index = index + 1
        if date != None:
            index = 0
            while index < len(selected):
                if selected[index]['date'] != date:
                    selected.pop(index)
                else:
                    index = index + 1
        return selected

    def insert_user(self, username, date):
        """
        Inserts a new user into the database
        :param username: string
        :param date: string
        :return: True
        """
        new_entry = {'username':username, 'date':date, 'exercises':'usercreated'}
        if username in [entry['username'] for entry in self.entries]:
            return False
        self.entries.append(new_entry)
        return True

    def insert_workout(self, username, date, exercises):
        """
        Appends a new list of values representing a new workout
        Ensures that there does not already exist an entry with a matching username and date
        :param username: string
        :param date: string
        :param exercises: list (of dictionaries)
        :return: True if workout successfully inserted
        """
        new_entry = {'username':username, 'date':date, 'exercises':exercises}
        for entry in self.entries:
            if new_entry['username'] == entry['username'] and new_entry['date'] == entry['date'] and entry['exercises'] != 'usercreated':
                return False
        self.entries.append(new_entry)
        return True

    def delete_user(self, username):
        """
        Deletes all entries with username
        :param username: string
        :return: True
        """
        index = 0
        while index < len(self.entries):
            if self.entries[index]['username'] == username:
                del self.entries[index]
            else:
                index = index + 1
        return True

    def delete_workout(self, username, date):
        """
        Deletes all matching entries from the database
        :param username: string
        :param date: string
        :return: True
        """
        index = 0
        while index < len(self.entries):
            if self.entries[index]['username'] == username and self.entries[index]['date'] == date and self.entries[index]['exercises'] != 'usercreated':
                del self.entries[index]
            else:
                index = index + 1
        return True

    def update_user(self, old_username, new_username, new_created_date):
        """
        Updates username and the date that user was created
        :param old_username: string
        :param new_username: string
        :param new_created_date: string
        :return: True if successful
        """
        if old_username != new_username and new_username in [entry['username'] for entry in self.entries]:
            return False
        else:
            for i in range(len(self.entries)):
                if self.entries[i]['username'] == old_username:
                    print('Found a matching entry')
                    self.entries[i]['username'] = new_username
                    print('{} changed to {}'.format(old_username, self.entries[i]['username']))
                    if self.entries[i]['exercises'] == 'usercreated':
                        self.entries[i]['date'] = new_created_date
            print(self.entries)
            return True

    def update_workout(self, username, old_date, new_date, new_exercises=None):
        """
        Updates entries matching username and old_date with the new info
        :param username: string
        :param old_date: string
        :param new_date: string
        :param new_exercises: list (of dictionaries)
        :return: True if successful
        """
        for i in range(len(self.entries)):
            if self.entries[i]['username'] == username and self.entries[i]['date'] == old_date and self.entries[i]['exercises'] != 'usercreated':
                self.entries[i]['date'] = new_date
                if new_exercises != None:
                    self.entries[i]['exercises'] = new_exercises