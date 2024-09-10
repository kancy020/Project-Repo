from backendFiles.LoginException import * 
from backendFiles.User import User

class Authenticator:
    userDict={}

    def fillData(self):
        #just for testing
        Authenticator.userDict["Logan"] = User("Logan","test",1234)


    def addUser(self,username, password, contactNumber):
         
        if username in self.userDict:
                raise UsernameAlreadyExists(username)
        else:
            
            if len(password)< 6:
                raise PasswordTooShort(username)
            else:
                #need to add to the database
                self.userDict[username] = User(username, password, contactNumber)

    
    def login(self,username, password):
        '''Takes username and passwork and returns the user object'''
        #Change the code to Database?
        if username in self.userDict:
            
            user=self.userDict[username] #retviing the user object to do stuff with
            
            if user.checkPassword(password)==True:
                print("you have logged in")
                
                return user
            else:
                raise InvalidPassword(username)
            
        else:
            raise InvalidUsername(username)
        
