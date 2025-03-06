


class Human(object):
    """
    Represents to Humans within the simulation.
    The main difference between Human and Zombie, it's the infection level. 
    Human becomes in Zombie when the infection points reach the maximum value 
    or their `hp`(health points) down to zero.
    Attributes:
        hp(int): health points of the Human
        infection(float): infection points | Max value is 100.0

    """

    def __init__(self, hp:int=100, infection:float=0.0):
        self.__hp = hp
        self.__infection = infection

    def getHealthPoints(self) -> int:
        """
        """
        return self.__hp

    def getInfectionProgress(self):
        """
        This method allows Humans to check his infection progress in the IoT Sensors
        installed in each Room.
        """
        return self.__infection

    def infectionIncreases(self, infection_points):
        """
        Setter for the infection progress
        """
        self.__infection += infection_points
        
    def attack(self) -> int:
        """
        Throw a punch to the enemies at the same `Room`.
        """
        damage = 20 # All Humans make 20 points of damage
        return damage


    def __sub__(self, value):
        self.__hp -= value
        pass

    def __del__(self):
        pass