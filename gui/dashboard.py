# Modules
import tkinter as tk
import customtkinter as ctk, sys
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

def dashboard(previous:ctk.windows.ctk_tk.CTk,simulation_details:tuple[int,int,int]):

    # ---------------------------> Comands <------------------------------------

    def enable_check_room(choice="") -> None:
        """
        """
        if checkbox.get() == 1:
            room_selector.configure(state="normal")
            fsum_label.configure(text="Per Room Summary")

            floor_index :int = locations_map[location_selector.get()]
            roomIndex :int = rooms_map[room_selector.get()]

            nhumans, nzombies, nsensors = (0,0,0)

            for loc in _simulation.getLocations():
                room = loc.getRoom()
                room.checkRoom(whoIs=_simulation.whoIs(locId=loc.getId()))
                if room.getFloorNumber() == floor_index and room.getRoomNumber() == roomIndex:
                    if room.getSensorState() == 'alert':
                        nsensors += 1
                    for entity in _simulation.whoIs(locId=loc.getId()):
                        if type(entity.getInstance()) == Human:
                            nhumans += 1
                        else:
                            nzombies += 1
                        continue
                    pass
                continue

            humansCard_value.configure(text=str(nhumans))
            zombiesCard_value.configure(text=str(nzombies))
            sensorsCard_value.configure(text=str(nsensors))
            pass
        else:
            room_selector.configure(state="disabled")
            fsum_label.configure(text="Floor Summary")
            handle_location()

        pass

    def ping_sensors() -> None:
        """
        `ping_btn`'s command.
        This procedure let users to ping the sensors once time per shift.
        """
        sensor_log_value.configure(state="normal")
        activity :list[str] = _simulation.get_sensors_info()
        for act in activity:
            sensor_log_value.insert("0.0", f"{act} set off!\n")
        
        sensor_log_value.configure(state="disabled")
        ping_btn.configure(state="disabled")

        sensor_display.configure(text=activity[-1])

    def reset_sensors() -> None:
        """
        """
        # This is the Sensor logs located at left column.
        sensor_log_value.configure(state="normal")
        sensor_log_value.delete("0.0", "end")
        sensor_log_value.configure(state="disabled")   

        # This is "Last sensor Triggered" at right column.
        sensor_display.configure(text="No info yet.")

    def get_simulation_logs() -> None:
        """
        This procedure updates the simulation activities in Dashboard
        """
        logs :list[str] = _simulation.get_log()
        logs.reverse()
        if type(logs) != None and len(logs) != 0:
            sim_value.configure(state="normal")
            sim_value.delete("0.0","end")
            history = ""
            for line in logs:
                history += f"{line}\n"

            sim_value.insert("0.0", history)
            sim_value.configure(state="disabled")
            pass
        else:
            pass

    def handle_location(choice="") -> None:
        """
        This procedure handles the `command` call function at the `ctk.CtkOptionMenu`
        for the `Location` selection.
        Args:
            choice(str): The choice that user has taken. It's equal to the floor index.
        """
        choiceInt = locations_map[location_selector.get()]
        
        nhumans, nzombies, nsensors = (0,0,0)

        for loc in _simulation.getLocations():
            if loc.getRoom().getFloorNumber() == choiceInt:
                loc.getRoom().checkRoom(whoIs=_simulation.whoIs(locId=loc.getId()))
                if loc.getRoom().getSensorState() == 'alert':
                    nsensors += 1
                for entity in _simulation.whoIs(locId=loc.getId()):
                    if type(entity.getInstance()) == Human:
                        nhumans += 1
                    else:
                        nzombies += 1
                    
        humansCard_value.configure(text=str(nhumans))
        zombiesCard_value.configure(text=str(nzombies))
        sensorsCard_value.configure(text=str(nsensors))
        pass

    def update_scenery() -> None:
        """
        This procedure refresh the information about the scenery at the upper right side.
        """
        scenery_display.configure(state="normal")
        scenery_display.delete("0.0", "end")
        shift, survivors, zombies = _simulation.getShift(), _simulation.getSurvivors(), _simulation.getZombies()
        data = f"shift:{shift}\nsurvivors:{survivors}\nzombies:{zombies}"
        scenery_display.insert("0.0", data)
        scenery_display.configure(state="disabled")

    def refresh_dashboard() -> None:
        """
        This procedure refresh data about floor summary, scenery and Simulation logs. 
        it lets us to display updated info over Dashboard.
        """
        get_simulation_logs()   # Updates the Simulation logs
        update_scenery()   # Updates the scenery details

        if checkbox.get() == 1:
            enable_check_room()
        else:
            handle_location(location_selector.get()) # Updates the Floor Summary

        pass

    def play_simulation() -> None:
        _simulation.start()
        refresh_dashboard()

        # Enabling the ping button again
        ping_btn.configure(state="normal")

    def stop_simulation():
        _simulation.stop()
        root.destroy()
        previous.deiconify()

    def restart_simulation():
        _simulation.restart()
        reset_sensors() # Updates the sensor logs and last triggered.
        refresh_dashboard()
    # --------------------------------------------------------------------------

    _floors, _rooms, _humans = simulation_details
    _simulation = Simulation(
        n_floors=_floors,
        n_rooms=_rooms,
        n_humans=_humans
    )
    _simulation.build_scenery()
    time.sleep(0.700)
    

    locations_map :dict[str, int]= dict()
    for floor in range(_floors):
        locations_map[f"floor {floor+1}"] = floor+1

    rooms_map :dict[str, int]= dict()
    for room in range(_rooms):
        
        rooms_map[f"room {room+1}"] = room+1
    
    
    # --------------------------------------------------------------------------
    # root define the base.
    root = ctk.CTkToplevel(previous)
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

    # -----------------------------------------> LEFT COLUMN <-----------------------------------------------
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
        command=handle_location
        )
    location_selector.grid(row=0,column=1, pady=10,padx=10)

    checkbox = ctk.CTkCheckBox(master=location, text="check room", command=enable_check_room)
    checkbox.grid(row=0, column=2, pady=10, padx=10)

    room_var = tk.StringVar(value="room 1")
    room_selector = ctk.CTkOptionMenu(
        master=location,
        font=styles.NORMAL_FONT,
        values=[key for key in rooms_map.keys()],
        variable=room_var,
        command=enable_check_room,
        state="disabled"
        )
    room_selector.grid(row=0, column=3, pady=10, padx=10)

    # --------------------> fsum: Floor summary <---------------------
    # This is inside leftCol
    fsum_label = ctk.CTkLabel(master=leftCol,text="Floor Summary", font=styles.NORMAL_FONT)
    fsum_label.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

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
    sim_value = ctk.CTkTextbox(master=simFrame, font=styles.NORMAL_FONT)
    sim_value.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    sensorFrame = ctk.CTkFrame(master=simInfo)
    sensorFrame.grid(row=0, column=1, sticky="we", padx=5, pady=5)
    sensorFrame.grid_rowconfigure(1,weight=1)
    sensorFrame.grid_columnconfigure(0, weight=1)

    # Sensor label
    sensor_log_label = ctk.CTkLabel(master=sensorFrame, text="Sensor logs", font=styles.NORMAL_FONT)
    sensor_log_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    ping_btn = ctk.CTkButton(master=sensorFrame, text="ping", width=30, height=30, command=ping_sensors)
    ping_btn.grid(row=0, column=0, padx=15, pady=5, sticky="e")

    # Sensor values
    sensor_log_value = ctk.CTkTextbox(master=sensorFrame, font=styles.NORMAL_FONT)
    sensor_log_value.grid(row=1,column=0, padx=5, pady=5, sticky="we")


    # --------------------------------------------------> RIGHT COLUMN <-------------------------------------------
    # Right column in colsLayout
    rightCol = ctk.CTkFrame(master=colsLayout)
    rightCol.grid(row=0, column=1, padx=(5,10), pady=10, sticky="nsew")
    rightCol.grid_columnconfigure(0, weight=1)
    rightCol.grid_rowconfigure(1, weight=1)
    rightCol.grid_rowconfigure(3, weight=2)

    #------------------------> scenery group <------------------------------
    scenery_label = ctk.CTkLabel(master=rightCol, text="scenery", font=styles.NORMAL_FONT)
    scenery_label.grid(row=0, column=0, sticky="nw", padx=5)

    scenery_display = ctk.CTkTextbox(master=rightCol, font=styles.NORMAL_FONT, state="disabled")
    scenery_display.grid(row=1, column=0, sticky="nsew",padx=5)

    # Last Sensor triggered
    # ---------------------------> Sensor group <-------------------------------
    sensor_label = ctk.CTkLabel(master=rightCol, text="Last Sensor Triggered", font=styles.NORMAL_FONT)
    sensor_label.grid(row=2, column=0, sticky="nw", padx=5)

    sensor_value = tk.StringVar()

    sensorCard = ctk.CTkFrame(master=rightCol)
    sensorCard.grid(row=3, column=0, sticky="nsew",padx=5, pady=5)
    sensorCard.grid_columnconfigure(0, weight=1)
    sensorCard.grid_rowconfigure(0, weight=1)

    sensor_display = ctk.CTkLabel(master=sensorCard, text="No info yet.", font=("Roboto", 20))
    sensor_display.grid(row=0, column=0, sticky="nsew",)

    # -----------------------------------------> Controls <---------------------------------------------------------
    controls = ctk.CTkFrame(master=frame)
    controls.grid(row=2, column=0, pady=(10, 5), padx=10)
    controls.grid_columnconfigure((0,1,2,3), weight=1)


    play = ctk.CTkButton(master=controls, text="next", font=styles.NORMAL_FONT, command=play_simulation) # Agregar command
    play.grid(row=0, column=0, padx=5, pady=5)

    stop = ctk.CTkButton(master=controls, text="stop",  font=styles.NORMAL_FONT, command=stop_simulation) # Agregar command
    stop.grid(row=0, column=1, padx=5, pady=5)

    restart = ctk.CTkButton(master=controls, text="restart", font=styles.NORMAL_FONT,command=restart_simulation) # Agregar command
    restart.grid(row=0, column=2, padx=5, pady=5)

    # save = ctk.CTkButton(master=controls, text="save", font=styles.NORMAL_FONT,command=example) # Agregar command
    # save.grid(row=0, column=3, padx=5, pady=5)
    #
    #
    # -----------------------------------------> Controls END <---------------------------------------------------------

    # ---------------------------------------- > INIT COMMAND CALL <-------------------------------------------
    refresh_dashboard()
    # ----------------------------------------------------------------------------------------------------------

    def closeAll():
        root.destroy()
        previous.destroy()

    root.protocol("WM_DELETE_WINDOW", closeAll)


if __name__ == "__main__":
    dashboard()