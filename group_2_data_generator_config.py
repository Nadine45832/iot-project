import json
import tkinter as tk
from tkinter import ttk
import random

source_names_examples = [
    "Smart Thermostat",
    "Smart Light Bulb",
    "Smart Plug",
    "Smart Door Lock",
    "Smart Security Camera",
    "Smart Smoke Detector",
    "Smart Refrigerator",
    "Smart Washing Machine",
    "Smart Vacuum Cleaner",
    "Smart Air Purifier",
    "Smart Irrigation Controller",
    "Smart Garage Door Opener",
    "Smart Pet Feeder",
    "Smart Doorbell",
    "Smart Fitness Tracker",
    "Smart TV",
    "Smart Coffee Maker",
    "Smart Baby Monitor",
    "Smart Mirror",
    "Smart Window Sensor",
    "Smert Bulb",
    "Smart Computer",
]


class SourceForm(tk.Frame):
    def __init__(self, master, source_number, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.source_number = source_number

        ttk.Label(self, text=f"Source {source_number}").grid(row=0, column=0, pady=5)

        # Name input
        ttk.Label(self, text="Name:").grid(row=1, column=0, sticky="e")
        self.name_entry = ttk.Entry(self)

        source = random.choice(source_names_examples)
        source_names_examples.remove(source)
        self.name_entry.insert(0, source)
        self.name_entry.grid(row=1, column=1)

        # Signal type combo
        ttk.Label(self, text="Type:").grid(row=1, column=2, sticky="e")
        self.type_combo = ttk.Combobox(
            self,
            values=[
                "random",
                "sine",
                "gaussian",
                "value_with_random_noise",
                "random_signal_with_noise",
            ],
        )
        self.type_combo.grid(row=1, column=3)
        self.type_combo.current(0)

        # Numeric entries
        labels = ["Range Min", "Range Max", "Mean", "Std"]
        default_values = [-10, 10, 0, 1]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(self, text=f"{label}:").grid(row=2, column=i * 2, sticky="e")
            entry = ttk.Entry(self)
            entry.insert(0, str(default_values[i]))
            entry.grid(row=2, column=i * 2 + 1, pady=10)
            self.entries[label] = entry

    def get_data(self):
        return {
            "name": self.name_entry.get(),
            "pattern": self.type_combo.get(),
            "min": self.entries["Range Min"].get(),
            "max": self.entries["Range Max"].get(),
            "mean": self.entries["Mean"].get(),
            "std": self.entries["Std"].get(),
        }


class SignalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data generator")
        self.geometry("800x600")

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="top", pady=10)
        self.add_button = tk.Button(
            self.button_frame, text="Add Source", command=self.add_source
        )
        self.add_button.pack(side="left", padx=10)
        self.save_button = tk.Button(
            self.button_frame, text="Save to JSON", command=self.save_to_json
        )
        self.save_button.pack(side="left", padx=10)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.scrollable_frame.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.sources = []
        self.source_count = 0

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_source(self):
        self.source_count += 1
        source = SourceForm(self.scrollable_frame, self.source_count)
        source.pack(pady=10, fill="x", padx=10)
        self.sources.append(source)

    def save_to_json(self):
        all_data = []
        for source in self.sources:
            data = source.get_data()
            try:
                data["min"] = float(data["min"])
                data["max"] = float(data["max"])
                data["mean"] = float(data["mean"])
                data["std"] = float(data["std"])
            except ValueError:
                print(f"Invalid number input in Source {source.source_number}")
                continue
            all_data.append(data)

        with open("sources.json", "w") as f:
            json.dump(all_data, f)


if __name__ == "__main__":
    app = SignalApp()
    app.mainloop()
