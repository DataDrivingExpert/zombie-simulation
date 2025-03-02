from classes.Simulation import Simulation
from classes.entities.Human import Human
from classes.infrastructure.Building import Building

building = Building(n_floors=4, n_rooms=4)

for floor in building.floors:
    print("En el piso: ", floor.getFloorNumber())
    for room in floor.getRooms():
        print("Existen las habitaciones: ", room.getRoomNumber())


