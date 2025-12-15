import tkinter as tk #GUI library
from tkinter import ttk, messagebox #modern gui elements and message boxes
import numpy as np #arrays and numerical operations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class WirelessPropagationCalculator:
    def __init__(self, root):# runs when class is called
        self.root = root
        self.root.title("Coverage Calculator")#main window
        self.root.geometry("900x700") #window size
        
        self.create_widgets()# function that build the GUI
    
    def create_widgets(self):
        main = ttk.Frame(self.root, padding=10) #frame to hold everything
        main.grid(sticky="nsew")# make frame expadn in all directions(show)
        
        # Input Section# frame named input parametrs to place all inmputs inside
        input_frame = ttk.LabelFrame(main, text="Input Parameters", padding=10)
        input_frame.grid(row=0, column=0, sticky="nw", padx=5, pady=5)# placed north west
        
        row = 0 #describes the first row content-frequency
        ttk.Label(input_frame, text="Frequency:").grid(row=row, column=0, sticky="w", pady=3)
        self.freq_entry = ttk.Entry(input_frame, width=15)
        self.freq_entry.grid(row=row, column=1, pady=3)
        self.freq_unit = ttk.Combobox(input_frame, values=["MHz", "GHz"], width=5, state="readonly")#combobox can be editable or readonly
        self.freq_unit.grid(row=row, column=2, padx=5, pady=3)
        self.freq_unit.set("MHz")
        
        fields = [
            ("Tx Power (dBm):", "tx_power"),
            ("Tx Gain (dBi):", "tx_gain"),
            ("Rx Gain (dBi):", "rx_gain"),
            ("Tx Height (m):", "tx_height"),
            ("Rx Height (m):", "rx_height"),
            ("Rx Sensitivity (dBm):", "sensitivity")
        ]
        
        self.entries = {}#dictionary to store input entries
        for label, key in fields:#loop to create labels and eneteries automatically
            row += 1 
            ttk.Label(input_frame, text=label).grid(row=row, column=0, sticky="w", pady=3)
            entry = ttk.Entry(input_frame, width=15)
            entry.grid(row=row, column=1, pady=3)
            self.entries[key] = entry
        #after the loop we add distance range inputs
        row += 1
        ttk.Label(input_frame, text="Distance Range (m):").grid(row=row, column=0, sticky="w", pady=3)
        dist_frame = ttk.Frame(input_frame)
        dist_frame.grid(row=row, column=1, columnspan=2, sticky="w")
        self.d_min = ttk.Entry(dist_frame, width=8)
        self.d_min.pack(side="left", padx=2)
        ttk.Label(dist_frame, text="to").pack(side="left", padx=5)
        self.d_max = ttk.Entry(dist_frame, width=8)
        self.d_max.pack(side="left", padx=2)
        
        row += 1# input frame to hold the buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=row, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Calculate", command=self.calculate).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Load Sample", command=self.load_sample).pack(side="left", padx=5)
        
        # Results Text Area
        results_frame = ttk.LabelFrame(main, text="Results", padding=10)
        results_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.results_text = tk.Text(results_frame, height=15, width=40, font=('Consolas', 10))
        self.results_text.pack(fill="both", expand=True)#grows with the frame
        
        # Plot Area
        plot_frame = ttk.LabelFrame(main, text="Power vs Distance", padding=10)
        plot_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)#stretches in all directions #puts the plot area below the input and results frames
        main.rowconfigure(1, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        
        self.figure, self.ax = plt.subplots(figsize=(8, 5))# create figure and axis for plotting
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)# embed the plot in the tkinter frame
        self.canvas.get_tk_widget().pack(fill="both", expand=True)#make the g
    
    def load_sample(self):#clears all entries and loads sample data
        self.freq_entry.delete(0, tk.END)
        self.freq_entry.insert(0, "2400")
        self.freq_unit.set("MHz")
        self.entries['tx_power'].delete(0, tk.END)
        self.entries['tx_power'].insert(0, "10")
        self.entries['tx_gain'].delete(0, tk.END)
        self.entries['tx_gain'].insert(0, "2")
        self.entries['rx_gain'].delete(0, tk.END)
        self.entries['rx_gain'].insert(0, "2")
        self.d_min.delete(0, tk.END)
        self.d_min.insert(0, "1")
        self.d_max.delete(0, tk.END)
        self.d_max.insert(0, "1000")
        self.entries['tx_height'].delete(0, tk.END)
        self.entries['tx_height'].insert(0, "10")
        self.entries['rx_height'].delete(0, tk.END)
        self.entries['rx_height'].insert(0, "1.5")
        self.entries['sensitivity'].delete(0, tk.END)
        self.entries['sensitivity'].insert(0, "-70")
    
    def clear(self):#clears all input fields and results
        self.freq_entry.delete(0, tk.END)
        self.d_min.delete(0, tk.END)
        self.d_max.delete(0, tk.END)
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.ax.clear()
        self.canvas.draw()
    
    def calculate(self):
        try: #retrieves inputs, performs calculations, and updates results and plot
            # Get inputs
            freq_value = float(self.freq_entry.get())
            freq_unit = self.freq_unit.get().lower()
            tx_power = float(self.entries['tx_power'].get())
            tx_gain = float(self.entries['tx_gain'].get())
            rx_gain = float(self.entries['rx_gain'].get())
            d_min = float(self.d_min.get())
            d_max = float(self.d_max.get())
            tx_height = float(self.entries['tx_height'].get())
            rx_height = float(self.entries['rx_height'].get())
            sensitivity = float(self.entries['sensitivity'].get())
            
            # Validation #distance cant be negative or max less than min
            if d_min <= 0 or d_max <= d_min:
                raise ValueError("Distance range is invalid.")
            
            # Convert frequency #converts if unit is ghz else the unit is mhz
            frequency = freq_value * 1e9 if freq_unit == "ghz" else freq_value * 1e6
            
            # Helper functions #converts dBm to watt 
            def dbm_to_watt(dbm):
                return 10 ** ((dbm - 30) / 10)
            
            def watt_to_dbm(watt):#converts watt to dBm
                return 10 * math.log10(watt) + 30 if watt > 0 else -1000
            
            def dbi_to_linear(dbi):#converts dBi to linear scale #frii and 2ray deal with linear so we convert for this
                return 10 ** (dbi / 10)
            
            # Create distance array - np linspace creates an array of evenly spaced values. Here, it generates 500 points between d_min and d_max because qw want to calculate power at many distances between transmitter and receiver  we wanna plot at a range of distances and also to determine the coverage distance.
            distances = np.linspace(d_min, d_max, 500) #500 points between d_min and d_max
            
            # Friis model calculation
            friis_power = [] #does the conversions and then calculates the frii power
            for d in distances:
                Pt = dbm_to_watt(tx_power)
                Gt = dbi_to_linear(tx_gain)
                Gr = dbi_to_linear(rx_gain)
                wavelength = 3e8 / frequency
                Pr = Pt * Gt * Gr * (wavelength / (4 * math.pi * d)) ** 2
                friis_power.append(watt_to_dbm(Pr))#calculates friis received power and appends to list
            
            # Two-ray model calculation
            two_ray_power = []
            for d in distances:# calculates the two ray power # no need for conversions as two ray works in dBm and dBi directly
                path_loss = (40 * math.log10(d) - tx_gain - rx_gain - 
                            20 * math.log10(tx_height) - 20 * math.log10(rx_height))#pathloss formula for two ray
                two_ray_power.append(tx_power - path_loss)#calculates two ray received power by subtracting pathloss from power and appends to list
            
            # Coverage distances # function to find the maximum distance where received power is above sensitivity
            def find_coverage(power_array, distance_array, sensitivity):
                valid = distance_array[np.array(power_array) >= sensitivity]
                return valid[-1] if len(valid) > 0 else 0 #can be calculated using the distance rule but we already have an array for distance so we just check where the power is greater than senistivity
            #power has to be greater than sensitivity for coverage
            friis_cov = find_coverage(friis_power, distances, sensitivity)
            two_ray_cov = find_coverage(two_ray_power, distances, sensitivity)
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            results = f"Frequency: {freq_value} {freq_unit.upper()}\n"
            results += f"Tx Power: {tx_power} dBm\n"
            results += f"Sensitivity: {sensitivity} dBm\n\n"
            results += f"Friis Coverage: {friis_cov:.2f} m\n"
            results += f"Two-Ray Coverage: {two_ray_cov:.2f} m\n\n"
            
            if friis_cov > two_ray_cov:
                results += "Friis: Larger coverage (optimistic)\n"
            else:
                results += "Two-Ray: Smaller coverage (realistic)\n"
            
            self.results_text.insert(1.0, results)
            
            # Plot
            self.ax.clear()
            self.ax.plot(distances, friis_power, 'b-', label="Friis Model", linewidth=2)
            self.ax.plot(distances, two_ray_power, 'r-', label="Two-Ray Model", linewidth=2)
            self.ax.axhline(sensitivity, color='k', linestyle='--', label=f"Sensitivity ({sensitivity} dBm)")
            if friis_cov > 0:
                self.ax.axvline(friis_cov, color='b', linestyle=':', alpha=0.5)
            if two_ray_cov > 0:
                self.ax.axvline(two_ray_cov, color='r', linestyle=':', alpha=0.5)
            
            self.ax.set_xlabel("Distance (m)")
            self.ax.set_ylabel("Received Power (dBm)")
            self.ax.set_title("Received Power vs Distance")
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)
            self.canvas.draw()
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")

def main():
    root = tk.Tk()
    app = WirelessPropagationCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()