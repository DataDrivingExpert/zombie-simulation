from ..technologies.Sensor import Sensor
from classes.entities.NPC import NPC

from dataTypes.common import sensorStates

class Room(object):
    """
    Represents a single room in a specific floor. At each room of the building, it is one
    sensor that communicate the state of the room.
    """
    def __init__(self, room_number:int, floor:int):
        self.__room_number = room_number
        self.__sensor = Sensor(f'Floor {floor} Room {room_number}')

        self.__floor = floor

    def checkRoom(self, whoIs:tuple[NPC,...]):
        return self.__sensor.checkActivity(whoIs)

    def getRoomNumber(self):
        """
        Returns the identification number of the room
        """
        return self.__room_number
    
    def getFloorNumber(self):
        return self.__floor
    
    def getSensorInstance(self):
        return self.__sensor
    
    def getSensorState(self) -> sensorStates:
        """
        Returns the number of the occupants in the room
        """
        return self.__sensor.getState()
    
    def __str__(self):
        return f"Floor {self.__floor} Room {self.__room_number}"
        
    