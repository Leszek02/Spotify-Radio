import RPi.GPIO as GPIO
import time
import serial
import json
from spotifyClass import SpotifyRequests

spotify = SpotifyRequests
# Set GPIO mode and setup
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for buttons
button_pins = [17, 22, 23, 24, 27]

# Setup the serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Change '/dev/ttyS0' to your actual serial port

# Setup the GPIO pins for input with pull-up resistors
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

response = spotify.classInterface("playbackStateRequest")
json_data = response.json()

repeat_state = json_data["repeat_state"]
shuffle_state = json_data["shuffle_state"]
is_playing = json_data["is_playing"]
prev_data = 0

try:
    print("Button Press Detection. Press Ctrl+C to exit.")

    while True:
        if GPIO.input(17) == GPIO.LOW:
            spotify.classInterface("skipToNextRequest")

        if GPIO.input(22) == GPIO.LOW:
            spotify.classInterface("skipToPreviousRequest")

        if GPIO.input(23) == GPIO.LOW:
            response = spotify.classInterface("playbackStateRequest")
            json_data = response.json()
            is_playing = json_data["is_playing"]
            if is_playing:
                spotify.classInterface("stopRequest")
            else:
                spotify.classInterface("playRequest")

        if GPIO.input(24) == GPIO.LOW:
            response = spotify.classInterface("playbackStateRequest")
            json_data = response.json()
            shuffle_state = json_data["shuffle_state"]
            spotify.classInterface("toggleShuffleRequest", not shuffle_state)

        if GPIO.input(27) == GPIO.LOW:
            response = spotify.classInterface("playbackStateRequest")
            json_data = response.json()
            repeat_state = json_data["repeat_state"]
            print(repeat_state)
            if (repeat_state == "off"):
                spotify.classInterface("repeatModeRequest", "context")
                print("context")
            else:
                spotify.classInterface("repeatModeRequest", "off")
                print("off")


        curr_data = ser.readline().decode('utf-8').strip()
        #print(curr_data)
        curr_data = int(curr_data)
        if abs(curr_data - prev_data) > 5:
            spotify.classInterface("changeVolumeRequest", curr_data)
            print(curr_data)
            prev_data = curr_data

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
