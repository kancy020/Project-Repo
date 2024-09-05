class AuthenticationException(Exception):
    def __init__(self, username):
        super().__init__(username)
        self.username = username


class UsernameAlreadyExists(AuthenticationException):
    #make an alert relating
    pass

class PasswordTooShort(AuthenticationException):
    #make an alert relating
    pass

class InvalidUsername(AuthenticationException):
    #make an alert relating
    pass

class InvalidPassword(AuthenticationException):
    #make an alert relating
    pass