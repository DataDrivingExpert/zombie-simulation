from .Floor import Floor

class Building(object):
    """
    Allows us to simulate buildings in the zombie invasion
    """
    def __init__(self, n_floors:int, n_rooms:int, floors: tuple[Floor] | None = None):
        self.__n_floors = n_floors
        self.__n_rooms = n_rooms
        self.__floors = floors
    
    @property
    def floors(self):
        """
        Generate the number of floors indicated by the user in n_floors attribute.
        """
        if self.__floors is None: # Only execute at start
            f_objects : list[Floor] = []
            for i in range(self.__n_floors):
                f_objects.append(Floor(i+1, self.__n_rooms))
            self.__floors = tuple(f_objects)

        return self.__floors