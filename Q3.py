
import RPi.GPIO as GPIO
import time
import threading

# Define the GPIO pins connected to the LEDs.
LEDs = [26, 14, 17, 18, 23, 24, 27, 4]
ON = GPIO.HIGH
OFF = GPIO.LOW

# Initialize GPIO
def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    for pin in LEDs:
        GPIO.setup(pin, GPIO.OUT)

# Function to clean up GPIO
def cleanup_GPIO():
    GPIO.cleanup()

# Function to control the blinking of LEDs
def blink_leds(stop_event):
    try:
        while not stop_event.is_set():
            # Starting from the center and moving outwards
            half = len(LEDs) // 2
            for offset in range(half):
                left_index, right_index = half - offset - 1, half + offset
                GPIO.output(LEDs[left_index], ON)
                GPIO.output(LEDs[right_index], ON)
                time.sleep(1)  # Adjust timing as needed
                GPIO.output(LEDs[left_index], OFF)
                GPIO.output(LEDs[right_index], OFF)
                time.sleep(0.3)  # Adjust timing as needed

            # Optional: Reverse direction - from the ends back to the center
            for offset in reversed(range(half)):
                left_index, right_index = half - offset - 1, half + offset
                GPIO.output(LEDs[left_index], ON)
                GPIO.output(LEDs[right_index], ON)
                time.sleep(1)  # Adjust timing as needed
                GPIO.output(LEDs[left_index], OFF)
                GPIO.output(LEDs[right_index], OFF)
                time.sleep(0.3)  # Adjust timing as needed

    finally:
        cleanup_GPIO()

# Main function to start the program
def main():
    setup_GPIO()
    stop_event = threading.Event()
    thread = threading.Thread(target=blink_leds, args=(stop_event,))
    
    try:
        thread.start()
        input("Press Enter to stop...")
        stop_event.set()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        stop_event.set()
        thread.join()

if __name__ == "__main__":
    main()
