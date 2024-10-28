# Logitech Heavy Equipment Side Panel Interface
A Python program that allows you to use the Logitech Heavy Equipment Side Panel as a control panel-like device on Linux.
(And maybe macOS, but I don't know for sure. Windows isn't supported currently.)

#### Features:

- Multiple profiles (sort of)
- Device disconnect/reconnect support
- Asynchronous functionality
- All buttons are supported (the joystick technically isn't supported, though)

(This is less of a program and more of a bloated script, though. Some work may be required to make it work out for
your uses. I'm horrible at programming lol.)

### Usage:
To use this program, in `main.py`, set your device's vendor ID and product ID:
```python
# (in main.py)

# Variables
vendor_id: str = "your vendor ID"
product_id: str = "your product ID"
```

These values can be acquired from running `lsusb` in a terminal:
```shell
Bus 001 Device 011: ID (vendor ID):(product ID) Mad Catz, Inc. Saitek Side Panel Control Deck
```
(Note that the device will most likely not be labeled as even a Logitech device, but instead a "Mad Catz Side Panel.")
(Also note that the device ID *must* be acquired from `lsusb` and not anywhere else. This is because `lsusb` shows the
device ID in hexadecimal, or base-16, format, while Python's `evdev` sees product and vendor IDs as decimal, or base-10.
A conversion is run in the program to convert the hexadecimal value to decimal. So if your product and vendor IDs aren't
in hex format, the program won't find your device.)

Functionality for each button can be set in `logitech_side_panel.py`, under the main class, in the `handleButtonPress()`
class method.
```python
# (in logitech_side_panel.py)

async def handleButtonPress(self, code: int) -> None:
    # Path for profile one(or 0)
    if self.current_profile == 0:
        if code == self.button_1:
            print("Button 1 pressed")
            return
        elif code == self.button_2:
            # Do something
            return
        # and so on...
    # Add as many profiles as you desire. To switch profiles, just increment or decrement the
    # self.current_profile variable. You can even make a button do this.
    elif self.current_profile == 1:
        # Just copy the code for each button from profile zero, then add
        # whatever functionality you desire for this profile for each button.
        ...
```

To run the program:
```shell
pip install -r requirements.txt
python main.py
```
