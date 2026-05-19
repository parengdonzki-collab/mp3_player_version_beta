class PlaylistModel():
    def __init__(self):
        self.songs=[]
        self.current_index = -1
    
    def add_song(self, song):
        
        if song not in self.songs:
            self.songs.append(song)
    def get_current_song(self):
        if 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
        return None
    def next_song(self):
        if not self.songs:
            return None
        
        self.current_index += 1
        
        if self.current_index >= len(self.songs):
            self.current_index = 0
        return self.get_current_song()
    
    
        
        
