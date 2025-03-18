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
import cv2
import threading
import threads
from PIL import Image, ImageTk

ESP32_CAM_URL = "http://172.20.10.4/stream"  # ESP32-CAM IP

# assigning ESP32s to a serial port
esp1 = serial.Serial('/dev/rfcomm1', 115200, timeout=1)
esp2 = serial.Serial('/dev/rfcomm2', 115200, timeout=1)

# read value from water tank
def read_water_level():
    try:
       with open("output.txt", "r") as file:
           lines = file.readlines()
           for i, line in enumerate(lines):
               if "'Water Level': Sending state" in line:
                  words = line.split()
                  if len(words) > 2:
                     try:
                        sensor_level = float(words[5])
                        return words[5][:5] + " %"
                     except ValueError:
                         return "NA"
       return "NA"
    except FileNotFoundError:
       return "File Not Found" 

# continuously update values from water tank
def update_water_level(label_var, page):
    water_level = read_water_level()
    label_var.set(f"Water Tank Level: {water_level}")
    page.after(2000, lambda: update_water_level(label_var, page))

# read value from propane tank
def read_propane_level():
    try:
       with open("output.txt", "r") as file:
           lines = file.readlines()
           for i, line in enumerate(lines):
               if "'Propane Level': Sending state" in line:
                  words = line.split()
                  if len(words) > 2:
                     try:
                        sensor_level = float(words[5])
                        return words[5][:5] + " %"
                     except ValueError:
                         return "NA"
       return "NA"
    except FileNotFoundError:
       return "File Not Found" 

# continuously update values from propane tank
def update_propane_level(label_var, page):
    propane_level = read_propane_level()
    label_var.set(f"Propane Tank Level: {propane_level}")
    page.after(2000, lambda: update_propane_level(label_var, page))


# gets the data from the various sensors
def fetch_data():
    temp1 = ""
    temp2 = ""
    temp1_raw = ""
    temp2_raw = ""
    temp1_value = ""
    temp2_value = ""

    # loop to continuously get temperature data
    while(True): 
       if esp1.in_waiting > 0:
          temp1_raw = esp1.readline().decode().strip()
          temp1_value = temp1_raw.split()[0] + " F\n                      " + temp1_raw.split()[1] if temp1_raw else "NA"
          temp1 = f"{temp1_value} %" 
       if esp2.in_waiting > 0:
          temp2_raw = esp2.readline().decode().strip()  
          temp2_value = temp2_raw.split()[0] if temp2_raw else "NA"
          temp2 = f"{temp2_value} F" 
       return temp1, temp2

# updates the temperature on the screen 
def update_data(page, temp1_label_var, temp2_label_var):
    # get updated data, set the variable, print the data to the screen every 2 seconds
    temp1, temp2 = fetch_data()
    temp1_label_var.set(f"Cabin Temperature: {temp1}")
    temp2_label_var.set(f"Fridge Temperature: {temp2}")
    page.after(2000, lambda: update_data(page, temp1_label_var, temp2_label_var))

# main application class for the GUI
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.attributes("-fullscreen", True)
        # Create a Canvas for the border
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="white")
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a container for the border
        self.border_container = ttk.Frame(self, relief="solid", padding=10)
        self.border_container.place(x=10, y=10, relwidth=1, relheight=1, anchor="nw", width=-20, height=-20)

        # Green-bordered frame around the container
        self.container_frame = ttk.Frame(self.border_container, padding=5)
        self.container_frame.pack(fill="both", expand=True)

        # Main container for pages with green border
        self.container = tk.Frame(self.container_frame, bg="white", highlightbackground="dark green",
                                  highlightthickness=4)
        self.container.pack(fill="both", expand=True, padx=5, pady=5)

        self.pages = {}
        for Page in (MainMenu, TemperaturePage, CameraPage, PropanePage, WaterPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

	self.show_page("MainMenu")
	        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
	        self.bind("<Configure>", self.draw_border)  # Redraw border when resized
	
    def draw_border(self, event=None):
	self.canvas.delete("border")  # Clear previous border
	width = self.winfo_width()
	height = self.winfo_height()
	margin = 40

	self.canvas.create_rectangle(
	    margin, margin, width - margin, height - margin,
	    outline="dark green", width=4, tags="border"
	)

    def show_page(self, page_name):
	frame = self.pages[page_name]
	frame.tkraise()


class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="Main.TFrame")

        # Make the MainMenu grid expand to fill the entire parent window
        self.grid_columnconfigure(0, weight=1)

	self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        # Title
        label = tk.Label(self, text="Welcome Home!", font=("Rockwell", 42), anchor="center")
        label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=(50,0))

        # Button Container
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, sticky="nsew", padx=293, pady=0)

        # Adjust the grid inside the button_frame to center the buttons
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)

        # Load Images (Ensure the images exist in the same directory)
        def load_image(path, size=100):
            img = tk.PhotoImage(file=path)
            return img.subsample(img.width() // size, img.height() // size)

        self.img_temperature = load_image("/home/capstone/gui/photos/temperature_icon.png")
        self.img_camera = load_image("/home/capstone/gui/photos/camera_icon.png")
        self.img_propane = load_image("/home/capstone/gui/photos/propane_icon.png")
        self.img_water = load_image("/home/capstone/gui/photos/water_icon.png")

        # Buttons
        buttons = [
            ("Temperature", self.img_temperature, "TemperaturePage"),
            ("Camera", self.img_camera, "CameraPage"),
            ("Propane", self.img_propane, "PropanePage"),
            ("Water", self.img_water, "WaterPage")
        ]

        for i, (text, img, page) in enumerate(buttons):
            row, col = divmod(i, 2)
            btn = tk.Button(button_frame, image=img, text=text, compound="top",
                            font=("Rockwell", 14), bg="white", fg="black",
                            command=lambda p=page: controller.show_page(p))
            btn.grid(row=row, column=col, sticky="nsew", padx=20, pady=26.5)

        # Center the button_frame inside MainMenu by configuring the column and row
        self.grid_rowconfigure(1, weight=3, minsize=100)  # Extra space for centering vertically
        self.grid_columnconfigure(0, weight=1)  # Center horizontally



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


class CameraPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = tk.Label(self, text="ESP32-CAM Stream", font=("Helvetica", 20))
        self.label.pack(pady=10)

        self.video_label = tk.Label(self)
        self.video_label.pack()

        self.start_button = ttk.Button(self, text="Start Stream", command=self.start_stream)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self, text="Stop Stream", command=self.stop_stream)
        self.stop_button.pack(pady=5)

        self.back_button = ttk.Button(self, text="Back", command=lambda: controller.show_page("MainMenu"))
        self.back_button.pack(pady=10)

        self.running = False
        self.cap = None

    def start_stream(self):
        """Starts the ESP32-CAM video stream."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.update_frame, daemon=True)
            self.thread.start()

    def update_frame(self):
        """Fetch frames from ESP32-CAM and display in Tkinter."""
        self.cap = cv2.VideoCapture(ESP32_CAM_URL)

        if not self.cap.isOpened():
            print("❌ Error: Unable to connect to ESP32-CAM stream.")
            self.running = False
            return

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                self.video_label.configure(image=img)
                self.video_label.image = img
            else:
                print("⚠️ Failed to retrieve frame")

        self.cap.release()

    def stop_stream(self):
        """Stops the ESP32-CAM video stream."""
        self.running = False
        if self.cap:
            self.cap.release()


class WaterPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.water_level_var = tk.StringVar()
        self.water_level_var.set("Water Tank Level: -- %")

        ttk.Label(self, textvariable=self.water_level_var, font=("Helvetica", 16)).pack(pady=20)


        ttk.Button(self, text="Back", command=lambda: controller.show_page("MainMenu")).pack(pady=10)
        update_water_level(self.water_level_var, self)


class PropanePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.propane_level_var = tk.StringVar()
        self.propane_level_var.set("Propane Tank Level: -- %")

        ttk.Label(self, textvariable=self.propane_level_var, font=("Helvetica", 16)).pack(pady=20)


        ttk.Button(self, text="Back", command=lambda: controller.show_page("MainMenu")).pack(pady=10)
        update_propane_level(self.propane_level_var, self)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
