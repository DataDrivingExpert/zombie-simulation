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

    def initCommands() -> None:
        """
        This procedure execute the handlers for recover the information at start.
        """
        handleLocation(location_selector.get())
        updateScenario()
        get_simulation_logs()
        pass

    def ping_sensors() -> None:
        """
        This procedure let users to ping the sensors once time per shift.
        """
        sensor_log_value.configure(state="normal")
        activity :list[str] = _simulation.get_sensors_info()
        for act in activity:
            sensor_log_value.insert("0.0", f"{act} set off!\n")
        
        sensor_log_value.configure(state="disabled")
        ping_btn.configure(state="disabled")

        sensor_display.configure(text=activity[-1])


    def get_simulation_logs() -> None:
        """
        This procedure updates the simulation activities in Dashboard
        """
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
        """
        This procedure handles the `command` call function at the `ctk.CtkOptionMenu`
        for the `Location` selection.
        Args:
            choice(str): The choice that user has taken. It's equal to the floor index.
        """
        choiceInt = locations_map[choice]
        
        nhumans, nzombies = (0,0)

        for loc in _simulation.getLocations():
            if loc.getRoom().getFloorNumber() == choiceInt:
                for entity in _simulation.whoIs(locId=loc.getId()):
                    if type(entity.getInstance()) == Human:
                        nhumans += 1
                    else:
                        nzombies += 1
                    
        humansCard_value.configure(text=str(nhumans))
        zombiesCard_value.configure(text=str(nzombies))
        #sensorsCard_value.configure(text=str(somevalue))
        
        pass

    def updateScenario() -> None:
        """
        This procedure refresh the information about the scenario at the upper right side.
        """
        scenario_display.configure(state="normal")
        scenario_display.delete("0.0", "end")
        shift, survivors, zombies = _simulation.getShift(), _simulation.getSurvivors(), _simulation.getZombies()
        data = f"shift:{shift}\nsurvivors:{survivors}\nzombies:{zombies}"
        scenario_display.insert("0.0", data)
        scenario_display.configure(state="disabled")


    def playSimulation():
        _simulation.start()
        handleLocation(location_selector.get())
        updateScenario()
        get_simulation_logs()

        # Enabling the ping button again
        ping_btn.configure(state="normal")

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
    # fsum_display = ctk.CTkTextbox(master=leftCol, font=styles.NORMAL_FONT)
    # fsum_display.grid(row=2, column=0, padx=(20,5),pady=(0,10), sticky="ew")

    #------------------------------------> Three cols CARDS <--------------------------------------
    threeCols = ctk.CTkFrame(master=leftCol)
    threeCols.grid(row=2, column=0, sticky="we", padx=(20,5),pady=(0,10))
    threeCols.grid_columnconfigure((0,1,2), weight=1)

    humansCard = ctk.CTkFrame(master=threeCols)
    humansCard.grid(row=0, column=0, padx=5, pady=5, sticky="we")
    humansCard.grid_columnconfigure(0, weight=1)

    humansCard_value = ctk.CTkLabel(master=humansCard, text="0", font=styles.HEADER_FONT)
    humansCard_value.grid(row=0, column=0, pady=5,sticky="nsew")

    humansCard_title = ctk.CTkLabel(master=humansCard, text="Humans", font=styles.NORMAL_FONT)
    humansCard_title.grid(row=1, column=0, pady=5,sticky="sew")

    zombiesCard = ctk.CTkFrame(master=threeCols)
    zombiesCard.grid(row=0, column=1, padx=5, pady=5,sticky="we")
    zombiesCard.grid_columnconfigure(0, weight=1)

    zombiesCard_value = ctk.CTkLabel(master=zombiesCard, text="0", font=styles.HEADER_FONT)
    zombiesCard_value.grid(row=0, column=0, pady=5,sticky="nsew")

    zombiesCard_title = ctk.CTkLabel(master=zombiesCard, text="Zombies", font=styles.NORMAL_FONT)
    zombiesCard_title.grid(row=1, column=0, pady=5,sticky="sew")

    sensorsCard = ctk.CTkFrame(master=threeCols)
    sensorsCard.grid(row=0, column=2, padx=5, pady=5,sticky="we")
    sensorsCard.grid_columnconfigure(0, weight=1)

    sensorsCard_value = ctk.CTkLabel(master=sensorsCard, text="0", font=styles.HEADER_FONT)
    sensorsCard_value.grid(row=0, column=0, pady=5,sticky="nsew")

    sensorsCard_title = ctk.CTkLabel(master=sensorsCard, text="sensors in alert", font=styles.NORMAL_FONT)
    sensorsCard_title.grid(row=1, column=0, pady=5,sticky="sew")

    #-------------------------------------------> Three cols  END <-------------------------------------------

    # Simulation activity

    simInfo = ctk.CTkFrame(master=leftCol)
    simInfo.grid(row=3, column=0, padx=(20,5),pady=(0,10), sticky="ew")
    simInfo.grid_columnconfigure((0,1), weight=1)
    # simInfo.grid_rowconfigure()

    simFrame = ctk.CTkFrame(master=simInfo)
    simFrame.grid(row=0, column=0, sticky="we", padx=5, pady=5)
    simFrame.grid_rowconfigure(1,weight=1)
    simFrame.grid_columnconfigure(0, weight=1)

    sim_label = ctk.CTkLabel(master=simFrame, text="Simulation activity", font=styles.NORMAL_FONT)
    sim_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    # sim TextBox
    sim_display = ctk.CTkTextbox(master=simFrame, font=styles.NORMAL_FONT)
    sim_display.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    sensorFrame = ctk.CTkFrame(master=simInfo)
    sensorFrame.grid(row=0, column=1, sticky="we", padx=5, pady=5)
    sensorFrame.grid_rowconfigure(1,weight=1)
    sensorFrame.grid_columnconfigure(0, weight=1)

    # Sensor label
    sensor_log_label = ctk.CTkLabel(master=sensorFrame, text="Sensor logs", font=styles.NORMAL_FONT)
    sensor_log_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Here should be the PhotoImage <---------------------------------------
    ping_btn = ctk.CTkButton(master=sensorFrame, text="ping", width=30, height=30, command=ping_sensors)
    ping_btn.grid(row=0, column=0, padx=15, pady=5, sticky="e")

    # Sensor values
    sensor_log_value = ctk.CTkTextbox(master=sensorFrame, font=styles.NORMAL_FONT)
    sensor_log_value.grid(row=1,column=0, padx=5, pady=5, sticky="we")


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

    scenario_display = ctk.CTkTextbox(master=rightCol, font=styles.NORMAL_FONT, state="disabled")
    scenario_display.grid(row=1, column=0, sticky="nsew",padx=5)

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