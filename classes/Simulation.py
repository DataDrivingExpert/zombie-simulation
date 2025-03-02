from dataTypes.common import simulationStates
from classes.entities.Human import Human
from classes.entities.Zombie import Zombie
from classes.infrastructure.Building import Building
import random

class Simulation(object):

    def __init__(self, n_floors:int, n_rooms:int, n_humans:int=10):
        self.__n_floors = n_floors
        self.__n_rooms = n_rooms
        self.__n_humans = n_humans

        self.__turn :int = 0
        self.__state :simulationStates = 'created'
        self.__survivors: set[Human] = set()
        self.__zombies: set[Zombie] = set()
        self.__building: Building | None = None

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
        return len(self.__survivors)
    
    def getZombies(self) -> int:
        """
        Returns how many Zombies are in the current session.
        """
        return len(self.__zombies)
    
        
    # Class Methods
    def getSummary(self) -> dict:
        return {
            "state": self.getState(),
            "turn": self.getTurn(),
            "scenario": self.__building,
            "survivors": self.getSurvivors(),
            "zombies": self.getZombies()
        }
    
    def nextTurn(self):
        """
        Move forward in the Simulation one Turn.
        """
        self.__turn += 1
        pass

    def __build_scenario(self):
        """
        This private procedure generate the scenario of the Simulation.
        """
        if self.__building is None:
            # Defining new objects instances
            # Creating a new Building...
            self.__building = Building(n_floors=self.__n_floors, n_rooms=self.__n_rooms)
            # Creating new Survivors
            for _ in range(self.__n_humans):
                self.__survivors.add(Human())
            # Creating zombies
            for _ in range(random.randint(a=1, b=5)):
                self.__zombies.add(Zombie())
            
        pass

    def start(self):
        """
        This procedure execute the simulation with the indicated attributes.
        """
        # If it is the first time that simulation starts, then Scenario will be created.
        self.__build_scenario()
        self.setState('playing')
        while self.getState() is 'playing':
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

