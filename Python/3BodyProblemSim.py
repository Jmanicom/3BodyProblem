"""
====================================
File Name: 3BodyProblemSim.py
Student: Joshua Manicom
Date: Apr 4th, 2025
Version: 1.2

Brief Description: This program is an interactable simulation of the widely famous '3 Body problem'. Through this simulation we are able to explore the interactions
between multiples celestial bodies in a simplified and fun way. The parameters of the bodies (mass, velocity, position) are scaled down, along side the constant G, to make
the simulation easier to run and the 3D plot smaller.

For a more detailed description, please view the file in this folder "README"
=====================================
"""
# >>>>>>>>>>>>>>>> Simulation Setup - Body Parameters, Module Initialization, etc. <<<<<<<<<<<<<<<

# =================== Library Setup =================== #
import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# =================== Constants =================== #
G = 1.25  # Gravitational constant (scaled for simulation)
softening = 0.5  # Softening factor to avoid singularities (accel. approaches inf)
paused = False  # Initial bool value for the puase function

# =================== Presets =================== #
presets = {
    "Default Orbit": [
        {"mass": 8.0, "pos": [2.0, -2.0, 1.0], "vel": [0.0, 1.0, 0.0]},
        {"mass": 3.0, "pos": [-1.0, -2.0, -1.0], "vel": [0.0, -1.2, 0.0]},
        {"mass": 4.0, "pos": [0.0, -4.0, -1.0], "vel": [-1.0, 0.0, 0.0]}
    ],
    "Chaotic Dance": [
        {"mass": 8.0, "pos": [2.0, -2.0, 1.0], "vel": [0.5, 0.2, 0.0]},
        {"mass": 3.0, "pos": [-0.5, -2.5, -1.5], "vel": [-0.3, -1.2, 0.3]},
        {"mass": 4.0, "pos": [0.5, -3.0, -1.0], "vel": [-1.2, 0.6, -0.3]}
    ],
    "Slingshot": [
        {"mass": 8.0, "pos": [2.0, -2.0, 1.0], "vel": [0.0, 0.8, 0.0]},
        {"mass": 3.0, "pos": [-1.0, -2.0, -1.0], "vel": [0.0, -1.2, 0.0]},
        {"mass": 0.5, "pos": [5.0, -5.0, 0.0], "vel": [-3.0, 2.0, 0.0]}
    ]
}

# =============== Create the Bodies from the Above Presets =============== #
def load_bodies(preset_name):
    # Initialize body parameters from selected preset
    return [{
        "mass": b["mass"],
        "pos": np.array(b["pos"], dtype=float),
        "vel": np.array(b["vel"], dtype=float),
        "trail": [],
        "locked": False  # Track whether body is locked
    } for b in presets[preset_name]]

bodies = load_bodies("Default Orbit")

# >>>>>>>>>>>>>>>> GUI, 3D Plot Setup - Space Parameters, Colouring/Graphics, Buttons <<<<<<<<<<<<<<<

# =================== GUI Setup =================== #
root = tk.Tk()
root.title("3-Body Simulation")
root.configure(bg="black")

# ============ Define and Create the MatPlotLib 3D Plot =========== #
fig = Figure(figsize=(6, 6), dpi=100)
fig.patch.set_facecolor("black")
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor("black")
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_zlim(-30, 30)
ax.set_title("3-Body Gravitational Interaction", color='white')
ax.tick_params(colors='white')
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.zaxis.label.set_color("white")

# ============ Define the Canvas for the 3D Plot =========== #
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# ============ 3D Plot Setup Visuals =========== #
colors = ['white', 'cyan', 'lime']
plots = []
for color in colors:
    dot, = ax.plot([], [], [], marker='o', color=color, markersize=5)
    trail, = ax.plot([], [], [], linestyle='-', color=color, linewidth=1)
    plots.append((dot, trail))

# ============ Control Panel =========== #
control_frame = tk.Frame(root, bg="black")
control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# ============ Define Time Step Slider and Initial Value =========== #
dt_var = tk.DoubleVar(value=0.1)

# ============ Setup Labels for the Parameter Buttons =========== #
label_vars = [{
    "mass": tk.StringVar(),
    "vx": tk.StringVar(), "vy": tk.StringVar(), "vz": tk.StringVar(),
    "locked": tk.StringVar()
} for _ in range(3)]

# ============ Update the labels function =========== #
def update_labels():
    for i, b in enumerate(bodies):
        label_vars[i]["mass"].set(f"{b['mass']:.1f}")
        for j, axis in enumerate("xyz"):
            label_vars[i][f"v{axis}"].set(f"{b['vel'][j]:.1f}")
        label_vars[i]["locked"].set("Locked" if b["locked"] else "Unlocked")

# >>>>>>>>>>>>>>>> Parameter Updating Functions/ Simulation Controls <<<<<<<<<<<<<<<
def adjust_mass(i, delta):
    if not bodies[i]["locked"]:
        bodies[i]["mass"] = max(0.1, bodies[i]["mass"] + delta)
        update_labels()

def adjust_velocity(i, axis, delta):
    if not bodies[i]["locked"]:
        axis_map = {"x": 0, "y": 1, "z": 2}
        bodies[i]["vel"][axis_map[axis]] += delta
        update_labels()

def toggle_lock(i):
    bodies[i]["locked"] = not bodies[i]["locked"]
    update_labels()

def toggle_pause():
    global paused
    paused = not paused
    pause_btn.config(text="Resume" if paused else "Pause")

def reset_sim():
    global bodies
    bodies = load_bodies("Default Orbit")
    update_labels()

# >>>>>>>>>>>>>>>> Creating the Control Buttons to Add to the Canvas <<<<<<<<<<<<<<<
for i in range(3):
    row = i * 2
    color = colors[i]
    font = ("Courier New", 12)
    tk.Label(control_frame, text=f"Body {i+1}", bg="black", fg=color, font=font).grid(row=row, column=0, columnspan=2)
    tk.Label(control_frame, text="Mass:", bg="black", fg=color, font=font).grid(row=row+1, column=0)
    tk.Label(control_frame, textvariable=label_vars[i]["mass"], bg="black", fg=color, font=font).grid(row=row+1, column=1)
    tk.Button(control_frame, text="+", command=lambda i=i: adjust_mass(i, +1), bg="gray20", fg=color, font=font).grid(row=row+1, column=2)
    tk.Button(control_frame, text="-", command=lambda i=i: adjust_mass(i, -1), bg="gray20", fg=color, font=font).grid(row=row+1, column=3)

    for j, axis in enumerate("xyz"):
        base_col = 5 + j * 4
        tk.Label(control_frame, text=f"v{axis}:", bg="black", fg=color, font=font).grid(row=row+1, column=base_col)
        tk.Label(control_frame, textvariable=label_vars[i][f"v{axis}"], bg="black", fg=color, font=font).grid(row=row+1, column=base_col + 1)
        tk.Button(control_frame, text="+", command=lambda i=i, axis=axis: adjust_velocity(i, axis, +0.5), bg="gray20", fg=color, font=font).grid(row=row+1, column=base_col + 2)
        tk.Button(control_frame, text="-", command=lambda i=i, axis=axis: adjust_velocity(i, axis, -0.5), bg="gray20", fg=color, font=font).grid(row=row+1, column=base_col + 3)

    # Lock/Unlock Button
    tk.Button(control_frame, textvariable=label_vars[i]["locked"], command=lambda i=i: toggle_lock(i), bg="gray30", fg=color, font=font).grid(row=row+1, column=18, columnspan=2, padx=(20,0))

# >>>>>>>>>>>>>>>> Creating the Preset Dropdown Menu <<<<<<<<<<<<<<<
selected_preset = tk.StringVar(value="Default Orbit")
tk.Label(control_frame, text="Presets:", bg="black", fg="white", font=font).grid(row=9, column=0)
preset_menu = tk.OptionMenu(control_frame, selected_preset, *presets.keys())
preset_menu.config(bg="gray20", fg="white", highlightthickness=0, font=font)
preset_menu.grid(row=9, column=1, columnspan=2)

def load_selected_preset():
    global bodies
    bodies = load_bodies(selected_preset.get())
    update_labels()

tk.Button(control_frame, text="Load Preset", command=load_selected_preset, bg="gray20", fg="white", font=font).grid(row=9, column=3, columnspan=2)

pause_btn = tk.Button(control_frame, text="Pause", command=toggle_pause, bg="gray20", fg="white", font=font)
pause_btn.grid(row=7, column=0, columnspan=2, pady=5)

reset_btn = tk.Button(control_frame, text="Reset", command=reset_sim, bg="gray20", fg="white", font=font)
reset_btn.grid(row=7, column=2, columnspan=2, pady=5)

tk.Label(control_frame, text="Time Step:", bg="black", fg="white", font=font).grid(row=8, column=0, sticky='e', padx=5)
tk.Scale(control_frame, from_=0.01, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, variable=dt_var, length=200, bg="black", fg="white", troughcolor="gray30").grid(row=8, column=1, columnspan=4, sticky='w')

# >>>>>>>>>>>>>>>> Help Text for Users to Understand Controls <<<<<<<<<<<<<<<
instructions = (
    "Plot Controls:\n"
    "• Rotate: Left-click + drag\n"
    "• Zoom in: Right-Click + drag down\n"
    "• Zoom out: Right-click + drag up\n\n"
    "Simulation Tips:\n"
    "• Use +/– to adjust mass or velocity\n"
    "• Lock bodies to freeze them\n"
    "• dt slider controls speed\n"
    "• Pause/Reset anytime\n"
    "• Use presets to explore\n"
    "\t• Select Preset in Dropdown then 'load preset'\n"
)

help_label = tk.Label(root, text=instructions, justify="left", font=("Courier New", 12), bg="black", fg="white", anchor="se", padx=10, pady=10)
help_label.place(relx=1.0, rely=1.0, anchor="se")

# >>>>>>>>>>>>>>>> Simulation Logic + Plot Updater <<<<<<<<<<<<<<<
def update_simulation():
    global paused
    if not paused:
        dt = dt_var.get()
        accels = [np.zeros(3) for _ in range(3)]
        for i in range(3):
            if bodies[i]["locked"]:
                continue
            for j in range(3):
                if i != j:
                    r_ij = bodies[j]["pos"] - bodies[i]["pos"]
                    d = np.linalg.norm(r_ij)
                    accels[i] += G * bodies[j]["mass"] * r_ij / (d**2 + softening**2)**1.5

        for i in range(3):
            if bodies[i]["locked"]:
                continue
            bodies[i]["vel"] += accels[i] * dt
            bodies[i]["pos"] += bodies[i]["vel"] * dt
            bodies[i]["trail"].append(bodies[i]["pos"].copy())
            if len(bodies[i]["trail"]) > 300:
                bodies[i]["trail"].pop(0)

        update_plot()
    root.after(50, update_simulation)

# === Update Plot === #
def update_plot():
    for i, (dot, trail) in enumerate(plots):
        b = bodies[i]
        pos = b["pos"]
        dot.set_data([pos[0]], [pos[1]])
        dot.set_3d_properties([pos[2]])
        if b["trail"]:
            t = np.array(b["trail"])
            trail.set_data(t[:, 0], t[:, 1])
            trail.set_3d_properties(t[:, 2])
        else:
            trail.set_data([], [])
            trail.set_3d_properties([])
        dot.set_markersize(b["mass"] * 2)
    canvas.draw()

# ======== Run Simulation ======== #
update_labels()
update_simulation()
root.mainloop()