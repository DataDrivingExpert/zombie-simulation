from classes.Simulation import Simulation
from classes.entities.Human import Human
from classes.infrastructure.Building import Building


sim = Simulation(
    n_floors=4,
    n_rooms=4,
    n_humans=5
)

sim.build_scenario()

print(sim.whereIs(npcId=0))

for npc in sim.whoIs(locId=0):
    print(npc)

# print("Summary of the Simulation")
# for key, value in sim.getSummary().items():
#     if key == "map_of_coordinates":
#         print(key, ": ")
#         for loc in value:
#             print(loc,"\n")
#     else:
#         print(key,": ", value)
