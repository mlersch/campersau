import pygame
import random
import threading
import time
import wave
import numpy as np
from scipy.io import wavfile
from scipy import signal

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
            print(f"Mock: GPIO.output(pin={pin}, value={value}")


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

# Add these global variables after existing imports
is_playing = False
blink_thread = None
current_bpm = 120  # default BPM

def analyze_bpm(audio_file):
    # Convert mp3 to wav temporarily for analysis
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play()
    pygame.mixer.music.stop()
    
    # Read audio file
    sample_rate, audio_data = wavfile.read(audio_file)
    
    # Convert stereo to mono if necessary
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    # Calculate tempo using onset detection
    tempo, beats = signal.beat.beat_track(y=audio_data, sr=sample_rate)
    return tempo

def random_light_show():
    global is_playing, current_bpm
    led_pins = [
        LED_PIN_SCHEINWERFER_L, LED_PIN_SCHEINWERFER_R,
        LED_PIN_BLINKER_HL, LED_PIN_BLINKER_HR,
        LED_PIN_BLINKER_VL, LED_PIN_BLINKER_VR,
        LED_PIN_RÜCKLICHT_L, LED_PIN_RÜCKLICHT_R,
        LED_PIN_BREMSE_L, LED_PIN_BREMSE_R
    ]
    
    beat_interval = 60.0 / current_bpm  # Calculate seconds per beat
    
    while is_playing:
        # Randomly select 1-4 LEDs to light up
        active_leds = random.sample(led_pins, random.randint(1, 4))
        
        # Turn on selected LEDs
        for pin in active_leds:
            GPIO.output(pin, GPIO.HIGH)
            
        # Wait for half a beat
        time.sleep(beat_interval * 0.5)
        
        # Turn off all LEDs
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
            
        # Wait for half a beat
        time.sleep(beat_interval * 0.5)

def einwurf(channel):
    global is_playing, blink_thread, current_bpm
    print("Einwurf erkannt")
    
    # Stop any existing light show
    is_playing = False
    if blink_thread and blink_thread.is_alive():
        blink_thread.join()
    
    # Select random music file
    music_file = AUDIO_FOLDER + random.choice(AUDIO_FILE_MUSIC)
    
    # Analyze BPM
    try:
        current_bpm = analyze_bpm(music_file)
        print(f"Detected BPM: {current_bpm}")
    except Exception as e:
        print(f"BPM detection failed, using default: {e}")
        current_bpm = 120
    
    # Start music
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(1)
    
    # Start light show in separate thread
    is_playing = True
    blink_thread = threading.Thread(target=random_light_show)
    blink_thread.start()
    
    # Set up a callback for when music ends
    pygame.mixer.music.set_endevent(pygame.USEREVENT)

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