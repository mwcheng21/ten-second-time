import pygame


class MusicPlayer():
    def __init__(self, song):
        pygame.mixer.init()
        self.player = pygame.mixer.music
        self.song = song

    @staticmethod
    def click():
        pygame.mixer.Sound("assets/audio/select_001.ogg").play()

    @staticmethod
    def hover():
        pygame.mixer.Sound("assets/audio/select_001.ogg").play()

    @staticmethod
    def play_jump():
        pygame.mixer.Sound("assets/audio/whoosh.mp3").play()

    @staticmethod
    def play_switch():
        pygame.mixer.Sound("assets/audio/select_001.ogg").play()

    @staticmethod
    def play_dash():
        pygame.mixer.Sound("assets/audio/whoosh.mp3").play()

    @staticmethod
    def play_powerup():
        pygame.mixer.Sound("assets/audio/confirmation_001.ogg").play()
    
    @staticmethod
    def stop():
        pygame.mixer.music.stop()

    def play(self, loops=-1, start_time=0.0, fade_ms=0):
        self.player.play(loops, start_time, fade_ms)

    def pause(self):
        self.player.pause()

    def unpause(self):
        self.player.unpause()

    def fadeout(self, time):
        self.player.fadeout(time)

    def set_volume(self, volume):
        self.player.set_volume(volume)

    def get_volume(self):
        return self.player.get_volume()

    def is_playing(self):
        return self.player.get_busy()

    def reset(self):
        self.player.stop()
        self.player.unload()
        self.player = pygame.mixer.music
        self.player.load(self.song)
