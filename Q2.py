
import RPi.GPIO as GPIO
import time
import threading

class LEDPassingAnimation:
    def __init__(self, led_pins):
        self.led_pins = led_pins
        self.stop_flag = False
        GPIO.setmode(GPIO.BCM)
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)
    
    def start(self):
        """Initiates the LED animation and listens for a stop command."""
        thread = threading.Thread(target=self._keyboard_input_listener)
        thread.start()
        self._animate_leds()
        thread.join()
        GPIO.cleanup()

    def _keyboard_input_listener(self):
        """Listens for keyboard input to stop the animation."""
        input("Press any key to stop...")
        self.stop_flag = True

    def _animate_leds(self):
        """Animates LEDs moving towards opposite ends and then back."""
        led_count = len(self.led_pins)
        try:
            while not self.stop_flag:
                # Move towards the opposite ends
                for i in range(led_count):
                    if self.stop_flag:
                        break
                    self._turn_on_led(i)
                    if i > 0:  # Turn off the previous LED except for the first iteration
                        self._turn_off_led(i - 1)
                    time.sleep(.5)

                # Pause at the ends
                time.sleep(.5)

                # Move back to the starting ends
                for i in range(led_count - 2, -1, -1):
                    if self.stop_flag:
                        break
                    self._turn_on_led(i)
                    if i < led_count - 1:  # Turn off the next LED except for the last iteration
                        self._turn_off_led(i + 1)
                    time.sleep(.5)

                # Pause at the ends
                time.sleep(.5)

        finally:
            GPIO.cleanup()

    def _turn_on_led(self, index):
        """Turns on the LED for the given index, handling wraparound."""
        GPIO.output(self.led_pins[index % len(self.led_pins)], GPIO.HIGH)
        GPIO.output(self.led_pins[-(index % len(self.led_pins) + 1)], GPIO.HIGH)

    def _turn_off_led(self, index):
        """Turns off the LED for the given index, handling wraparound."""
        GPIO.output(self.led_pins[index % len(self.led_pins)], GPIO.LOW)
        GPIO.output(self.led_pins[-(index % len(self.led_pins) + 1)], GPIO.LOW)

# Define the GPIO pins connected to the LEDs.
led_pins = [26, 14, 17, 18, 23, 24, 27, 4]

# Create an instance of the class and start the animation.
animation = LEDPassingAnimation(led_pins)
animation.start()
