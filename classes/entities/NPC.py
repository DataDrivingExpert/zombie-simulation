from .Human import Human
from .Zombie import Zombie


class NPC(object):

    def __init__(self, npcId:int, npc:Human | Zombie):
        self.__npcID = npcId
        self.__npc = npc

        self.__turned = False

    def getId(self) -> int:
        """
        Returns the identification number of the NPC.
        """
        return self.__npcID

    def getInstance(self) -> Human | Zombie:
        """
        Returns the instance of the entity that object belongs.
        """
        return self.__npc
    
    def isTurned(self) -> bool:
        return self.__turned
    
    def attack(self) -> int:
        """
        Returns the damage of the attack.
        """
        return self.getInstance().attack()

    def isAlive(self) -> bool:
        """
        Detects if the `self.__npc` is alive or not.
        Returns:
            result(bool): Returns **True** if it's still alive or **False** otherwise.
        """
        instance :Human|Zombie = self.getInstance()
        if type(instance) == Human:
            if instance.getHealthPoints() > 0 and instance.getInfectionProgress() <  100.0:
                # All it's OK, pass the check.
                return True
            else:
                # Ups!, Human NPC has become a Zombie  
                self.__infected()
                return True # But, it's still alive... Zombie, but alive after all.
        else:
            if instance.getHealthPoints() > 0:
                return True
            else:
                return False
            
    def reindex(self, newId:int):
        """
        """
        self.__npcID = newId

    def __infected(self):
        """
        This procedure transform `Human` to `Zombie`, keeping its `self.__npcId`.
        """
        if type(self.getInstance()) == Human:
            self.__npc = Zombie()
            self.__turned = True
        pass

    def __str__(self):
        return f"Human (id:{self.__npcID})" if type(self.__npc) == Human else f"Zombie (id:{self.__npcID})"
    
    def __sub__(self, value:int):
        self.__npc - value
        if type(self.getInstance()) == Human:
            self.__npc\
                .infectionIncreases(infection_points=value*2)
            pass
        self.isAlive()
        pass

    def __del__(self):
        del self.__npc
        
