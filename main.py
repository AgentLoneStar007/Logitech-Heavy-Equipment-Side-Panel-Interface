import sys
import traceback
import evdev
from evdev import InputDevice, ecodes
import asyncio
from logitech_side_panel import LogitechSidePanel

# Variables
vendor_id: str = "your vendor ID"
product_id: str = "your product ID"


# Function to fetch the device in /dev/input
async def fetchDevicePath(device_vendor_id: str, device_product_id: str) -> str | None:
    print("Looking for device...")

    # Convert the Hexadecimal(base-16) values to a decimal(base-10) value
    device_vendor_id: int = int(device_vendor_id, 16)
    device_product_id: int = int(device_product_id, 16)

    while True:
        devices = [InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if (device.info.vendor == device_vendor_id) and (device.info.product == device_product_id):
                return device.path

        # Wait half a second at each interval before trying again
        await asyncio.sleep(0.5)


# Main program loop
async def main() -> None:
    # Create an object of the Logitech side panel class
    side_panel: LogitechSidePanel = LogitechSidePanel()

    while True:
        # Fetch the device's path
        device_path: str = await fetchDevicePath(device_vendor_id=vendor_id, device_product_id=product_id)

        # Open the device
        device = InputDevice(device_path)

        print(f"Listening to events from {device_path}...")
        try:
            for event in device.read_loop():
                if event.type == evdev.ecodes.EV_ABS:  # Absolute axis event, typical for joysticks
                    abs_event: evdev.events.AbsEvent = evdev.categorize(event)
                    axis: int = abs_event.event.code
                    value: int = abs_event.event.value

                    # Print the axis code and its corresponding value (joystick position)
                    print(f"Axis: {axis}, Value: {value}")

                    # You can add specific conditions to handle different axes or ranges of values
                    # Example: Move left or right based on axis 1 values
                    if axis == evdev.ecodes.ABS_X:  # Horizontal movement axis
                        if value < 128:
                            print("Joystick moved left")
                        elif value > 128:
                            print("Joystick moved right")

                    elif axis == evdev.ecodes.ABS_Y:  # Vertical movement axis
                        if value < 128:
                            print("Joystick moved up")
                        elif value > 128:
                            print("Joystick moved down")

                # Key event, button presses
                elif event.type == ecodes.EV_KEY:
                    if event.value == 1:  # Key press (value 0 is release)
                        if event.code in side_panel.button_codes:
                            # Handle a button press
                            await side_panel.handleButtonPress(code=event.code)

                        else:
                            # Print to console if the button isn't recognized
                            print(f"Unrecognized button code: {event.code}")

                    else:
                        # Something can be done here upon the button release, if desired
                        ...

        except OSError:
            print("Lost connection to device, attempting reconnect...")


# Main program execution
if __name__ == "__main__":
    # Create a variable for the return code
    return_code: int = 0

    # Create the program loop
    loop: asyncio.AbstractEventLoop | None = asyncio.new_event_loop()

    try:
        # Run the program
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        print("Stopping!")

    except Exception as error:
        print(f"Process failed with the following error: {error}")
        print(type(error))
        traceback.print_exception()

        # Update the return code
        return_code = 1

    finally:
        # Gracefully stop the event loop
        loop.stop()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        # Stop and return the return code
        sys.exit(return_code)
