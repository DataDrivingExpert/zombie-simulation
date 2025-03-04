# Classes
from classes.entities.Human import Human
from classes.entities.Zombie import Zombie
from classes.entities.NPC import NPC
from classes.infrastructure.Location import Location
from classes.infrastructure.Building import Building
# Data types
from dataTypes.common import simulationStates, mapOptions
# Errors
from exceptions.GetMapOptionError import GetMapOptionError
# Modules
import random
import numpy as np

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
        return len([human for human in self.__npc if type(human.getInstance()) is Human])
    
    def getZombies(self) -> int:
        """
        Returns how many Zombies are in the current session.
        """
        return len([zombie for zombie in self.__npc if type(zombie.getInstance()) is Zombie])
    
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
    def getSummary(self) -> dict:
        """
        Display a summary with the main information about the `Simulation`.
        Returns:
            result(dict): Python's dictionary with the info.
        """
        return {
            "state": self.getState(),
            "turn": self.getShift(),
            "scenario": self.__building,
            "survivors": self.getSurvivors(),
            "zombies": self.getZombies(),
            "map_of_coordinates": self.getMap(mode="beauty")
        }
    
    def nextTurn(self):
        """
        Move forward in the `Simulation` one Turn.
        """
        self.__shift += 1
        self.__state = 'standby'
        pass

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
            for _ in range(random.randint(a=1, b=5)):
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
        # Getting the specific column associated to the Location.
        roomSelected = self.__map[:,locId].getA1()
        # Gathering the indexes of NPCs at the Location.
        npc_ids = np.flatnonzero(roomSelected)
        # Saving the NPC instances temporally
        result :list[NPC] = []
        for _id in np.nditer(npc_ids, op_dtypes=np.dtype('int32')):
            result.append(self.__npc[_id])
        # Returning the tuple with the NPCs founded
        return tuple(result)


    def start(self):
        """
        This procedure execute the `Simulation` with the indicated attributes.
        """
        # If it is the first time that simulation starts, then Scenario will be created.
        self.__build_scenario()
        self.setState('playing')
        while self.getState() == 'playing':
            # Write here the main logic of simulation
            pass
        
        pass

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

