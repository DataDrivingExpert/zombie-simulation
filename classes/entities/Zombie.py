from .Human import Human


class Zombie(Human):
    """
    This class define the Zombie entity.

    Attributes:
        hp(int): Health Points of the Zombie
    """

    def __init__(self, hp:int=100, infection:float=100.0):
        super().__init__(hp, infection)

    
