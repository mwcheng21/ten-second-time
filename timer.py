import time
import pygame

# Times how long it takes to complete task
class Timer():
    def __init__(self):
        self.reset()
        self.multiplier = 1
        self.removed_time = 0

    def start(self):
        assert not self.isRunning
        self.start_time = time.time()
        self.isRunning = True

    def stop(self):
        assert self.isRunning
        self.running_time += time.time() - self.start_time
        self.isRunning = False

    def toggle(self):
        if self.isRunning:
            self.stop()
        else:
            self.start()

    def get_running_time(self):
        real_running_time = self.running_time if not self.isRunning else self.running_time + time.time() - self.start_time
        return real_running_time * self.multiplier - self.removed_time
    
    def reset(self):
        self.running_time = 0
        self.isRunning = False


    def slow_down(self, multiplier):
        self.multiplier = self.multiplier * multiplier

    @staticmethod
    def time_to_str(time_in_seconds: float) -> str:
        neg = False
        if time_in_seconds < 0:
            neg = True
            time_in_seconds = abs(time_in_seconds)
        minutes = str(int(time_in_seconds / 60))
        seconds = str(int(time_in_seconds % 60))
        milliseconds = str(int((time_in_seconds - int(time_in_seconds)) * 100))
        return f"{'-' if neg else ''}{minutes}:{seconds.zfill(2)}.{milliseconds.zfill(2)}"

class PygameTimer():
    def __init__(self, cooldown):
        self.last = pygame.time.get_ticks()
        self.cooldown = cooldown    

    def fire(self):
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            return True
        return False

    def reset(self):
        self.last = pygame.time.get_ticks()