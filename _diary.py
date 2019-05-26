from dragonfly import Function, Choice, IntegerRef, Dictation, Repeat, MappingRule, Playback, Clipboard, Mimic, Key, Text, Grammar
from subprocess import Popen
import datetime

DIARY_PATH = "C:/Users/Mike/Documents/notes/"
TITLE      = "Notes - Mike Roberts"

def diary():
    now = datetime.datetime.now()
    datestr = "%s-%s-%s" % (now.year, now.month, now.day)
    path = "%s%s.md" % (DIARY_PATH, datestr)
    if not os.path.isfile(path):
        with open(path, "w+") as f:
            f.write(title = "# %s - %s\n" % (datestr, TITLE))
    Popen(["notepad", path])

class Diary(MappingRule):
    mapping = {
        "open diary": Function(diary),
    }

grammar = Grammar("Diary")
grammar.add_rule(Diary())
grammar.load()