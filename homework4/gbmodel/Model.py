class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self, name, description, street_address, type_of_service, phone_number, hours_of_operation, reviews):
        """
        Inserts entry into database
        :param name: String
        :param description: String
        :param street_address: String
        :param type_of_service: String
        :param phone_number: String
        :param hours_of_operation: String
        :param reviews: String
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass
