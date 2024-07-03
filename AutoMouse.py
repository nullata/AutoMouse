import tkinter as tk
import os
import sys
from pynput.mouse import Controller
import threading
import time

class MouseMoverApp:
    def __init__(self, master):
        self.master = master
        master.title("AutoMouse")
        master.geometry("400x300")
        master.minsize(400, 300)
        master.maxsize(400, 300)
        master.resizable(False, False)


        # set window icon relative to the script's location
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=true and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(application_path, 'logo.ico')
        master.iconbitmap(default=icon_path)

        # create a frame with padding
        frame = tk.Frame(master, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        # configure grid layout inside the frame
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # label for time
        self.label_time = tk.Label(frame, text="Inactivity time (s):", anchor='w')
        self.label_time.grid(row=0, column=0, sticky='ew')

        # entry widget to enter the time with default value
        self.time_entry = tk.Entry(frame)
        self.time_entry.insert(0, "30")  #default value
        self.time_entry.grid(row=0, column=1, sticky='ew')

        # label for movement
        self.label_movement = tk.Label(frame, text="Move pixels:", anchor='w')
        self.label_movement.grid(row=1, column=0, sticky='ew')

        # entry Widget for movement pixels
        self.movement_entry = tk.Entry(frame)
        self.movement_entry.insert(0, "5")  # default value
        self.movement_entry.grid(row=1, column=1, sticky='ew')

        # label for delay
        self.label_delay = tk.Label(frame, text="Delay between steps (s):", anchor='w')
        self.label_delay.grid(row=2, column=0, sticky='ew')

        # entry Widget for delay
        self.delay_entry = tk.Entry(frame)
        self.delay_entry.insert(0, "0.025")  # default delay value
        self.delay_entry.grid(row=2, column=1, sticky='ew')

        # checkbox for horizontal movement
        self.move_horizontal = tk.BooleanVar(value=True)
        self.checkbox_horizontal = tk.Checkbutton(frame, text="Move Horizontal", var=self.move_horizontal, anchor='w')
        self.checkbox_horizontal.grid(row=3, column=0, columnspan=2, sticky='ew')

        # checkbox for vertical movement
        self.move_vertical = tk.BooleanVar(value=False)
        self.checkbox_vertical = tk.Checkbutton(frame, text="Move Vertical", var=self.move_vertical, anchor='w')
        self.checkbox_vertical.grid(row=4, column=0, columnspan=2, sticky='ew')

        # checkbox for smooth movement
        self.smooth_movement = tk.BooleanVar()
        self.checkbox_smooth = tk.Checkbutton(frame, text="Smooth Movement", var=self.smooth_movement, anchor='w')
        self.checkbox_smooth.grid(row=5, column=0, columnspan=2, sticky='ew')

        # toggle button for monitoring
        self.monitor_button = tk.Button(frame, text="Start Monitoring", command=self.toggle_monitoring)
        self.monitor_button.grid(row=6, column=0, columnspan=2, sticky='ew')

        # mouse controller
        self.mouse_controller = Controller()
        self.running = False
        self.monitor_thread = None

        # setup close window event
        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_monitoring(self):
        if not self.running:
            self.running = True
            self.inactivity_period = float(self.time_entry.get())  # ensure it is set before starting the thread
            self.monitor_thread = threading.Thread(target=self.monitor_mouse)
            self.monitor_thread.start()
            self.monitor_button.config(text="Stop Monitoring")
        else:
            self.stop_monitoring()

    def monitor_mouse(self):
        last_pos = self.mouse_controller.position
        last_time = time.time()

        while self.running:
            current_pos = self.mouse_controller.position
            current_time = time.time()

            if current_pos == last_pos:
                if current_time - last_time > self.inactivity_period:
                    self.move_mouse()
                    last_time = current_time
            else:
                last_pos = current_pos
                last_time = time.time()

            time.sleep(1)  # check every second

    def stop_monitoring(self):
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.monitor_button.config(text="Start Monitoring")

    def on_close(self):
        self.stop_monitoring()
        self.master.destroy()

    def move_mouse(self):
        current_pos = self.mouse_controller.position
        movement = int(self.movement_entry.get())
        delay = float(self.delay_entry.get())
        steps = 20
        dx = movement if self.move_horizontal.get() else 0
        dy = movement if self.move_vertical.get() else 0

        if self.smooth_movement.get():
            for step in range(steps):
                intermediate_pos = (current_pos[0] + (dx * (step + 1) // steps), current_pos[1] + (dy * (step + 1) // steps))
                self.mouse_controller.position = intermediate_pos
                time.sleep(delay)
            for step in range(steps, -1, -1):
                intermediate_pos = (current_pos[0] + (dx * step // steps), current_pos[1] + (dy * step // steps))
                self.mouse_controller.position = intermediate_pos
                time.sleep(delay)
        else:
            target_pos = (current_pos[0] + dx, current_pos[1] + dy)
            self.mouse_controller.position = target_pos
            time.sleep(0.1)
            self.mouse_controller.position = current_pos

# create the main window and pass it to the app
root = tk.Tk()
app = MouseMoverApp(root)
root.mainloop()
