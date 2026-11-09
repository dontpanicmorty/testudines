from solution import Playlist


def test_defaults_not_shared():
    a = Playlist("morning")
    b = Playlist("evening")
    a.add("song")
    assert len(a) == 1
    assert len(b) == 0


def test_starting_tracks():
    p = Playlist("mix", ["x", "y"])
    assert len(p) == 2
    assert p.name == "mix"


def test_caller_list_is_copied():
    source = ["x"]
    p = Playlist("mix", source)
    source.append("z")
    p.add("w")
    assert len(p) == 2
    assert source == ["x", "z"]
