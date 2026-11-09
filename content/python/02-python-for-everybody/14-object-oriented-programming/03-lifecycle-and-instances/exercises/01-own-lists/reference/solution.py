class Playlist:
    def __init__(self, name, tracks=None):
        self.name = name
        self.tracks = [] if tracks is None else list(tracks)

    def add(self, track):
        self.tracks.append(track)

    def __len__(self):
        return len(self.tracks)
