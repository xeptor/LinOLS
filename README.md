# LinOLS
LinOLS is a free, open-source chiptuning software, similar to WinOLS.

# LinOLS - Chiptuning Software

LinOLS is a free, open-source chiptuning software. It allows for advanced ECU mapping and remapping for tuning and optimization, similar to WinOLS. LinOLS is built with Python and provides a graphical user interface for easier interaction and visualization of data.

## Features

- Advanced ECU mapping and remapping
- Plotting and data visualization with `matplotlib`.
- Customizable to suit various ECU tuning needs.

## How to run LinOLS on Linux
You can download an `executable` for Linux, executable is located under `Linux_executable` map in this repository.

And then you just run it with `./LinOLS`.

Important: If you install the executable only thing you need to download is `zenity`, if you don't have it already.

## How to run LinOLS on Windows
You can download an `setup file` for Window 10/11 64bit in map called `Windows_Setup` in this repository. 

## Donations
You can donate here: `https://www.paypal.com/donate?hosted_button_id=HEKSD48J386MJ`
## Prerequisites

### System Requirements

- **Operating System**: Windows or Linux-based (Ubuntu, Arch, or other distributions).
- **Python 3**: Ensure Python 3.x is installed.
  - Check if Python is installed: `python3 --version`
  - If not installed, you can install it using your system package manager.

### Required Dependencies

#### Python Dependencies

- **matplotlib**: A plotting library for Python used for graphical representation.
  
  To install `matplotlib`, use `pip`:
  ```bash
  pip install matplotlib

- **customtkinter**: A GUI library for Python used for making GUI applications.
  
  To install `customtkinter`, use `pip`:
  ```bash
  pip install customtkinter

- **tkinter**: A GUI library for Python used for making GUI applications.

  To install `tkinter`, use your distro's `package manager`:
  
  Arch based distros:
  ```bash
  sudo pacman -S tk
  ```
  Ubuntu/Debian based distros:
  ```bash
  sudo apt install python3-tk
  ```
  Fedora based distros:
  ```bash
  sudo dnf install python3-tkinter
  ```
#### Other Dependencies

- **zenity**: A package for Gnu/Linux distros used for making things like file dialogs.

  To install `zenity`, use your distro's `package manager`:
  
  Arch based distros:
  ```bash
  sudo pacman -S zenity
  ```
  Ubuntu/Debian based distros:
  ```bash
  sudo apt install zenity
  ```
  Fedora based distros:
  ```bash
  sudo dnf install zenity
  ```
## How to run LinOLS
  When you installed all dependencies and they are working as intended you can run LinOLS using the following command:
  ```bash
  python3 main.py
```
## How to make an executable
  To make an Executable you have to use `pyinstaller` a Python library to make executables.
  You can install `pyinstaller` using `pip`:
  ```bash
  pip install pyinstaller
  ```
  Once you have pyinstaller installed you can run this command in the `"LinOLS directory"`:
  ```bash
  pyinstaller --onefile --windowed --hidden-import='PIL._tkinter_finder' main.py
  ```
## Desktop Shortcut
  If you want you can use a provided template desktop shortcut named: `LinOLS.desktop`.
  New update
  You can also find an icon named: `icon.png`.

  Only thing you need to edit is `Exec` and `Icon`.

## Instructions
  ### Text Tab
  You can select multiple numbers with holding the `left click` and then draging with your mouse. You can only drag from up to down.

  You can select one value and right click on text widget to copy value's hex address.
  
  You can use 'm'/'M' to increase number of columns by one or use 'w'/'W' to decrease the columns by one.
  
  You can use 'Page Up' and 'Page Down' for faster navigation.

  `16-bit Lo-Hi and 16-Bit Hi-Lo` are for chaning the byte order and changing the mode will ERASE any changes done.

  `Selected: #` button is for showing you how many numbers do you have selected currently

  `Ori: #` buttion is for showing the original value of the selected value.

  `Columns box` is used for changing the number of columns.

  `Shift box` is used for changing the shift value which basicly moves every value for x times to the right.

  `Text to 2D` is used to show where the selected value or values are in 2d mode.

  `Copy` is used for copying values into Excel or LibreCalc

  `Paste` is used for pasting values from Excel or LibreCalc into your file.

  `Undo` for undoing any changes.

  `Redo` for redoing any changes.

  ### 2D Tab
  You can select a number on 2d canva and you will automaticly show you that number in text mode.
  
  You can use 'Page Up' and 'Page Down' for faster navigation.
  
  `<` move one frame to the left.
  
  `>` move frame to the right.
  
  `<<` move a little bit to the left. 

  `>>` move a little bit to the left. 
  
  `Update` this will update 2d mode with the latest data from text mode.

  `Value: #` this will show you what value you have selected in 2d mode.

  `%` update location of the 2d mode to the one that is enetered in entry box.

  `-` and `+` increase or decrease the value by one.

  ### 3D Tab
  To select the values hold left click and drag over the values you want to select (doesn't work on axis).

  To rotate 3D plot hold left click and drag it around.
  
  You can right click on both axis and any map value to change the axis's/map's properties.

  Every copy and paste buttons are meant for interection with programs like `Excel` and `Libre Calc`

  `Sign` is used to sign values in 3d plot view.

  `Copy Map` copy the values of the map without axis to clipboard.

  `Copy Selected` is used to copy selected values to clipboard.
  
  `Copy X Axis` is used to copy whole X axis to clipboard.

  `Copy Y Axis` is used to copy whole Y axis to clipboard.

  `Update` is used to update values from text view to 3d view.

  `Diff: 0` Shows what is the change on the selected value.

  `Row and column boxes` are used to show current rows and columns in 3d view.

  `Value` is used to change selected value quickly.

  `Write Map` is used to transfer values from 3d grid to text view, so update them.

  `Paste X Axis` is used to paste whole X axis to 3d grid.

  `Paste Y Axis` is used to paste whole Y axis to 3d grid.

  `Paste Selected` is used to paste values from clipboard to the location of the starting value / ONE selected value.

  `Paste` is used to paste the map to 3d grid, excluding both axis.

  ### Maps Tab
  `Maps Tab` is used to show all of the created or imported maps.

  You can `right click` on the map you want to remove. 

  ### File Menu
  `Open` - Open a new file.
  
  `Save` - Save everything into a new file.

  ### Options Menu
  `Find` can be used to find certain number in your file.

  `Import` is used to import already made file with the current one.

  `Difference` is used to show you diffrences done in your file.

  `Value Changes` is used to change multiple numbers at once.

  `Find Hex Address` is used to find your hex address in opened file.

  ### Mappack Menu
  `Import Mappack` is used to import mappack / `.mp` files.

  `Export Mappack` is used to export mappack / `.mp` files.  

  ### Shortcuts
  Edit mode - `E`

  Skip to the next changed value in 2d mode - `n` or `N`
  
  Ship to the previous changed value in 2d mode - `v` or `V`

  Value Dialog - Shift + 5 (Can be accessible via Options menu)

  `Ctrl+V` on Text view for opening files fast

  `Ctrl+I` on Text view for importing files fast
