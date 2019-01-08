""" This model hadles users """

from datetime import datetime, timedelta

USERS = []

class UserModel(object):
    """ A class that maps user data """
    
    def __init__(self):
        self.users = USERS
    
    def signup(self, firstname, lastname, othername, email, phoneNumber, username, registered, isAdmin, password):
        """ Method to manipulate addition of new users """

        user = {
            "id": len(self.users) + 1,
            "firstname": firstname,
            "lastname": lastname,
            "othername": othername,
            "email": email,
            "phoneNumber": phoneNumber,
            "registered": registered,
            "isAdmin": isAdmin,
            "password": password
        }

        self.users.append(user)
        return user