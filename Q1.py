
import RPi.GPIO as GPIO
import time
import threading

LEDs = [26, 14, 17, 18, 23, 24, 27, 4]
ON = GPIO.HIGH
OFF = GPIO.LOW
stop_flag = False

GPIO.setmode(GPIO.BCM)

for pin in LEDs:
    GPIO.setup(pin, GPIO.OUT)

def keyboard_input_listener():
    global stop_flag
    input("Press any key to stop...")
    stop_flag = True

def blink_leds():
    global stop_flag
    try:
        while not stop_flag:
            for pin in LEDs:
                if stop_flag:
                    break
                GPIO.output(pin, ON)
                time.sleep(1)
                GPIO.output(pin, OFF)
                time.sleep(1)
            
            for pin in reversed(LEDs):
                if stop_flag:
                    break
                GPIO.output(pin, ON)
                time.sleep(1)
                GPIO.output(pin, OFF)
                time.sleep(0.5)
    finally:
        GPIO.cleanup()

try:
    input_thread = threading.Thread(target=keyboard_input_listener)
    input_thread.start()
    
    blink_leds()
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")
finally:
    stop_flag = True
    if input_thread.is_alive():
        input_thread.join()
    # GPIO.cleanup() is removed here since it's already called in blink_leds() finally block.
