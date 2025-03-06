from ..technologies.Sensor import Sensor

class Room(object):
    """
    Represents a single room in a specific floor. At each room of the building, it is one
    sensor that communicate the state of the room.
    """
    def __init__(self, room_number:int, floor:int, occupants:int = 0):
        self.__room_number = room_number
        self.__occupants = occupants
        self.__sensor = Sensor(f'F{floor}R{room_number}')

        self.__floor = floor

    @property
    def sensor(self):
        return self.__sensor.checkActivity(self.getOccupants())

    def getRoomNumber(self):
        """
        Returns the identification number of the room
        """
        return self.__room_number
    
    def getFloorNumber(self):
        return self.__floor
    
    def getOccupants(self):
        """
        Returns the number of the occupants in the room
        """
        return self.__occupants
    
    def __str__(self):
        return f"Floor {self.__floor} Room {self.__room_number}"
        
    