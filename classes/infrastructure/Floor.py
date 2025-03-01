from .Room import Room


class Floor(object):
    """
    Represents a group of rooms in a specific building
    """
    def __init__(self, floor_number:int, n_rooms:int, rooms: tuple[Room] | None = None):
        self.__floor_number = floor_number
        self.__n_rooms = n_rooms
        self.__rooms = rooms

    @property
    def rooms(self):
        if self.__rooms is None:
            r_objects: list[Room] = []
            for i in range(self.__n_rooms):
                r_objects.append(Room(room_number=i, floor=self.getFloorNumber()))
            self.__rooms = tuple(r_objects)
        return self.__rooms
    
    def getFloorNumber(self) -> int:
        """
        Returns the identification number of the Floor
        """
        return self.__floor_number

    def getNumerOfRooms(self) -> int:
        """
        Returns how many Rooms exists in the current Floor.
        """
        return self.__n_rooms