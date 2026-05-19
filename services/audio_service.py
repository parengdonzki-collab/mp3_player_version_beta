import pygame
from mutagen.mp3 import MP3


class AudioService:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.alive = True
    
  
    def play(self, song,):
        pygame.mixer.music.load(song.path)
        pygame.mixer.music.play()
        print("Playing:", song.title)

    def pause(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()

    def resume(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def quit(self):
        if self.alive:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            self.alive = False
    def set_volume(self, volume):

        pygame.mixer.music.set_volume(volume)
        
        
        
    def get_song_length(self, song):
        
        audio = MP3(song.path)
        
        return audio.info.length