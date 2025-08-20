import RPi.GPIO as GPIO
import time

PIN = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)  # externer Pull-Down!

def callback(channel):
    val = GPIO.input(PIN)

    if val:
        print("Hell erkannt")
    else:
        print("Dunkel erkannt")

GPIO.add_event_detect(PIN, GPIO.FALLING, callback=callback, bouncetime=10)

try:
    print("Starte… (STRG+C zum Beenden)")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
