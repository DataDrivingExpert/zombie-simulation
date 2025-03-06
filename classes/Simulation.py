# Classes
from classes.entities.Human import Human
from classes.entities.Zombie import Zombie
from classes.entities.NPC import NPC
from classes.infrastructure.Location import Location
from classes.infrastructure.Building import Building
# Data types
from dataTypes.common import (
    simulationStates, 
    mapOptions,
    summaryOptions
    )
# Errors
from exceptions.GetMapOptionError import GetMapOptionError
from exceptions.DeadNPCError import DeadNPCError
# Modules
import random
import numpy as np
# Local modules
from utils.common import inRange

class Simulation(object):

    """
    This is the orchestator of the `Simulation`.
    Attributes:
        n_floors(int): Number of `Floor` to include in the building of simulation's
        n_rooms(int): Number of `Room` to create in each Floor
        n_humans(int = 10): Number of NPC of type `Human` to generate in the `Simulation`.
        turn(int=0): The current turn of the `Simulation`.
        state(simulationStates='created'): The current state of the `Simulation`.

    """

    def __init__(self, n_floors:int, n_rooms:int, n_humans:int=10):
        self.__n_floors = n_floors
        self.__n_rooms = n_rooms
        self.__n_humans = n_humans

        self.__shift :int = 0
        self.__state :simulationStates = 'created'
        self.__building: Building | None = None

        self.__locations :tuple[Location,...] | None = None
        self.__npc :list[NPC] = []
        self.__map :np.matrix = np.matrix("")

    # Getters and Setters
    def getShift(self) -> int:
        """
        Returns the current shift number of the `Simulation`.
        """
        return self.__shift
    
    def getState(self) -> simulationStates:
        """
        Getter for the state of the `Simulation`.
        """
        return self.__state

    def setState(self, newState:simulationStates):
        """
        Setter for the state of the `Simulation`.
        """
        self.__state = newState
        pass

    def getSurvivors(self) -> int:
        """
        Returns how many Humans are still alive within the simulation.
        """
        return len([human for human in self.__npc if type(human.getInstance()) is Human and human.isAlive()])
    
    def getZombies(self) -> int:
        """
        Returns how many Zombies are in the current session.
        """
        return len([zombie for zombie in self.__npc if type(zombie.getInstance()) is Zombie and zombie.isAlive()])
    
    def getLocations(self, astype:str|Location = Location) -> tuple[Location,...]:
        if astype == str:
            return [str(loc) for loc in self.__locations]
        else:
            return self.__locations 

    def getMap(self, mode:mapOptions) -> np.matrix | list[str]:
        """
        Show the Map of Locations in the adjacency matrix.
        Params:
            mode(mapOptions): The mode of the function will determine the format of the result.

        Returns:
            result(np.matrix | list[str]): the result depends on the selected mode.
        """
        if mode == "raw":
            return self.__map
        elif mode == "beauty":
            result :list[str] = []
            for index in range(self.__map.shape[0]):
                npc = self.__npc[index]
                roomIndex= int(np.nonzero(self.__map[index,:].getA1())[0])
                npc_location = self.__locations[roomIndex]
                result.append(f"{npc} is at {npc_location.getRoom()}")
            return result
        else:
            raise GetMapOptionError(f"Option \"{mode}\" it is not recognized")
        
    # Class Methods
    def getSummary(self, mode:summaryOptions='production') -> dict:
        """
        Display a summary with the main information about the `Simulation`.
        Returns:
            result(dict): Python's dictionary with the info.
        """
        if mode == 'debug':
            return {
                "state": self.getState(),
                "turn": self.getShift(),
                "scenario": self.__building,
                "survivors": self.getSurvivors(),
                "zombies": self.getZombies(),
                "map_of_coordinates": self.getMap(mode='raw')
            }
        elif mode == 'production':
            return {
                "state": self.getState(),
                "turn": self.getShift(),
                "scenario": self.__building,
                "survivors": self.getSurvivors(),
                "zombies": self.getZombies(),
            }
        else:
            raise
    
    def nextShift(self):
        """
        Move forward in the `Simulation` one shift.
        """
        self.__shift += 1
        self.__state = 'playing'
        pass

    def whereIs(self, npcId:int) -> Location:
        """
        Find the Location instance where the indicated NPC at.
        Params:
            npcId(int): Identification number of the NPC to search.
        Returns:
            loc(Location): Location object where NPC at.
        """
        # Getting the 'npcId' locations row  
        coordinates = self.__map[npcId, : ].getA1()
        # Gathering the index where NPC is located.
        roomIndex = np.flatnonzero(coordinates)
        assert roomIndex.size == 1, "The NPC can't be at two locations at the same time."
        # Returning the location where the NPC is at. 
        return self.__locations[int(roomIndex[0])]

    def whoIs(self, locId:int) -> tuple[NPC,...]:
        """
        Show all NPCs at the indicated Location
        Params:
            locId(int): Identification number of the Location of interest.
        Returns:
            result(tuple[NPC,...]): tuple of NPCs founded at the Location.
        """
        print("debug message: locId = ",locId)
        # Getting the specific column associated to the Location.
        roomSelected = self.__map[:,locId].getA1()
        print("debug message: roomSelected = ",roomSelected)
        # Gathering the indexes of NPCs at the Location.
        npc_ids = np.flatnonzero(roomSelected)
        print("debug message: npc_ids = ",npc_ids)
        # Saving the NPC instances temporally
        result :list[NPC] = []
        if npc_ids.size != 0:
            print("El bucle a continuación".center(100, "*"))
            for _id in npc_ids:
                print("_id = ", _id)
                npc :NPC = self.__npc[_id]
                if npc.isAlive():
                    print("Si, esta vivo")
                    result.append(self.__npc[_id])
            # Returning the tuple with the NPCs founded
            return tuple(result)
        else:
            return tuple()
   
    def build_scenario(self):
        """
        This private procedure generate the scenario of the `Simulation`.
        """
        if self.__building is None:
            # Defining new objects instances

            # Creating a new Building...
            self.__building = Building(n_floors=self.__n_floors, n_rooms=self.__n_rooms)
            # Saving characters temporally
            temp :list[Human|Zombie]= []
            # Creating new Survivors
            for _ in range(self.__n_humans):
                temp.append(Human())
            # Creating zombies
            for _ in range(random.randint(a=2, b=5)):
                temp.append(Zombie())

            # Creating map of coordinates
            self.__map = np.asmatrix(np.zeros(
                shape=(
                    len(temp), # each row represents a NPC
                    self.__building.getTotalOfRooms() # each column represents a Room
                    )
                ))

            # Identifying Rooms
            roomIndex = 0
            temp_locations :list[Location] = []
            for floor in self.__building.floors:
                for room in floor.getRooms():
                    temp_locations.append(Location(locId=roomIndex, loc=room))
                    roomIndex += 1
            # Assigning Locations
            self.__locations = tuple(temp_locations)

            # Identifying and Placing NPCs
            for index, entity in enumerate(temp):
                self.__npc.append(NPC(npcId=index, npc=entity)) # Adding a label to NPC
                # Placing NPCs
                if type(entity) is Human: # Humans spawn in random Rooms of the Building
                    self.__map[index, random.randint(a=0, b=(self.__building.getTotalOfRooms() - 1))] = 1
                    continue
                else:
                    # Zombies only spawn at first `Floor` and Rooms. Then, they can move on forward.
                    self.__map[index, 0] = 1 
                    continue

        pass    

    # Class intern methods
    def __moveNpc(self,npc:NPC):
        """
        Movement logic for the `NPC` within the `Simulation`
        Params:
            npc(NPC): `NPC` instance to move it.
        """
        # Security check
        if not npc.isAlive():
            raise DeadNPCError("NPC is dead. So, it can't move or fight")
        # Get the Id of the NPC
        index = npc.getId()
        # Gathering the index of the Room where the NPC is located.
        currentLocation = int(np.flatnonzero(
            self.__map[index, : ].getA1()
            )[0])
        
        # Who is at the same Room?
        whoIs = self.whoIs(locId=currentLocation)
        # If there is nobody, don't fight.
        if len(whoIs) != 0:
            for who in whoIs:
                if who.getId() == npc.getId(): # If it is the NPC itself
                    continue                    # Then, skip this iteration

                # if it's there Zombie vs Human
                if type(who.getInstance()) != type(npc.getInstance()) and who.isAlive():
                    # Then, fight!
                    who - npc.attack() # This affects who.__hp directly because __sub__() method
                    
                else:
                    # If they belong to the same Class or it's opponent is dead.
                    # Then, do nothing. 
                    pass

        # Map limits represent the end of the building.
        map_limit = int(self.__map.shape[1] - 1)

        if type(npc.getInstance()) == Human:
            count_zombies = len([zombie for zombie in whoIs if type(zombie.getInstance()) is Human and zombie.isAlive()])
            # Humans are smart; if they see two zombies or more, then they run.
            if count_zombies >= 2:
                print("Human its running")
                self.__map[index, currentLocation] = 0
                self.__map[index, inRange(max=map_limit, value=currentLocation + 1)] = 1
            else:
                # Otherwise, they just defend their position.
                pass
        elif type(npc.getInstance()) == Zombie:
            # Zombie eats brain. Zombie just stop to eat.
            count_humans = len([human for human in whoIs if type(human.getInstance()) is Human and human.isAlive()])
            if count_humans > 0:
                print("(Zombie) Debug message: count_humans is ", count_humans, " so Zombie stay quiet")
                pass # Don't move, here is food.
            else:
                # Leave the room. Find some brains.
                print("(Zombie) Debug message: Zombie moves")
                self.__map[index, currentLocation] = 0
                self.__map[index, inRange(max=map_limit, value=currentLocation + 1)] = 1
            pass

    def __cleaner(self):
        """
        """
        if (self.getShift() + 1 ) % 2 == 0:
            print("Cleaner it's working".center(100,"*"))
            # testing
            testing = self.__npc[0]
            test_position = np.flatnonzero(self.__map[testing.getId(), : ].getA1())[0]
            roomIndex = int(test_position)
            print("testing defined")

            # Find the bodies
            dead_npcs = [npc for npc in self.__npc if not npc.isAlive()]
            print("dead_npcs: ", dead_npcs)
            for body in dead_npcs:
                # npc index in adjacency matrix
                index = body.getId()
                print("index: ",index)
                # Deleting from the map
                self.__map = np.delete(self.__map, index, axis=0)
                print("DEBUGGING MAP", self.__map)
                # Removing from the NPC List
                self.__npc.remove(body)
                # Reindexing NPCs
                for npc in self.__npc:
                    if index < npc.getId():
                        npc.reindex(newId=npc.getId() - 1)
                        pass
                    continue
                
            newPosition = np.flatnonzero(self.__map[testing.getId(), : ].getA1())[0]
            assert int(newPosition) == roomIndex, "algo ha salido mal"

            
            pass

    def __display_summary(self):
        for key, value in self.getSummary(mode='debug').items():
            if key == "map_of_coordinates":
                print(key,": \n" ,value)
            else:
                print(key,": ", value)

    def start(self):
        """
        This procedure execute the `Simulation` with the indicated attributes.
        """
        # If it is the first time that simulation starts, then Scenario will be created.
        self.build_scenario()

        if self.getShift() == 0:
            self.setState('playing')

        # while True:
        self.__cleaner()
        while self.getState() == 'playing':
            for npc in self.__npc:
                try:
                    self.__moveNpc(npc=npc)
                except DeadNPCError:
                    print(npc," is dead. So it can't move it.")
                    continue

            # self.__display_summary()

            self.setState('standby')


    def stop(self):
        """
        Stop the simulation and end the session.
        """
        self.setState('stoped')
        pass

    def restart(self):
        """
        Procedure that restart the simulation. Deleting the former instance and creating a new one.
        """
        self.setState('restart')
        pass

    def pause(self):
        """
        This procedure pause the simulation keeping the states of the current scenario.
        """
        self.setState('paused')
        pass

    def resume(self):
        """
        Resume the last stopped session.
        """
        self.setState('playing')
        pass

