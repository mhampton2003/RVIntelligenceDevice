"""
================================================= 
 RV Intelligence Device
 Emmanuel Loria, Jordan Krause, Maya Hampton
 Date 1/27/2025
 Script to run the GUI and display data
 https://www.geeksforgeeks.org/build-a-basic-form-gui-using-customtkinter-module-in-python/
==================================================
"""

import tkinter as tk
from tkinter import ttk
import random
import serial
import time

# assigning ESP32s to a serial port
esp1 = serial.Serial('/dev/rfcomm1',115200,timeout=1)
esp2 = serial.Serial('/dev/rfcomm2',115200,timeout=1)

# gets the data from the various sensors
def fetch_data():
    water_level = ""
    propane_level = ""
   
    while True: 
        if esp1.in_waiting > 0:
            water_level = f"{esp1.readline().decode()}%" 
        if esp2.in_waiting > 0:
            propane_level = f"{esp2.readline().decode()}%" 
        time.sleep(0.1) 

        temperature = f"{random.uniform(20, 35):.1f} C"
        return propane_level, water_level, temperature

# continually gets data and assigns it
# creates labels for the data
def update_data():
        propane_level, water_level, temperature = fetch_data()
        propane_label_var.set(f"Propane Tank Level: {propane_level}")
        water_label_var.set(f"Water Tank Level: {water_level}")
        temp_label_var.set(f"Temperature: {temperature}")
        root.after(2000, update_data)

# initializes Tkinter window with title and initial size
root = tk.Tk()
root.title("Tank Levels & Temperature")
root.geometry("400x300")

# provides styling
style = ttk.Style()
style.configure("TLabel", font=("Arial", 14))

# creates data labels as strings
propane_label_var = tk.StringVar()
water_label_var = tk.StringVar()
temp_label_var = tk.StringVar()

# sets the labels
propane_label_var.set("Propane Tank Level: --%")
water_label_var.set("Water Tank Level: --%")
temp_label_var.set("Temperature: --C")

# displays data under respective label
ttk.Label(root, textvariable=propane_label_var).pack(pady=10)
ttk.Label(root, textvariable=water_label_var).pack(pady=10)
ttk.Label(root, textvariable=temp_label_var).pack(pady=10)

# creates button to exit GUI
ttk.Button(root, text="Exit", command=root.quit).pack(pady=20)

# get the data and run the GUI
update_data()
root.attributes('-fullscreen', True)
root.mainloop()

