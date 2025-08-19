import pygame

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


AUDIO_FOLDER = "../audio/"

AUDIO_FILE_PIG = []
AUDIO_FILE_PIG.append("pig001.mp3")
AUDIO_FILE_PIG.append("pig002.mp3")

AUDIO_FILE_MUSIC = []
AUDIO_FILE_MUSIC.append("music001.mp3") 
AUDIO_FILE_MUSIC.append("music002.mp3")

LED_PIN_SCHEINWERFER_L = 12
LED_PIN_SCHEINWERFER_R = 13

LED_PIN_BLINKER_HL = 17
LED_PIN_BLINKER_HR = 27
LED_PIN_BLINKER_VL = 22
LED_PIN_BLINKER_VR = 23

LED_PIN_RÜCKLICHT_L = 5
LED_PIN_RÜCKLICHT_R = 6

LED_PIN_BREMSE_L = 24
LED_PIN_BREMSE_R = 25

SENSOR_PIN_EINWURF_1 = 16
SENSOR_PIN_EINWURF_2 = 26

SENSOR_PIN_NASE = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
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


# Funktion zum Setzen der Blinker
def set_blinker(state, direction):
    if direction == 'HL':
        GPIO.output(LED_PIN_BLINKER_HL, state)
    elif direction == 'HR':
        GPIO.output(LED_PIN_BLINKER_HR, state)
    elif direction == 'VL':
        GPIO.output(LED_PIN_BLINKER_VL, state)
    elif direction == 'VR':
        GPIO.output(LED_PIN_BLINKER_VR, state)


try:
    print(AUDIO_FOLDER + AUDIO_FILE_PIG[0])
    pygame.mixer.music.load(AUDIO_FOLDER + AUDIO_FILE_PIG[0])  # Beispiel: Erstes Pig Audio laden
    pygame.mixer.music.set_volume(1.0)  # Lautstärke einstellen (0.0 - 1.0)
    pygame.mixer.music.play(10)

    # Optional: Warten, bis die Musik fertig ist
    while pygame.mixer.music.get_busy():
        print(".")
        pygame.time.Clock().tick(10)

except pygame.error:
    print("Fehler beim Laden oder Abspielen der Musik")
finally:
    pygame.mixer.quit()
    pygame.quit()