import re
from werkzeug.security import check_password_hash
from ..models.user_models import USERS


class UserValidation():
    def __init__(self):
        self.users = USERS

    def validate_password(self, password):
        exp = "^[a-zA-Z0-9@_+-.]{3,}$"
        return re.match(exp, password)

    def validate_email(self, email):
        exp = "^[\w]+[\d]?@[\w]+\.[\w]+$"
        return re.match(exp, email)

    def username_exists(self, username):
        usr = [user for user in self.users if user['username'] == username]
        if usr:
            return True
        else:
            return False

    def same_password(self, username, password):
        usr = [user for user in self.users if user['username'] == username]
        if usr:
            validate = check_password_hash(usr['password'], password)
            if validate:
                return True
            else:
                return False

    def email_exists(self, email):
        usr = [user for user in self.users if user['email'] == email]
        if usr:
            return True
        else:
            return False
