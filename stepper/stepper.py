# If you’re using Raspberry Pi OS (desktop - not Lite) then you have everything you need to use the remote GPIO feature.
# If you’re using Raspberry Pi OS Lite, or another distribution, you’ll need to install pigpio:

# sudo apt install pigpio
import RPi.GPIO as GPIO
from time import sleep
from utils import *
import sys


def main(*args):
    GPIO.setmode(GPIO.BCM)
    # Use the mock pin factory. Probably does not work on the physical device with the following line,
    # so comment it out when running on the physical device.
    # Device.pin_factory = MockFactory()

    test_velocity = 1 / 20
    gear_ratio = 5
    """
    See the PinLayout.png for an overview of the pins selected. The following are the defaults.
    """
    test_pin = Pin(27)

    z_out_pin = Pin(17)
    z_dir_pin = Pin(18)

    y_out_pin = Pin(22)
    y_dir_pin = Pin(23)

    pins = [z_out_pin, z_dir_pin, y_out_pin, y_dir_pin, test_pin]

    z_axis = Stepper(
        out_pin=z_out_pin, dir_pin=z_dir_pin, vel=test_velocity, gear_ratio=gear_ratio
    )
    y_axis = Stepper(
        out_pin=y_out_pin, dir_pin=y_dir_pin, vel=test_velocity, gear_ratio=gear_ratio
    )

    # Make sure that the pins start at off
    for pin in pins:
        pin.off()
    # Figure out how we want to run things, the following is an example
    # assert len(args) == 2, f"Expected 2 arguments, got {len(args) - 1}: {args[1:]}"
    if len(args) == 5:
        args = args[1:]

    print(f"Yaw: {args[2]} -> {args[0]}")
    print(f"Pitch: {args[3]} -> {args[1]}")

    psi, theta = args[0:2]
    oldPsi, oldTheta = args[2:4]
    z_steps = z_axis.move_to(int(psi), pos=int(oldPsi))
    y_steps = y_axis.move_to(int(theta), pos=int(oldTheta))

    GPIO.cleanup()
    return {"z_steps": z_steps, "y_steps": y_steps}


if __name__ == "__main__":
    args = sys.argv
    main(*args)

"""
Navigate to the stepper folder and try the script with the following command:
python .\stepper.py 360, -180

The required packages are found in requirements.txt and can be installed into
any create virtual environment by the command:
pip install -r requirements.txt
"""
