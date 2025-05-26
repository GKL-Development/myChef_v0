################################## Variable, classes and functions ########################################

# Temporary hard-coded variables
firstName = 'Louis'
n = 6

# Defining user class
class User:
    def __init__(self, userName, userAllerg=None, userDislike=None, userDiet=None):
        self.userName = userName
        self.userAllerg = userAllerg
        self.userDiet= userDiet
        self.userDislike = userDislike
