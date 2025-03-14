from .Floor import Floor

class Building(object):
    """
    Allows us to simulate buildings in the zombie invasion
    """
    def __init__(self, n_floors:int, n_rooms:int):
        self.__n_floors = n_floors
        self.__n_rooms = n_rooms
        self.__floors :tuple[Floor,...] | None = None
    
    @property
    def floors(self) -> tuple[Floor,...]:
        """
        Generate the number of floors indicated by the user in n_floors attribute.
        """
        if self.__floors is None: # Only execute at start
            f_objects : list[Floor] = []
            for i in range(self.__n_floors):
                f_objects.append(Floor(i+1, self.__n_rooms))
            self.__floors = tuple(f_objects)

        return self.__floors
    
    def getTotalOfRooms(self):
        """
        Returns the total of Rooms in the Building
        """
        return self.__n_floors * self.__n_rooms
    
    
    def __str__(self):
        return f"Building have {self.__n_floors} floors and {self.__n_rooms * self.__n_floors} rooms."