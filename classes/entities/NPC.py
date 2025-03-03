from .Human import Human
from .Zombie import Zombie


class NPC(object):

    def __init__(self, npcId:int, npc:Human | Zombie):
        self.__npcID = npcId
        self.__npc = npc

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

    def infected(self):
        """
        This procedure transform Human to Zombie, keeping it npcId.
        """
        if isinstance(self.__npc, Human):
            del self.__npc
            self.__npc = Zombie()
