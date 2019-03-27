from dragonfly import Function, Choice, IntegerRef, Dictation, Repeat, MappingRule, Playback, Clipboard, Mimic, Key, Text, Grammar

class Music(MappingRule):
    mapping = {
        "volume up [<n>]"     : Key("volumeup/5:%(n)d"),
        "volume down [<n>]"   : Key("volumedown/5:%(n)d"),
        "volume (mute|unmute)": Key("volumemute"),
        "music next"          : Key("tracknext"),
        "music previous"      : Key("trackprev"),
        "music (pause|play)"  : Key("playpause"),
    }
    extras = [
        IntegerRef("n", 1, 20),
    ]
    defaults = {"n": 1}

grammar = Grammar("Music")
grammar.add_rule(Music())
grammar.load()
