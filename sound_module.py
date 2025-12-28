import pygame
import time

def play_alarm_sound(sound_file, duration=3):
    """Play the specified alarm sound for a set duration."""
    pygame.mixer.init()
    pygame.mixer.music.load('eye/test_sound.wav')
    
    pygame.mixer.music.play()
    start_time = time.time()
    
    
    while pygame.mixer.music.get_busy() and (time.time() - start_time) < duration:
        continue
        
    pygame.mixer.music.stop()  
