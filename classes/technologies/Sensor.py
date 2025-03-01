from dataTypes.common import sensorStates

class Sensor(object):
    """
    Represents the device to monitoring the current room's situation.
    Each of this devices have a name given by their Floor and Room.
    Attributes:
            name(str): the name of the device
            state(sensorStates): the state of the place where the sensor is installed.
    For example:
        Device at the 8th room, placed at 2nd floor it will be named F2R8
    """
    def __init__(self, name:str, state:sensorStates='normal'):
        self.__name = name
        self.__state = state

    def getName(self) -> str:
        """
        Returns the name of the Sensor object.
        """
        return self.__name

    def getState(self) -> sensorStates:
        """
        Returns the current state of the Sensor object.
        """
        return self.__state

    def checkActivity(self, num_occupants:int):
        """
        Function that updates the state of Sensor instance and returns it.
        """
        if num_occupants > 0:
            self.__state = 'alert'
        else:
            self.__state = 'normal'

        return self.__state