from .Room import Room

class Location(object):

    def __init__(self, locId:int, loc:Room):
        self.__locId = locId
        self.__loc = loc

    def getId(self) -> int:
        """
        Returns the identification number of the Location.
        """
        return self.__locId
    
    def getRoom(self) -> Room:
        """
        Returns the Room instance associated to Location.
        """
        return self.__loc
    
    def __str__(self):
        return f"{self.getRoom()}"
    