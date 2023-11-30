import time
import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
from pynput import keyboard

class KeyRecorder:
    def __init__(self, master):
        self.master = master
        self.recorded_keys = []
        self.recorded_times = []  # Az időpontok rögzítéséhez
        self.recording = False
        self.intervals = []  # Lista az intevallumok tárolására

        self.master.title("Hotkey Harmony")
        self.master.geometry("500x200")  # Ablak mérete

        self.label = tk.Label(master, text="Records:")
        self.label.config(font=("Arial", 14, "bold"))
        self.label.pack(side=tk.TOP, pady=10, anchor="w")  # Balra igazítás hozzáadva


        # Menü létrehozása
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        # "File" menü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="Save", command=self.save_recorded_keys)
        file_menu.add_command(label="Load", command=self.load_recorded_keys)
        file_menu.add_command(label="Quit", command=self.quit_app)

        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options_menu)

        # "Playback" opció
        playback_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Playback", menu=playback_menu)

        playback_menu.add_command(label="Speed", command=self.playback_option1)
        playback_menu.add_command(label="Repeat", command=self.playback_option2)

        # "Recording" opció
        recording_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Recording", menu=recording_menu)
        
        recording_menu.add_command(label="Option", command=self.recording_option1)
     
        # "Settings" opció
        settings_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Settings", menu=settings_menu)

        settings_menu.add_command(label="Hotkeys", command=self.settings_option1)
        settings_menu.add_command(label="View", command=self.settings_option2)
        settings_menu.add_command(label="Other", command=self.settings_option3)
        
        # Címke a státusz üzenetekhez
        self.status_label = tk.Label(master, text="Ready...", font=("Arial", 10), anchor="w", fg="green")
        self.status_label.pack(side=tk.BOTTOM, anchor=tk.SW, padx=10, pady=5)


        # Gombok és eseménykezelők
        self.start_button = tk.Button(master, text="Record", font=("Arial", 12), command=self.start_recording)
        self.start_button.pack(side=tk.RIGHT, padx=10)

        self.stop_button = tk.Button(master, text="Stop", font=("Arial", 12), command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

        self.play_button = tk.Button(master, text="Start", font=("Arial", 12), command=self.play_recorded_keys)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.author_label = tk.Label(master, text="CoderChef", font=("Arial", 8), fg="gray")
        self.author_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=5)

        self.recording_label = None  # Az aktuális felvétel-intervallum label

        master.bind("<Key>", self.on_key)
        master.bind("<F10>", lambda event: self.handle_hotkey_press("F10"))
        master.bind("<F11>", lambda event: self.handle_hotkey_press("F11"))
        master.bind("<F9>", lambda event: self.handle_hotkey_press("F9"))

    def start_recording(self):
        self.recorded_keys = []
        self.recorded_times = []  # Az időpontok rögzítéséhez
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Recording...", fg="red")

        # Az aktuális felvétel-intervallum label létrehozása
        self.recording_label = tk.Label(self.master, text="Lenyomott gombok:")
        self.recording_label.pack(side=tk.TOP, pady=10)

    def stop_recording(self):
        self.recording = False
        self.intervals.append((self.recorded_keys.copy(), self.recorded_times.copy()))  # Másolatokat készítünk
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.recording_label.destroy()  # Az aktuális felvétel-intervallum label törlése
        self.status_label.config(text="Ready...", fg="green")

    def on_key(self, event):
        if self.recording:
            key = event.char if event.char else str(event.keysym)
            if not self.recorded_keys or key != self.recorded_keys[-1]:
                self.recorded_keys.append(key)
                self.recorded_times.append(time.time())  # Rögzítjük az időpontot
                if self.recording_label:
                    self.update_recording_label()

    def update_recording_label(self):
        if self.recording_label:
            self.recording_label.config(text="Keys: " + " ".join(self.recorded_keys))


    def simulate_key_press(self, key):
        # Hozzunk létre egy Controller példányt
        controller = keyboard.Controller()

        # Szimuláljunk egy gombnyomást a létrehozott példánnyal
        controller.press(key)
        time.sleep(0.1)  # Várunk egy kicsit
        controller.release(key)

    def play_recorded_keys(self):
        self.status_label.config(text="Replaying...", fg="blue")
        for interval_keys, interval_times in self.intervals:
            for i in range(len(interval_keys)):
                key = interval_keys[i]
                self.label.config(text="Lenyomott gombok: " + key)
                self.simulate_key_press(key)
                # Várakozás a következő gombnyomásig
                if i + 1 < len(interval_times):
                    sleep_time = interval_times[i + 1] - interval_times[i]
                    time.sleep(sleep_time)
                self.master.update()
        self.status_label.config(text="Ready...", fg="green")


    def handle_hotkey_press(self, hotkey):
        messagebox.showinfo("Gyorsgomb értesítés", f"{hotkey} gomb megnyomva!", icon="info")
        self.master.after(3000, lambda: self.master.update_idletasks())  # 3 másodperc múlva töröljük az értesítést

    def new_file(self):
        # Töröljük az előző felvétel-intervallumokat
        self.intervals = []

    def save_recorded_keys(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if filename:
            with open(filename, "wb") as file:
                pickle.dump(self.intervals, file)

    def load_recorded_keys(self):
        filename = filedialog.askopenfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if filename:
            with open(filename, "rb") as file:
                self.intervals = pickle.load(file)

    def quit_app(self):
        self.master.destroy()

    def toggle_playback(self):
        # Implementáld a "Repeat" opció állapotának kezelését
        pass

    def recording(self):
        # Implementáld a "Hotkeys" opció állapotának kezelését
        pass

    def set_settings(self):
        # Implementáld a "Speed" opció funkcióját
        pass
        
    def playback_option1(self):
        print("Playback Option 1 selected")

    def playback_option2(self):
        print("Playback Option 2 selected")

    def playback_option3(self):
        print("Playback Option 3 selected")

    def recording_option1(self):
        print("Recording Option 1 selected")

    def recording_option2(self):
        print("Recording Option 2 selected")

    def recording_option3(self):
        print("Recording Option 3 selected")

    def settings_option1(self):
        print("Settings Option 1 selected")

    def settings_option2(self):
        print("Settings Option 2 selected")

    def settings_option3(self):
        print("Settings Option 3 selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyRecorder(root)
    root.mainloop()


