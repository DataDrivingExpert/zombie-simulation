from technologies.Sensor import Sensor 

class Room(object):
    """
    Represents a single room in a specific floor. At each room of the building, it is one
    sensor that communicate the state of the room.
    """
    def __init__(self, room_number:int, occupants:int = 0):
        self.__room_number = room_number
        self.__occupants = occupants
        self.__sensor = None
        
    