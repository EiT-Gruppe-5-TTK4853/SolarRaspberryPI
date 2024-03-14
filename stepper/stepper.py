# If you’re using Raspberry Pi OS (desktop - not Lite) then you have everything you need to use the remote GPIO feature. 
# If you’re using Raspberry Pi OS Lite, or another distribution, you’ll need to install pigpio:

# sudo apt install pigpio
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory
from time import sleep
from utils import *
import sys

# Use the mock pin factory. Probably does not work on the physical device with the following line,
# so comment it out when running on the physical device.
Device.pin_factory = MockFactory()

"""
See the PinLayout.png for an overview of the pins selected. The following are the defaults.
"""
z_out_pin = LED(11)
z_dir_pin = LED(12)

y_out_pin = LED(15)
y_dir_pin = LED(16)

z_axis= Stepper(out_pin=z_out_pin, dir_pin=z_dir_pin)
y_axis = Stepper(out_pin=y_out_pin, dir_pin=y_dir_pin)

def main(*args):
    # Figure out how we want to run things, the following is an example
    assert(len(args) == 3), f"Expected 2 arguments, got {len(args) - 1}: {args[1:]}"
    
    theta, psi = args[1:]
    z_axis.move_to(int(psi))
    y_axis.move_to(int(theta))

    return

if __name__ == "__main__":
    args = sys.argv
    main(*args)

"""
Navigate to the stepper folder and try the script with the following command:
python .\stepper.py 360, -180

Remember to activate the venv before:
windows:    venv\Scripts\activate
Unix/MacOS: source venv/bin/activate
"""