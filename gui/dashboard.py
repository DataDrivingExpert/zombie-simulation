
import tkinter as tk
import customtkinter as ctk

from globalConfig import styles

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

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

# This is inside leftCol and location
location_selector = ctk.CTkOptionMenu(master=location, font=styles.NORMAL_FONT,values=["floor 1", "floor 2"])
location_selector.grid(row=0,column=1, pady=10,padx=10)


# fsum: Floor summary
# This is inside leftCol
fsum_label = ctk.CTkLabel(master=leftCol,text="Floor Summary", font=styles.NORMAL_FONT)
fsum_label.grid(row=1, column=0, padx=(20,0), pady=10, sticky="w")

fsum_value = tk.StringVar()

# fsum TextBox
fsum_display = ctk.CTkTextbox(master=leftCol, font=styles.NORMAL_FONT)
fsum_display.grid(row=2, column=0, padx=(20,5),pady=(0,10), sticky="ew")

# Simulation activity
sim_label = ctk.CTkLabel(master=leftCol, text="Simulation activity", font=styles.NORMAL_FONT)
sim_label.grid(row=3, column=0, padx=(20, 0), pady=(0,10), sticky="w")

# sim TextBox
sim_display = ctk.CTkTextbox(master=leftCol, font=styles.NORMAL_FONT)
sim_display.grid(row=4, column=0, padx=(20,5),pady=(0,10), sticky="ew")

# Right column in colsLayout
rightCol = ctk.CTkFrame(master=colsLayout)
rightCol.grid(row=0, column=1, padx=(5,10), pady=10, sticky="nsew")
rightCol.grid_columnconfigure(0, weight=1)
rightCol.grid_rowconfigure(1, weight=1)
rightCol.grid_rowconfigure(3, weight=2)

# Scenario group
scenario_label = ctk.CTkLabel(master=rightCol, text="Scenario", font=styles.NORMAL_FONT)
scenario_label.grid(row=0, column=0, sticky="nw", padx=5)

SCENARIO_EXAMPLE = """ turn: 0\n survivors alive: 10\n zombies alive: 5\n """

scenario_value = tk.StringVar(value=SCENARIO_EXAMPLE)

scenario_display = ctk.CTkTextbox(master=rightCol, font=styles.NORMAL_FONT)
scenario_display.grid(row=1, column=0, sticky="nsew",padx=5)
scenario_display.insert("0.0", scenario_value.get())

# Last Sensor triggered
sensor_label = ctk.CTkLabel(master=rightCol, text="Last Sensor Triggered", font=styles.NORMAL_FONT)
sensor_label.grid(row=2, column=0, sticky="nw", padx=5)

sensor_value = tk.StringVar()

sensorCard = ctk.CTkFrame(master=rightCol)
sensorCard.grid(row=3, column=0, sticky="nsew",padx=5, pady=5)
sensorCard.grid_columnconfigure(0, weight=1)
sensorCard.grid_rowconfigure(0, weight=1)

sensor_display = ctk.CTkLabel(master=sensorCard, text="Room 3 at Floor 2", font=("Roboto", 20))
sensor_display.grid(row=0, column=0, sticky="nsew",)

# Controls
controls = ctk.CTkFrame(master=frame)
controls.grid(row=2, column=0, pady=(10, 5), padx=10)
controls.grid_columnconfigure((0,1,2,3), weight=1)

def example():
    pass

play = ctk.CTkButton(master=controls, text="next", font=styles.NORMAL_FONT, command=example) # Agregar command
play.grid(row=0, column=0, padx=5, pady=5)

stop = ctk.CTkButton(master=controls, text="stop",  font=styles.NORMAL_FONT, command=example) # Agregar command
stop.grid(row=0, column=1, padx=5, pady=5)

restart = ctk.CTkButton(master=controls, text="restart", font=styles.NORMAL_FONT,command=example) # Agregar command
restart.grid(row=0, column=2, padx=5, pady=5)

save = ctk.CTkButton(master=controls, text="save", font=styles.NORMAL_FONT,command=example) # Agregar command
save.grid(row=0, column=3, padx=5, pady=5)

root.mainloop()