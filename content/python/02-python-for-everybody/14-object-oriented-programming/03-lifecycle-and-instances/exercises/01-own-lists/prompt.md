Define `Playlist(name, tracks=None)`.

- `tracks` is an optional starting list of track names. Each playlist keeps its **own** list, and later changes to the list passed in must not alter the playlist.
- `add(track)` appends a track.
- `__len__` is supported, so `len(playlist)` gives the number of tracks.

```python
a = Playlist("morning")
b = Playlist("evening")
a.add("song")
len(b)    # 0
```
