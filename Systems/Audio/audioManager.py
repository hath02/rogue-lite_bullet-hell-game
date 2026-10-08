import pygame
    
class AudioManager:
    class Channel:
        MUSIC = 0
        AMBIENT = 1
        
        SPELL_START = 2
        SPELL_END = 7
        
        UI = 8
        
        TOTAL = 9
        
    def __init__(self):
        self.sounds = {}

        # Volumes
        self.music_volume = 1.0
        self.ambient_volume = 1.0
        self.sfx_volume = 1.0
        self.ui_volume = 1.0
        
        # Channels
        self.music_channel = pygame.mixer.Channel(
            self.Channel.MUSIC
        )
        
        self.ambient_channel = pygame.mixer.Channel(
            self.Channel.AMBIENT
        )
        
        self.ui_channel = pygame.mixer.Channel(
            self.Channel.UI
        )
        
        # Spell channels pool
        self.spell_channels = [
            pygame.mixer.Channel(i)
            for i in range(
                self.Channel.SPELL_START,
                self.Channel.SPELL_END + 1
            )
        ]

    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    # SPELLS
    def play_spell(self, name, loop = False):
        
        sound = self.sounds.get(name)
        
        if sound is None:
            return None
        
        sound.set_volume(self.sfx_volume)
        
        loops = -1 if loop else 0
        
        for channel in self.spell_channels:
            if not channel.get_busy():
                channel.play(
                    sound,
                    loops = loops
                )
                
                return channel
        
        # No free channel
        return None
    
    def stop_spell(self, channel):
        if channel is not None:
            channel.stop()
            
    def pause_spell(self, channel):
        if channel is not None:
            channel.pause()  
            
    def resume_spell(self, channel):
        if channel is not None:
            channel.unpause()      

    # MUSIC
    def play_music(self, path, loop = True):
        
        music = pygame.mixer.Sound(path)
        music.set_volume(self.music_volume)
        
        loops = -1 if loop else 0
        
        self.music_channel.play(
            music,
            loops = loops
        )

    def stop_music(self):
        self.music_channel.stop()

    def pause_music(self):
        self.music_channel.pause()

    def resume_music(self):
        self.music_channel.unpause()

    # AMBIENT
    def play_ambient(self, path, loop = True):
        
        ambient = pygame.mixer.Sound(path)
        ambient.set_volume(self.ambient_volume)
        
        loops = -1 if loop else 0
        
        self.ambient_channel.play(
            ambient,
            loops = loops
        )
        
    def stop_ambient(self):
        self.ambient_channel.stop()
        
    def pause_ambient(self):
        self.ambient_channel.pause()
        
    def resume_ambient(self):
        self.ambient_channel.unpause()
        
    # UI
    def play_ui(self, name):
        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(self.ui_volume)
            
            self.ui_channel.play(sound)
            
    # VOLUME
    def set_music_volume(self, volume):
        self.music_volume = volume
        self.music_channel.set_volume(volume)
        
    def set_ambient_volume(self, volume):
        self.ambient_volume = volume
        self.ambient_channel.set_volume(volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        
        for channel in self.spell_channels:
            channel.set_volume(volume)
        
    def set_ui_volume(self, volume):
        self.ui_volume = volume