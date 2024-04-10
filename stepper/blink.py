import RPi.GPIO as GPIO
import time
from utils import Pin

# Set GPIO mode
# GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

# # Set pin number
# led_pin = 27

# # Setup LED pin as output
# GPIO.setup(led_pin, GPIO.OUT)

test_pin = Pin(27)

try:
    while True:
        test_pin.toggle()
        # print(test_pin.value)
        time.sleep(20 / 200)
        test_pin.toggle()
        # # Turn on LED
        # GPIO.output(led_pin, GPIO.HIGH)
        # print("LED ON")
        # time.sleep(1)  # Delay for 1 second

        # # Turn off LED
        # GPIO.output(led_pin, GPIO.LOW)
        # print("LED OFF")
        # time.sleep(1)  # Delay for 1 second

except KeyboardInterrupt:
    # Clean up GPIO
    GPIO.cleanup()
