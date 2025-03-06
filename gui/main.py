# Modules
import customtkinter as ctk
import tkinter as tk
# Global configs
from gui.globalConfig import styles
# dashboard UI
from gui.dashboard import dashboard

# Setting global appearance
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

def home():
    # Root component
    root = ctk.CTk()
    root.title("Simulation/configuration")
    root.geometry("720x405")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Frame for layout
    frame = ctk.CTkFrame(master=root)

    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(master=frame, text="Zombie invasion simulator", font=("Roboto", 24))
    title.grid(row=0, column=0, pady=15)

    # UI for number of Floors selection
    nFloors = ctk.CTkFrame(master=frame)
    nFloors.grid(row=1, column=0, pady=15)
    nFloors.grid_columnconfigure((0,1,2), weight=1)

    floor_label = ctk.CTkLabel(master=nFloors, text="Floors", font=("Roboto", 12))
    floor_label.grid(row=0, column=0, padx=10, pady=10)

    floors_value = tk.IntVar(value=4)

    floor_slider = ctk.CTkSlider(nFloors, from_=1, to=10, number_of_steps=10, variable=floors_value)
    floor_slider.grid(row=0, column=1, padx=10, pady=10)

    floor_entry = ctk.CTkEntry(master=nFloors, textvariable=floors_value)
    floor_entry.configure(state="disabled")
    floor_entry.grid(row=0, column=2, padx=10, pady=10)

    # UI for number of rooms per floor
    nRooms = ctk.CTkFrame(master=frame)
    nRooms.grid(row=2, column=0, pady=15)
    nRooms.grid_columnconfigure((0,1,2), weight=1)

    room_label = ctk.CTkLabel(master=nRooms, text="Rooms", font=("Roboto", 12))
    room_label.grid(row=0, column=0, padx=10, pady=10)

    rooms_value = tk.IntVar(value=3)

    room_slider = ctk.CTkSlider(nRooms, from_=1, to=10, number_of_steps=10, variable=rooms_value)
    room_slider.grid(row=0, column=1, padx=10, pady=10)

    room_entry = ctk.CTkEntry(master=nRooms, textvariable=rooms_value)
    room_entry.configure(state="disabled")
    room_entry.grid(row=0, column=2, padx=10, pady=10)

    # UI for the number of humans selection
    nHumans = ctk.CTkFrame(master=frame)
    nHumans.grid(row=3, column=0, pady=15)
    nHumans.grid_columnconfigure((0,1,2), weight=1)

    human_label = ctk.CTkLabel(master=nHumans, text="Humans", font=("Roboto", 12))
    human_label.grid(row=0, column=0, padx=10, pady=10)

    humans_value = tk.IntVar(value=10)

    human_slider = ctk.CTkSlider(nHumans, from_=1, to=10, number_of_steps=10, variable=humans_value)
    human_slider.grid(row=0, column=1, padx=10, pady=10)

    human_entry = ctk.CTkEntry(master=nHumans, textvariable=humans_value)
    human_entry.configure(state="disabled")
    human_entry.grid(row=0, column=2, padx=10, pady=10)

    def start_simulation():
        simulation_details :tuple[int,int,int] =  (
            floors_value.get(),
            rooms_value.get(),
            humans_value.get()
        ) 
        root.withdraw()
        dashboard(previous=root, simulation_details=simulation_details)
        pass

    # Start button
    start = ctk.CTkButton(master=frame, text="start", command=start_simulation)
    start.grid(row=4, column=0, padx=10, pady=5)

    root.mainloop()

if __name__ == '__main__':
    home()