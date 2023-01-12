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

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews ]
    where each item is a Python string
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['name'], entity['description'], entity['street_address'], entity['type_of_service'],
            entity['phone_number'], entity['hours_of_operation'], entity['reviews']]

class model(Model):
    def __init__(self):
        self.client = datastore.Client('premium-canyon-374605')

    def select(self):
        """
        Gets all entries from datastore
        Each entry contains: name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews
        :return: List of lists containing all entries in datastore
        """
        query = self.client.query(kind = 'Charity')
        entities = list(map(from_datastore, query.fetch()))
        entities = [x for x in entities if x != None]
        return entities

    def insert(self, name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews):
        """
        Inserts entry into datastore
        :param name: String
        :param description: String
        :param street_address: String
        :param type_of_service: String
        :param phone_number: String
        :param hours_of_operation: String
        :param reviews: String
        :return: True
        """
        key = self.client.key('Charity')
        rev = datastore.Entity(key)
        rev.update({'name':name, 'description':description, 'street_address':street_address, 'type_of_service':type_of_service,
                  'phone_number':phone_number, 'hours_of_operation':hours_of_operation, 'reviews':reviews})
        self.client.put(rev)
        return True
