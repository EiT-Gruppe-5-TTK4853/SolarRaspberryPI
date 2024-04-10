# from gpiozero import LED
import RPi.GPIO as GPIO
from time import sleep, time_ns
import numpy as np


def rad2deg(rad):
    """
    Returns the degrees corresponding to rad radians
    """
    return rad / (2 * np.pi) * 360


def deg2rad(deg):
    """
    Returns the radians corresponding to deg degrees
    """
    return deg * 2 * np.pi / 360


def Rzy(theta=0, psi=0, deg=False):
    """
    Returns the rotation matrix corresponding to a rotation about the z-axis by psi radians,
    followed by a rotation about the y-axis by theta radians. Change deg to true in order to
    use degrees in stead.
    """
    if deg:
        theta = rad2deg(theta)
        psi = rad2deg(psi)

    R = np.array(
        [
            [np.cos(psi) * np.cos(theta), -np.sin(psi), np.cos(psi) * np.sin(theta)],
            [np.sin(psi) * np.cos(theta), np.cos(psi), np.sin(psi) * np.sin(theta)],
            [-np.sin(theta), 0, np.cos(theta)],
        ]
    )
    return R


def rot_from_target(x, y, z):
    """
    Calculates the angles theta and psi, corresponding to the angles of which to rotate about
    the y and z axis in order for the normal vector of the plane to point in the direction of
    the target which has the position p=(x, y, z). These are the angles from the position where
    the panel points straight up, p0=(0,0,1).
    """

    theta = np.arccos(z)
    psi = np.sign(y) * np.arccos(x / np.sin(theta))

    return Rzy(theta, psi), theta, psi


class Pin:
    def __init__(self, pin_number, mode="BCM") -> None:
        assert (
            mode == "BCM" or mode == "BOARD"
        ), f"{mode} is not an accepted mode. Use 'BCM' or 'BOARD'"
        self.pin = pin_number
        self.value = 0
        GPIO.setup(self.pin, GPIO.OUT)

    # def value(self):
    #     return GPIO.input(self.pin)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.value = 1

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.value = 0

    def toggle(self):
        if self.value:
            self.off()
            return

        self.on()


class Stepper:
    def __init__(
        self, out_pin: Pin, dir_pin: Pin, pos=0, ms=1, vel=1, gear_ratio=1.0
    ) -> None:
        """
        out_pin and dir_pin must be of type LED from gpiozero.
        """
        assert ms in [
            1,
            2,
            4,
            8,
            16,
            32,
        ], f"Invalid microstepping. Needs to be one of [1, 2, 4, 8, 16, 32], got {ms}"
        # assert(type(out_pin) == type(dir_pin) == type(LED)), f"The pins should be of type: {type(LED)}\
        #     got out_pin: {type(out_pin)} and dir_pin: {type(dir_pin)}"

        # Set how many steps it takes to make a full rotation. 200 is the default for this stepper,
        # microstepping can increase this number
        self.steps_per_rotation = 200 * ms

        # Set the pins for direction and sending pulses, should be of LED type
        self.out_pin = out_pin
        self.dir_pin = dir_pin

        # Set the direction pin to on.
        self.dir_pin.on()

        # Set starting position
        self.pos = pos

        # Set a default velocity
        self.vel = vel
        self.period = self.calculate_period(vel=vel)

        self.gear_ratio = gear_ratio
        self.da = 360 / (self.steps_per_rotation * self.gear_ratio)

    def calculate_period(self, vel):
        """
        Calculates the period between each step from velocity in rotation per second.
        """
        return 1 / (self.steps_per_rotation * vel)

    def move(self, steps, dir=1, vel=None):
        """
        Drives the stepper for steps number of steps in the direction specified by dir.
        If velocity is not specified, then the default velocity set when initializing
        the object is used.
        """
        if vel == None:
            period = self.period
        else:
            period = self.calculate_period(vel=vel)
            assert (
                abs(vel) < 10
            ), f"You are going too fast, the velocity is capped at 10 rot/s. Got {vel} rot/s"

        assert dir == 0 or dir == 1, f"Direction must be either 0 or 1. Got {dir}"

        # Set the direction
        if self.dir_pin.value != dir:
            self.dir_pin.toggle()

        t0 = time_ns()
        # Toggle the pin
        for i in range(steps):
            self.out_pin.toggle()
            sleep(period / 2)
            self.out_pin.toggle()
            sleep(period / 2)

        print(f"Took {steps} steps in {(time_ns() - t0) / 1000000} ms")

    def move_to(self, angle, pos=None, vel=None, rad=False):
        """
        Moves the stepper such that the angle about this axis is the same as angle.
        If the position of the stepper is not specified when calling the function,
        then it uses the currently calculated position of the stepper. The stepper
        moves at the velocity specified, or at the default value set when initializing
        the object. If angle is in radians, then set rad to True.
        """
        if pos == None:
            # No starting position specified, using own approximation
            pos = self.pos

        if vel == None:
            # No velocity specified, using the default
            vel = self.vel

        if rad:
            angle = rad2deg(angle)

        # Calculate number of steps and set direction
        steps = round((angle - pos) / self.da)
        dir = np.sign(steps)

        if dir == -1:
            dir = 0

        steps = abs(steps)

        print(
            f"Moving to angle {angle} from {pos}. This takes {steps} steps in {dir} direction"
        )

        # Move that many steps in said direction
        self.move(steps=steps, dir=dir, vel=vel)

        return steps
