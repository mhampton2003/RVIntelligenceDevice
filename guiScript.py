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

# assign ESP32 to serial port rfcomm1
esp1 = serial.Serial('/dev/rfcomm1', 115200, timeout=1)

# reads the level of the water tank using text file
def read_water_level():
    # open text file
    try:
       with open("output.txt", "r") as file:
           lines = file.readlines()
	   # find where water level data is at in file
           for i, line in enumerate(lines):
               if "'Water Level': Sending state" in line:
                  words = line.split()
                  if len(words) > 2:
		     # return only the part of string that contains data
                     try:
                        sensor_level = float(words[5])
                        return words[5][:5] + " %"
                     except ValueError:
                         return "NA"
       return "NA"
    # handle error if file cannot be opened
    except FileNotFoundError:
       return "File Not Found" 

# updates the water tank level continuously
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
        self.img_water = load_image("/home/capstone/gui/photos/water_icon_new.png")

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
            btn.grid(row=row, column=col, sticky="nsew", padx=20, pady=25)

        # Center the button_frame inside MainMenu by configuring the column and row
        self.grid_rowconfigure(1, weight=3, minsize=100)  # Extra space for centering vertically
        self.grid_columnconfigure(0, weight=1)  # Center horizontally


class TemperaturePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create data labels as strings
        self.temp_label_var = tk.StringVar()
        self.hum_label_var = tk.StringVar()
        self.temp_label_var.set("0")
        self.hum_label_var.set("0")

        self.label = tk.Label(self, text="Temperature & Humidity Levels", font=("Helvetica", 20))
        self.label.pack(pady=25)

        self.canvas = tk.Canvas(self, width=200, height=250)
        self.canvas.pack()

        # Load and resize thermometer image
        self.therm_img = Image.open("/home/maya/gui/photos/temperature_icon_new.png")
        self.therm_img = self.therm_img.resize((200, 230))  # Resize to fit canvas
        self.thermometer = ImageTk.PhotoImage(self.therm_img)

        # Draw the progress bar first (underneath the image)
        self.canvas.create_rectangle(95, 50, 105, 180, fill="white", outline="", tags="thermometer_fill")
	# Display thermometer image on top
        self.canvas.create_image(100, 130, image=self.thermometer)  # Centered placement

        # Label for sensor percentage
        self.value_label = tk.Label(self, text="0F", font=("Arial", 14), fg="black")
        self.value_label.pack()

        self.hum_label = tk.Label(self, text="0%", font=("Arial", 14), fg="black")
        self.hum_label.pack()

        # Back button
        ttk.Button(self, text="Back", command=lambda: controller.show_page("MainMenu")).pack(pady=20)

        # Update data
        self.fetch_data()
        self.update_thermometer()

    def fetch_data(self):
        temp, hum = "0", "0"
        temp_raw = esp1.readline().decode().strip()
        if temp_raw:
        temp_values = temp_raw.split()
            temp = temp_values[0] if len(temp_values) > 0 else "0"
            hum = temp_values[1] if len(temp_values) > 1 else "0"
        self.temp_label_var.set(f"{temp} F")
        self.hum_label_var.set(f"{hum} %")
        self.after(2000, self.fetch_data)


    def update_thermometer(self):
        """Updates the thermometer fill level dynamically."""
        temp = self.temp_label_var.get().split()[0]
        hum = self.hum_label_var.get().split()[0]
        fill_height = (int(float(temp)) / 100) * 92  # Adjust fill height for thermometer tube

        # Determine color based on sensor value
        if int(float(temp)) >=90:
            color = "dark red"
        elif int(float(temp)) >= 70:
            color = "red"
 	elif int(float(temp)) >= 50:
            color = "orange"
        elif int(float(temp)) >= 30:
            color = "skyblue"
        elif int(float(temp)) >= 0:
            color = "blue"
        else:
            color = "purple"

        # Clear previous fill
        self.canvas.delete("thermometer_fill")

        # Fill the circular bulb at the bottom
        self.canvas.create_oval(89, 167, 119, 199, fill=color, outline="", tags="thermometer_fill")  # Circle bulb

        # Draw the thermometer column (rectangle) aligned with the bulb
        bar_x1, bar_x2 = 100, 110  # Narrower column
        bar_bottom = 168  # Start from the top of the bulb
        bar_top = bar_bottom - fill_height  # Calculate height
	self.canvas.create_rectangle(bar_x1, bar_top, bar_x2, bar_bottom, fill=color, outline="", tags="thermometer_fill")

        # Update label (text always black)
        self.value_label.config(text=f"{temp} F", fg="black")
        self.hum_label.config(text=f"Humidity: {hum} %", fg="black")

        # Call again after 1 second
        self.after(1000, self.update_thermometer)


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
            print("Error: Unable to connect to ESP32-CAM stream.")
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
                print("Failed to retrieve frame")

        self.cap.release()

    def stop_stream(self):
        """Stops the ESP32-CAM video stream."""
        self.running = False
        if self.cap:
            self.cap.release()


class WaterPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.label = tk.Label(self, text="Water Tank Level", font=("Helvetica", 20))
        self.label.pack(pady=25)

        # Canvas to show propane tank image and fill level
        self.canvas = tk.Canvas(self, width=300, height=350)
        self.canvas.pack()

        # Load and display propane tank image
        self.water_img = Image.open("/home/capstone/gui/photos/water_icon_new.png")
        self.water_img = self.water_img.resize((275, 325))
        self.water_tank = ImageTk.PhotoImage(self.water_img)
        self.canvas.create_image(150, 175, image=self.water_tank)

        # Label for sensor percentage
        self.value_label = tk.Label(self, text="0%", font=("Arial", 14), fg="black")
        self.value_label.pack()

        # Back button
        ttk.Button(self, text="Back", command=lambda: controller.show_page("MainMenu")).pack(pady=10)

        # Start updating the progress bar
        self.update_progress()

    def update_progress(self):
        """Updates the water tank fill level dynamically."""
        sensor_value = read_water_level()

        if sensor_value == "NA":
           color = "red"
           fill_height = 0
        else:
           sensor_value = int(float(sensor_value[:-3]))
           fill_height = (sensor_value / 100) * 225  # Adjust fill height (tank area)
           color = "green" if sensor_value >= 50 else "orange" if sensor_value >= 20 else "red"

        # Clear previous fill
        self.canvas.delete("progress")

        # Draw the fill level inside the tank image
        self.canvas.create_rectangle(35, 310 - fill_height, 249.5, 310, fill=color, outline="", tags="progress")

        # Update label
        self.value_label.config(text=f"{sensor_value}%", fg="black")

        # Call again after 1 second
        self.after(1000, self.update_progress)



class PropanePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = tk.Label(self, text="Propane Tank Level", font=("Helvetica", 20))
        self.label.pack(pady=25)

        # Canvas to show propane tank image and fill level
        self.canvas = tk.Canvas(self, width=300, height=350)
        self.canvas.pack()

        # Load and display propane tank image
        self.propane_img = Image.open("/home/capstone/gui/photos/propane_icon.png")
        self.propane_img = self.propane_img.resize((275, 325))
        self.propane_tank = ImageTk.PhotoImage(self.propane_img)
        self.canvas.create_image(150, 175, image=self.propane_tank)

        # Label for sensor percentage
        self.value_label = tk.Label(self, text="0%", font=("Arial", 14), fg="black")
        self.value_label.pack()

        # Back button
        ttk.Button(self, text="Back", command=lambda: controller.show_page("MainMenu")).pack(pady=10)

        # Start updating the progress bar
        self.update_progress()
	
	    
   def update_progress(self):
        """Updates the propane tank fill level dynamically."""
        sensor_value = read_propane_level()

        if sensor_value == "NA":
           color = "red"
           fill_height = 0
        else:
           sensor_value = int(float(sensor_value[:-3]))
           fill_height = (sensor_value / 100) * 75  # Adjust fill height (tank area)
           color = "green" if sensor_value >= 50 else "orange" if sensor_value >= 20 else "red"

        # Clear previous fill
        self.canvas.delete("progress")

        # Draw the fill level inside the tank image
        self.canvas.create_rectangle(75, 255 - fill_height, 225, 255, fill=color, outline="", tags="progress")

        # Update label
        self.value_label.config(text=f"{sensor_value}%", fg="black")

        # Call again after 1 second
        self.after(1000, self.update_progress)



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
