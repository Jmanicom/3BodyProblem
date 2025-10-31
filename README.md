## Three Body Problem Gravity Simulation (Python)

This program is an interactive simulation that models the well known "Three Body Problem" studied in mechanics and chaos theory. This program was built using the MatPlotLib, tkninter, and numpy modules. The sim features adjustable parameters such as the ability to change the bodies masses, velocities, position in space, as well as simulation speed. Furthermore, there are various controls for the animation itself.

This project is an amateur/naive approach to similar projects done in the past by others. However, this prorgam was written in my first year of University as a final project for a dynamics physics course I was taking at the time. The goal of the project was to invoke curiosity into the user to explore more of dynamics.

## Requirements
- Python 3.8 or later
- `matplotlib` library
- `numpy` library
- `tkinter` library (included with most Python installations)

## Instruction for Use
To install required packages:

- Open a new terminal window
- Type the following to install any libraries that are underlined in the source code:
    - pip install numpy (to install numpy)
    - pip install matplotlib (to install matplotlib)

NOTE: First time use can take a minute to initialize. If nothing pops-up look for a new window on your taskbar, if missing, close VsCode and run it again.

Using the program:

- Masses are labled according to colour
- To change initial conditions:
  - Press 'reset' and then 'pause' quickly to reset the positions.
  - Use buttons to change the mass or velocities of the bodies, or lock them
  - Press 'resume' to let these new conditions play out
- OR, select a preset and click "load preset" to let a predetermined set of conditions play out.

---

P.S I am working on more optimized version of this project, as well as a C/C++ implementation as well.
