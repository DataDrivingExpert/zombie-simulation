# Modules
import tkinter as tk
import customtkinter as ctk
import time
# Classes
from classes.Simulation import Simulation
from classes.entities.NPC import NPC
from classes.entities.Human import Human
# Global config
from gui.globalConfig import styles

# Setting global appearance
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

def dashboard(simulation_details:tuple[int,int,int]):

    # ---------------------------> Comands <------------------------------------
    def example():
        pass

    def initCommands():
        handleLocation(location_selector.get())
        get_simulation_logs()

    def get_simulation_logs():
        logs :list[str] = _simulation.get_log()
        logs.reverse()
        if type(logs) != None and len(logs) != 0:
            sim_display.configure(state="normal")
            sim_display.delete("0.0","end")
            history = ""
            for line in logs:
                history += f"{line}\n"

            sim_display.insert("0.0", history)
            sim_display.configure(state="disabled")
            pass
        else:
            pass

    def handleLocation(choice) -> None:
        fsum_display.delete("0.0", "end")
        result = "entities at floor:\n"
        
        choiceInt = locations_map[choice]
        
        nhumans, nzombies = (0,0)

        for loc in _simulation.getLocations():
            if loc.getRoom().getFloorNumber() == choiceInt:
                for entity in _simulation.whoIs(locId=loc.getId()):
                    if type(entity.getInstance()) == Human:
                        nhumans += 1
                    else:
                        nzombies += 1
                    

        result += f"\tHumans alive: {str(nhumans)}\n\tZombies: {str(nzombies)}\n"
        fsum_display.insert("0.0", result)
        pass


    def playSimulation():
        _simulation.start()
        handleLocation(location_selector.get())
        get_simulation_logs()

    # --------------------------------------------------------------------------

    _floors, _rooms, _humans = simulation_details
    _simulation = Simulation(
        n_floors=_floors,
        n_rooms=_rooms,
        n_humans=_humans
    )
    _simulation.build_scenario()
    time.sleep(0.700)
    print(_simulation.getMap('raw'))


    locations_map :dict[str, int]= dict()
    for floor in range(_floors):
        locations_map[f"floor {floor+1}"] = floor
    
    # --------------------------------------------------------------------------
    # root define the base.
    root = ctk.CTk()
    root.title("Simulation/dashboard")
    root.geometry("1080x720+0+0")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # frame define the Layout
    frame = ctk.CTkScrollableFrame(master=root, height=710)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(master=frame, text="Dashboard", font=styles.HEADER_FONT)
    title.grid(row=0, column=0, padx=5,pady=20, sticky="w")

    # colsLayout let us divide the UI in two columns
    colsLayout = ctk.CTkFrame(master=frame,)
    colsLayout.grid(row=1, column=0, sticky="nsew")
    colsLayout.grid_columnconfigure((0), weight=1)

    # -----------------------> LEFT COLUMN <-----------------------------
    # Left col in colsLayout
    leftCol = ctk.CTkFrame(master=colsLayout)
    leftCol.grid(row=0, column=0, padx=(5,0),pady=10, sticky="ew")
    leftCol.grid_columnconfigure(0, weight=1)

    # This is inside leftCol
    location = ctk.CTkFrame(master=leftCol)
    location.grid(row=0, column=0, pady=10,padx=(20,5),sticky="ew")
    location.grid_columnconfigure((0,1), weight=1)

    # This is inside leftCol and location
    location_label = ctk.CTkLabel(master=location, text="Location", font=styles.NORMAL_FONT)
    location_label.grid(row=0, column=0, pady=10,padx=10)

    # This is inside leftCol and location ------------------------------------------------------------------------------------------
    location_var = tk.StringVar(value="floor 1")
    location_selector = ctk.CTkOptionMenu(
        master=location, 
        font=styles.NORMAL_FONT,
        values=[key for key in locations_map.keys()], 
        variable=location_var,
        command=handleLocation
        )
    location_selector.grid(row=0,column=1, pady=10,padx=10)


    # --------------------> fsum: Floor summary <---------------------
    # This is inside leftCol
    fsum_label = ctk.CTkLabel(master=leftCol,text="Floor Summary", font=styles.NORMAL_FONT)
    fsum_label.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

    # fsum TextBox
    fsum_display = ctk.CTkTextbox(master=leftCol, font=styles.NORMAL_FONT)
    fsum_display.grid(row=2, column=0, padx=(20,5),pady=(0,10), sticky="ew")

    # Simulation activity

    simInfo = ctk.CTkFrame(master=leftCol)
    simInfo.grid(row=3, column=0, padx=(20,5),pady=(0,10), sticky="ew")
    simInfo.grid_columnconfigure((0,1), weight=1)
    # simInfo.grid_rowconfigure()

    sim_label = ctk.CTkLabel(master=simInfo, text="Simulation activity", font=styles.NORMAL_FONT)
    sim_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    sensor_log_label = ctk.CTkLabel(master=simInfo, text="Sensor logs", font=styles.NORMAL_FONT)
    sensor_log_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # sim TextBox
    sim_display = ctk.CTkTextbox(master=simInfo, font=styles.NORMAL_FONT)
    sim_display.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    sensor_log = ctk.CTkTextbox(master=simInfo, font=styles.NORMAL_FONT)
    sensor_log.grid(row=1,column=1, padx=5, pady=5, sticky="we")


    # ---------------------------> RIGHT COLUMN <----------------------------
    # Right column in colsLayout
    rightCol = ctk.CTkFrame(master=colsLayout)
    rightCol.grid(row=0, column=1, padx=(5,10), pady=10, sticky="nsew")
    rightCol.grid_columnconfigure(0, weight=1)
    rightCol.grid_rowconfigure(1, weight=1)
    rightCol.grid_rowconfigure(3, weight=2)

    #------------------------> Scenario group <------------------------------
    scenario_label = ctk.CTkLabel(master=rightCol, text="Scenario", font=styles.NORMAL_FONT)
    scenario_label.grid(row=0, column=0, sticky="nw", padx=5)

    SCENARIO_EXAMPLE = """ turn: 0\n survivors alive: 10\n zombies alive: 5\n """

    scenario_value = tk.StringVar(value=SCENARIO_EXAMPLE)

    scenario_display = ctk.CTkTextbox(master=rightCol, font=styles.NORMAL_FONT)
    scenario_display.grid(row=1, column=0, sticky="nsew",padx=5)
    scenario_display.insert("0.0", scenario_value.get())

    # Last Sensor triggered
    # ---------------------------> Sensor group <-------------------------------
    sensor_label = ctk.CTkLabel(master=rightCol, text="Last Sensor Triggered", font=styles.NORMAL_FONT)
    sensor_label.grid(row=2, column=0, sticky="nw", padx=5)

    sensor_value = tk.StringVar()

    sensorCard = ctk.CTkFrame(master=rightCol)
    sensorCard.grid(row=3, column=0, sticky="nsew",padx=5, pady=5)
    sensorCard.grid_columnconfigure(0, weight=1)
    sensorCard.grid_rowconfigure(0, weight=1)

    sensor_display = ctk.CTkLabel(master=sensorCard, text="Room 3 at Floor 2", font=("Roboto", 20))
    sensor_display.grid(row=0, column=0, sticky="nsew",)

    # ---------------------------> Controls <-----------------------------------
    controls = ctk.CTkFrame(master=frame)
    controls.grid(row=2, column=0, pady=(10, 5), padx=10)
    controls.grid_columnconfigure((0,1,2,3), weight=1)


        

    play = ctk.CTkButton(master=controls, text="next", font=styles.NORMAL_FONT, command=playSimulation) # Agregar command
    play.grid(row=0, column=0, padx=5, pady=5)

    stop = ctk.CTkButton(master=controls, text="stop",  font=styles.NORMAL_FONT, command=example) # Agregar command
    stop.grid(row=0, column=1, padx=5, pady=5)

    restart = ctk.CTkButton(master=controls, text="restart", font=styles.NORMAL_FONT,command=example) # Agregar command
    restart.grid(row=0, column=2, padx=5, pady=5)

    save = ctk.CTkButton(master=controls, text="save", font=styles.NORMAL_FONT,command=example) # Agregar command
    save.grid(row=0, column=3, padx=5, pady=5)

    # ---------------------------------------- > INIT COMMAND CALL <-------------------------------------------
    initCommands()

    root.mainloop()




if __name__ == "__main__":
    dashboard()