from Room import Room


class Floor(object):
    """
    Represents a group of rooms in a specific building
    """
    def __init__(self, floor_number:int, n_rooms:int):
        self.__floor_number = floor_number
        self.__n_rooms = n_rooms
        self.__rooms = None

    @property
    def rooms(self):
        if self.__rooms is None:
            with self.__n_rooms as num:
                if num is not None:
                    r_objects = []
                    for i in range(num):
                        r_objects.append(Room(i))
                    self.__rooms = set(r_objects)
        return self.__rooms
    
    def getFloorNumber(self):
        """
        Returns the identification number of the Floor
        """
        return self.__floor_number

    def getNumerOfRooms(self):
        """
        Returns how many Rooms exists in the current Floor.
        """
        return self.__n_rooms