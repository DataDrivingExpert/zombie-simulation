

class Sensor(object):
    """
    Represents the device to monitoring the current room's situation.
    Each of this devices have a name given by their Floor and Room.
    """
    def __init__(self, name:str, state:'alert'|'normal'='normal'):
        self.__name = name
        self.__state = state

    def getName(self):
        """
        Returns the name of the Sensor object.
        """
        return self.__name

    def getState(self):
        """
        Returns the current state of the Sensor object.
        """
        return self.__state

    def checkActivity(self, num_occupants:int):
        """
        Procedure that updates the state of Sensor instance.
        """
        if num_occupants > 0:
            self.__state = 'alert'
        else:
            self.__state = 'normal'