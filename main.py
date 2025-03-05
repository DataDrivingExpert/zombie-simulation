from classes.Simulation import Simulation
from classes.entities.Human import Human
from classes.infrastructure.Building import Building


sim = Simulation(
    n_floors=4,
    n_rooms=4,
    n_humans=5
)

sim.start()


