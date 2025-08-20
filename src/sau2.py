import pygame
import random  # Add this import

try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for development on non-Pi systems
    class GPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        LOW = 0
        HIGH = 1

        @staticmethod
        def setmode(mode):
            print(f"Mock: GPIO.setmode({mode})")

        @staticmethod
        def setup(pin, mode, initial=None):
            print(f"Mock: GPIO.setup(pin={pin}, mode={mode}, initial={initial})")

        @staticmethod
        def output(pin, value):
            print(f"Mock: GPIO.output(pin={pin}, value={value})")


pygame.init()
pygame.mixer.init()


AUDIO_FOLDER = "../audio/bearbeitet/"

AUDIO_FILE_PIG = []
AUDIO_FILE_PIG.append("pig001.mp3")
AUDIO_FILE_PIG.append("pig002.mp3")

AUDIO_FILE_MUSIC = []
AUDIO_FILE_MUSIC.append("loop_001.mp3")
AUDIO_FILE_MUSIC.append("loop_002.mp3")
AUDIO_FILE_MUSIC.append("loop_003.mp3")
AUDIO_FILE_MUSIC.append("loop_004.mp3")
AUDIO_FILE_MUSIC.append("loop_005.mp3")
AUDIO_FILE_MUSIC.append("loop_007.mp3")

LED_PIN_SCHEINWERFER_L = 5
LED_PIN_SCHEINWERFER_R = 11

LED_PIN_BLINKER_HL = 13
LED_PIN_BLINKER_HR = 21
LED_PIN_BLINKER_VL = 6
LED_PIN_BLINKER_VR = 0

LED_PIN_RÜCKLICHT_L = 19
LED_PIN_RÜCKLICHT_R = 20

LED_PIN_BREMSE_L = 26
LED_PIN_BREMSE_R = 16

SENSOR_PIN_EINWURF_1 = 12
SENSOR_PIN_EINWURF_2 = 7

SENSOR_PIN_NASE = 18


try:
    # GPIO Setup
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers

    GPIO.setup(SENSOR_PIN_EINWURF_1, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(SENSOR_PIN_EINWURF_2, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

    GPIO.setup(LED_PIN_BLINKER_HL, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_BLINKER_HR, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_BLINKER_VL, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_BLINKER_VR, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_SCHEINWERFER_L, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_SCHEINWERFER_R, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_RÜCKLICHT_L, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_RÜCKLICHT_R, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_BREMSE_L, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_PIN_BREMSE_R, GPIO.OUT, initial=GPIO.LOW)
except Exception as e:
    print(f"Error setting up GPIO: {e}")
    GPIO.cleanup()
    exit(1)

def einwurf(channel):
        print("Einwurf erkannt")
        pygame.mixer.music.load(AUDIO_FOLDER + random.choice(AUDIO_FILE_MUSIC))  # Beispiel: Audio laden
        pygame.mixer.music.set_volume(1.0)  # Lautstärke einstellen (0.0 - 1.0)
        pygame.mixer.music.play(1)

GPIO.add_event_detect(SENSOR_PIN_EINWURF_1, GPIO.FALLING, callback=einwurf, bouncetime=10)
GPIO.add_event_detect(SENSOR_PIN_EINWURF_2, GPIO.FALLING, callback=einwurf, bouncetime=10)


try:
    print("Starte… (STRG+C zum Beenden)")
    while True:
        # Hier könnte die Hauptlogik des Programms stehen
        pygame.time.Clock().tick(10)  # Warten, um CPU-Last zu reduzieren
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Add GPIO cleanup
    pygame.mixer.quit()
    pygame.quit()