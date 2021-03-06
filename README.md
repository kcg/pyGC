pyGC
====

pyGC is a control programm for an automated CNC glass cutter.
The program takes care of the communication to the TinyG board which is used to control the three axes of the cutter.
It provides a GUI where dxf or gcode files can be loaded, previewed and the cutting is run.

Following features are implemented:
-----------------------------------
- Automatic connection to the glass cutter (TinyG)
- Manual control of the axis, inclusing homing and positioning
- Loading of dxf and gcode/ngc files
- Graphical preview of loaded files
- Automatic tool selection. A wheel cutter is used for horizontal and vertical lines. A diamond scribe for labels.
- Glass thickness is variable

Dependencies:
-------------
- Linux (tested on Ubuntu 14.04)
- Python 2.7, wxpython
- dxf2gcode (http://sourceforge.net/p/dxf2gcode/)
- TinyG for controlling the hardware (stepper motors and end-stops) (https://github.com/synthetos/TinyG).
- The glass cutter is custom built using a Shapeoko 2 (http://www.shapeoko.com/wiki/). 

Install and Run:
----------------
1. Download/Clone pyGC. There is no actual installation necessary.
2. Install/Download dxf2gcode (https://sourceforge.net/p/dxf2gcode/wiki/Installation/)
3. Update the path in the config.ini (config/config.ini)
4. Run "run.sh"

Contact:
--------
Karl C. Gödel,
mail@karl-goedel.de

Screenshots:
------------
![Screen1](https://github.com/kcg/pyGC/blob/master/screenshots/screen1.png "Screenshot 1")
![Screen2](https://github.com/kcg/pyGC/blob/master/screenshots/screen2.png "Screenshot 2")
