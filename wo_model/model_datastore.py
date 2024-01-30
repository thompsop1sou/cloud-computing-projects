# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file has been modified.

from .Model import Model
from google.cloud import datastore
import json

def entity_to_dict(entity):
    """Translates a Datastore entity into a dictionary

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {'username':username, 'date':date, 'exercises':exercises}
    """
    if entity == None:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    dct = {'username':entity['username'], 'date':entity['date'], 'exercises':entity['exercises']}
    return dct

class model(Model):

    def __init__(self):
        self.client = datastore.Client('premium-canyon-374605')

    def select_user(self, username=None):
        """
        Returns user info
        :param username: string
        :return: List of dictionaries
        """
        users = []
        filters = [('exercises', '=', 'usercreated')]
        if username != None:
            filters.append(('username', '=', username))
        query = self.client.query(kind='Workout', filters=filters)
        entities_iter = query.fetch()
        users = [entity_to_dict(entity) for entity in entities_iter if entity != None]
        users = [{'username':user['username'], 'created_date':user['date']} for user in users]
        return users

    def select_workout(self, username=None, date=None):
        """
        Returns workout entries matching parameters
        Each dictionary in entries contains: username, date, exercises
        Will filter returned entries based on params username and date
        :param username: string
        :param date: string
        :return: List of dictionaries
        """
        users = []
        filters = []
        if username != None:
            filters.append(('username', '=', username))
        if date != None:
            filters.append(('date', '=', date))
        query = self.client.query(kind='Workout', filters=filters)
        entities_iter = query.fetch()
        workouts = [entity_to_dict(entity) for entity in entities_iter if entity != None]
        workouts = [workout for workout in workouts if workout['exercises'] != 'usercreated']
        return workouts

    def insert_user(self, username, date):
        """
        Inserts a new user into the database
        :param username: string
        :param date: string
        :return: True if successful
        """
        existing_user = self.select_user(username)
        if len(existing_user) == 0:
            key = self.client.key('Workout')
            user = datastore.Entity(key)
            user.update({'username':username, 'date':date, 'exercises':'usercreated'})
            self.client.put(user)
            return True
        else:
            return False

    def insert_workout(self, username, date, exercises):
        """
        Inserts entry into database
        :param username: string
        :param date: string
        :param exercises: list (of dictionaries)
        :return: True if successful
        """
        existing_workout = self.select_workout(username, date)
        if len(existing_workout) == 0:
            key = self.client.key('Workout')
            workout = datastore.Entity(key)
            workout.update({'username':username, 'date':date, 'exercises':exercises})
            self.client.put(workout)
            return True
        else:
            return False

    def delete_user(self, username):
        """
        Deletes all entries with username
        :param username: string
        :return: True if successful
        """
        filters = [('username', '=', username)]
        query = self.client.query(kind='Workout', filters=filters)
        entities = query.fetch()
        keys = [entity.key for entity in entities if entity != None]
        if len(keys) > 0:
            self.client.delete_multi(keys)
            return True
        else:
            return False

    def delete_workout(self, username, date):
        """
        Deletes all matching entries from the database
        :param username: string
        :param date: string
        :return: True if successful
        """
        filters = [('username', '=', username), ('date', '=', date)]
        query = self.client.query(kind='Workout', filters=filters)
        entities = query.fetch()
        keys = [entity.key for entity in entities if (entity != None and 'exercises' in entity.keys() and entity['exercises'] != 'usercreated')]
        if len(keys) > 0:
            self.client.delete_multi(keys)
            return True
        else:
            return False

    def update_user(self, old_username, new_username, new_created_date):
        """
        Updates username and the date that user was created
        :param old_username: string
        :param new_username: string
        :param new_created_date: string
        :return: True if successful
        """
        filters = [('username', '=', old_username)]
        query = self.client.query(kind='Workout', filters=filters)
        entities = query.fetch()
        keys = [entity.key for entity in entities if (entity != None and 'exercises' in entity.keys())]
        if len(keys) > 0:
            for key in keys:
                workout = self.client.get(key)
                if workout['exercises'] == 'usercreated':
                    workout['username'] = new_username
                    workout['date'] = new_created_date
                else:
                    workout['username'] = new_username
                self.client.put(workout)
            return True
        else:
            return False

    def update_workout(self, username, old_date, new_date, new_exercises=None):
        """
        Updates entries matching username and old_date with the new info
        :param username: string
        :param date: string
        :param new_username: string
        :param new_date: string
        :param new_exercises: list (of dictionaries)
        :return: True if successful
        """
        filters = [('username', '=', username), ('date', '=', old_date)]
        query = self.client.query(kind='Workout')
        entities = query.fetch()
        keys = [entity.key for entity in entities if (entity != None and 'exercises' in entity.keys() and entity['exercises'] != 'usercreated' and entity['date'] == old_date)]
        if len(keys) > 0:
            workout = self.client.get(keys[0])
            workout['date'] = new_date
            if new_exercises != None:
                workout['exercises'] = new_exercises
            self.client.put(workout)
            return True
        else:
            return False