import hashlib

class User:

    def __init__(self,username: str ,password:str,contactNumber:int,homeLocations: list) -> None:
        self.__username= username
        self.__password = self._encryptPassword(password)
        self.contactNumber = contactNumber
        self.homeLocations= homeLocations
 
    def _encryptPassword(self, password):
        # Encrypt the password with the username and return the sha digest.
        hash_string = self.__username + password
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def checkPassword(self, password):
        # Returns True if the password is valid for this user, false otherwise.
        encrypted = self._encryptPassword(password)
        return encrypted == self.__password