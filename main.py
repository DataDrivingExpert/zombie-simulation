from classes.Simulation import Simulation
from classes.entities.Human import Human
from classes.infrastructure.Building import Building


sim = Simulation(
    n_floors=4,
    n_rooms=4,
)

sim.build_scenario()

print("Summary of the Simulation")
for key, value in sim.getSummary().items():
    if key == "map_of_coordinates":
        print(key,": \n",value)
    else:
        print(key,": ", value)

search = 9
npc_location = sim.whereIs(search)
if npc_location != None:
    print("The NPC ",search, " is at ", str(npc_location.getRoom()))