# Data types
from dataTypes.common import simulationStates
# Classes
from classes.entities.Human import Human
from classes.entities.Zombie import Zombie
from classes.entities.NPC import NPC
from classes.infrastructure.Location import Location
from classes.infrastructure.Building import Building
# Modules
import random
import numpy as np

class Simulation(object):

    """
    This is the orchestator of the Simulation.
    Attributes:
        n_floors(int): Number of Floor to include in the building of simulation's
        n_rooms(int): Number of Room to create in each Floor
        n_humans(int = 10): Number of NPC of type Human to generate in the Simulation.
        turn(int=0): The current turn of the Simulation.
        state(simulationStates='created'): The current state of the Simulation.

    """

    def __init__(self, n_floors:int, n_rooms:int, n_humans:int=10):
        self.__n_floors = n_floors
        self.__n_rooms = n_rooms
        self.__n_humans = n_humans

        self.__turn :int = 0
        self.__state :simulationStates = 'created'
        self.__building: Building | None = None

        self.__locations :set[Location] = set()
        self.__npc :set[NPC] = set()
        self.__map :np.matrix = np.matrix("") # Matriz de adyacencia

    # Getters and Setters
    def getTurn(self) -> int:
        """
        Returns the current turn number of the Simulation.
        """
        return self.__turn
    
    def getState(self) -> simulationStates:
        """
        Getter for the state of the Simulation.
        """
        return self.__state

    def setState(self, newState:simulationStates):
        """
        Setter for the state of the Simulation.
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
    
        
    # Class Methods
    def getSummary(self) -> dict:
        return {
            "state": self.getState(),
            "turn": self.getTurn(),
            "scenario": self.__building,
            "survivors": self.getSurvivors(),
            "zombies": self.getZombies(),
            "map_of_coordinates": self.__map
        }
    
    def nextTurn(self):
        """
        Move forward in the Simulation one Turn.
        """
        self.__turn += 1
        pass

    def build_scenario(self):
        """
        This private procedure generate the scenario of the Simulation.
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
            for floor in self.__building.floors:
                for room in floor.getRooms():
                    self.__locations.add(Location(locId=roomIndex, loc=room))
                    roomIndex += 1

            # Identifying and Placing NPCs
            for index, entity in enumerate(temp):
                self.__npc.add(NPC(npcId=index, npc=entity)) # Adding a label to NPC
                # Placing NPCs
                if type(entity) is Human: # Humans spawn in random Rooms of the Building
                    self.__map[index, random.randint(a=0, b=(self.__map.shape[1] - 1))] = 1
                    continue
                else:
                    # Zombies only spawn at first Floor and Rooms. Then, they can move on forward.
                    self.__map[index, 0] = 1 
                    continue

        pass

    def whereIs(self, npcId:int) -> Location | None:
        """
        Returns the Location instance where the NPC at.
        """
        coordinates = self.__map[npcId, : ].getA1()
        roomIndex = int(np.searchsorted(coordinates, 1))
        location = (location for location in self.__locations if location.getId() == roomIndex)
        return location[0]



    def start(self):
        """
        This procedure execute the simulation with the indicated attributes.
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

