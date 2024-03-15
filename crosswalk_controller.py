import RPi.GPIO as GPIO
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # You made this? I made this :)
import pygame
import threading
import mutagen.mp3
import random

class CrosswalkController:
    def __init__(self):
        self.timer_called = False
        try:
            self.init_gpio()
            self.play_random_ambiance()
            self.hang()
        finally:
            self.cleanup()
            self.stop_music()
            self.print("Goodbye friend!")

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(21, GPIO.BOTH, callback=self.GPIO_callback)
        GPIO.output(20, GPIO.HIGH)

    def play_music(self, song):
        print(f"Playing {song}")
        song = "sound/" + song
        mp3 = mutagen.mp3.MP3(song)
        pygame.mixer.init(frequency=mp3.info.sample_rate)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

    def play_random_ambiance(self):
        ambiance = ["ambiance_1.mp3", "ambiance_2.mp3", "ambiance_3.mp3"]
        song = random.choice(ambiance)
        print(f"Playing {song}")
        song = "sound/" + song
        mp3 = mutagen.mp3.MP3(song)
        pygame.mixer.init(frequency=mp3.info.sample_rate)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=-1)

    def stop_music(self):
        pygame.mixer.music.stop()
        print("Stopping song")

    def waiting_timer_callback(self):
        threading.Timer(9, self.crossing_timer_callback).start()
        self.print("Wow a car has stopped!")
        self.play_music("voiture_arret_depart_crop.mp3")

    def crossing_timer_callback(self):
        threading.Timer(8, self.car_timer_callback).start()
        self.print("You should cross.")
        GPIO.output(20, GPIO.LOW)

    def car_timer_callback(self):
        threading.Timer(5, self.idle_timer_callback).start()
        self.print("You should not cross!")
        GPIO.output(20, GPIO.HIGH)
        self.play_random_ambiance()

    def idle_timer_callback(self):
        self.timer_called = False
        self.print("Traffic light has finished its break, you can press the button again.")

    def GPIO_callback(self, channel):
        if GPIO.input(channel) == GPIO.HIGH:
            if not self.timer_called:
                self.print("Wait before crossing.")
                threading.Timer(5, self.waiting_timer_callback).start()
                self.timer_called = True

    def cleanup(self):
        GPIO.cleanup()

    def print(self, msg):
        print(msg + " :)")

    def hang(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.print("Received keyboard interrupt.")

def main():
    crosswalk_controller = CrosswalkController()

if __name__ == "__main__":
    main()
