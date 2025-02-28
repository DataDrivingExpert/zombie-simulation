from Floor import Floor

class Building(object):
    """
    Allows us to simulate buildings in the zombie invasion
    """
    def __init__(self, n_floors:int, n_rooms:int):
        self.__n_floors = n_floors
        self.__n_rooms = n_rooms
        self.__floors = None
    
    @property
    def floors(self):
        """
        Generate the number of floors indicated by the user in n_floors attribute.
        """
        if self.__floors is None: # Only execute at start
            with self.__n_floors as num: # 'with' allows us to define a namespace that
                                         # it will be detroyed when the process has finished
                if num is not None and self.__n_rooms is not None:
                    f_objects = [] # This list will save the floor objects temporally
                    for i in range(num):
                        f_objects.append(Floor(i+1, self.__n_rooms))
                    self.__floors = set(f_objects) # A set is more efficient than a list

        return self.__floors