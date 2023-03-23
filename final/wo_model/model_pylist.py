"""
Python list model
"""
from .Model import Model

class model(Model):

    def __init__(self):
        self.entries = []

    def select(self, username=None, date=None):
        """
        Returns entries list of dictionaries
        Each dictionary in entries contains: username, date, exercises
        Will filter returned entries based on params username and date
        :return: List of dictionaries
        """
        selected = self.entries.copy()
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

    def insert(self, username, date, exercises):
        """
        Appends a new list of values representing a new workout
        :param username: string
        :param date: string
        :param exercises: list (of dictionaries)
        :return: True
        """
        entry = {'username':username, 'date':date, 'exercises':exercises}
        self.entries.append(entry)
        return True
