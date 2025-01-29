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
esp1 = serial.Serial('/dev/rfcomm1', 115200, timeout=1)
esp2 = serial.Serial('/dev/rfcomm2', 115200, timeout=1)

# gets the data from the various sensors
def fetch_data():
    temp1 = ""
    temp2 = ""

    # loop to continuously get temperature data
    while True:
        if esp1.in_waiting > 0:
            temp1 = f"{esp1.readline().decode().strip()} C"
        if esp2.in_waiting > 0:
            temp2 = f"{esp2.readline().decode().strip()} C"
        time.sleep(0.1)

        return temp1, temp2

# updates the temperature on the screen 
def update_data(page, temp1_label_var, temp2_label_var):
    # get updated data, set the variable, print the data to the screen every 2 seconds
    temp1, temp2 = fetch_data()
    temp1_label_var.set(f"Refridgerator Temperature: {temp1}")
    temp2_label_var.set(f"Freezer Temperature: {temp2}")
    page.after(2000, lambda: update_data(page, temp1_label_var, temp2_label_var))

# main application class for the GUI
class MainApp(tk.Tk):
    # sets up the window
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry("600x400")

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.pages = {}

        # Initialize all pages
        for Page in (MainMenu, TemperaturePage, CameraPage, PropanePage, WaterPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("MainMenu")
    # display the specified page at the front of the window
    def show_page(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()

# main menu page class
class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Set grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Left-side label
        label = tk.Label(self, text="Select A Menu", font=("Helvetica", 24), bg="lightgray", anchor="center")
        label.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)

        # Buttons
        btn_temperature = tk.Button(self, text="View Temperature", font=("Helvetica", 14), bg="lightyellow",
                                     command=lambda: controller.show_page("TemperaturePage"))
        btn_temperature.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        btn_camera = tk.Button(self, text="View Camera Feed", font=("Helvetica", 14), bg="lightblue",
                                command=lambda: controller.show_page("CameraPage"))
        btn_camera.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        btn_propane = tk.Button(self, text="View Propane Tank Levels", font=("Helvetica", 14), bg="lightgreen",
                                 command=lambda: controller.show_page("PropanePage"))
        btn_propane.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        btn_water = tk.Button(self, text="View Water Tank Levels", font=("Helvetica", 14), bg="#DDA0DD",
                               command=lambda: controller.show_page("WaterPage"))
        btn_water.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

# temperature class page
class TemperaturePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Styling
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 14))

        # Create data labels as strings
        temp1_label_var = tk.StringVar()
        temp2_label_var = tk.StringVar()
        temp1_label_var.set("Temperature Sensor 1: -- C")
        temp2_label_var.set("Temperature Sensor 2: -- C")

        # Display data
        ttk.Label(self, textvariable=temp1_label_var).pack(pady=10)
        ttk.Label(self, textvariable=temp2_label_var).pack(pady=10)

        # Back button
        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_page("MainMenu")).pack(pady=20)

        # Update data
        update_data(self, temp1_label_var, temp2_label_var)

# camera page class
class CameraPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Camera Feed Page", font=("Helvetica", 20)).pack(pady=20)
        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_page("MainMenu")).pack(pady=10)

# propane tank page class
class PropanePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Propane Tank Levels Page", font=("Helvetica", 20)).pack(pady=20)
        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_page("MainMenu")).pack(pady=10)

# water tank page class
class WaterPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Water Tank Levels Page", font=("Helvetica", 20)).pack(pady=20)
        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_page("MainMenu")).pack(pady=10)

# runs the application
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
