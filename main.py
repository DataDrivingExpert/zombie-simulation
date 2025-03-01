from classes.infrastructure.Building import Building
from classes.infrastructure.Floor import Floor
from classes.infrastructure.Room import Room


edificio = Building(n_floors=4, n_rooms=4)
piso = Floor(1, 3)


for room in piso.rooms:
    print("habitación n° ",room.getRoomNumber(), " ocupantes: ", room.getOccupants())
    print("estado de la habitación: ", room.sensor)