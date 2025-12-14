import pygame
import numpy as np

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.sounds = {}
        
    def create_tone(self, frequency, duration, wave_type='sine', volume=0.5):
        """Создание тона с различными формами волн"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        
        # Генерация временной шкалы
        t = np.linspace(0, duration, n_samples, endpoint=False)
        
        # Генерация различных форм волн
        if wave_type == 'sine':
            wave = np.sin(2 * np.pi * frequency * t)
        elif wave_type == 'square':
            wave = np.sign(np.sin(2 * np.pi * frequency * t))
        elif wave_type == 'sawtooth':
            wave = 2 * (t * frequency - np.floor(0.5 + t * frequency))
        elif wave_type == 'triangle':
            wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        else:
            wave = np.sin(2 * np.pi * frequency * t)
        
        envelope = np.ones(n_samples)
        attack = int(0.01 * sample_rate)  
        decay = int(0.1 * sample_rate)    
        
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[attack:attack+decay] = np.linspace(1, 0.3, decay)
        envelope[attack+decay:] = 0.3
        
        wave = wave * envelope
        

        wave = np.int16(wave * volume * 32767)
        

        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def play_eat(self):
        """Звук съедания еды"""
        sound = self.create_tone(800, 0.1, 'square', 0.3)
        sound.play()
        
    def play_crash(self):
        """Звук столкновения"""
        sound1 = self.create_tone(400, 0.15, 'sawtooth', 0.4)
        sound2 = self.create_tone(200, 0.15, 'sawtooth', 0.4)
        sound1.play()
        pygame.time.delay(50)
        sound2.play()
        
    def play_menu(self):
        """Звук меню"""
        sound = self.create_tone(600, 0.08, 'sine', 0.2)
        sound.play()