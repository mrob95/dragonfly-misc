from dragonfly import Function, Choice, IntegerRef, Dictation, Repeat, MappingRule, Playback, Clipboard, Mimic, Key, Text, Grammar

from subprocess import Popen

def read_selected(same_is_okay=False):
    '''Returns a tuple:
    (0, "text from system") - indicates success
    (1, None) - indicates no change
    (2, None) - indicates clipboard error
    '''
    time.sleep(SETTINGS["keypress_wait"])
    cb = Clipboard(from_system=True)
    temporary = None
    prior_content = None
    try:
        prior_content = Clipboard.get_system_text()
        Clipboard.set_system_text("")
        Key("c-c").execute()
        time.sleep(SETTINGS["keypress_wait"])
        temporary = Clipboard.get_system_text()
        cb.copy_to_system()
    except Exception:
        return 2, None
    if prior_content == temporary and not same_is_okay:
        return 1, None
    return 0, temporary

BROWSER_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"

def browser_open(url):
    Popen([BROWSER_PATH, url])

def browser_search(text=None, url):
    if not text:
        _, selection = read_selected(True)
        selection = ''.join(i for i in selection if ord(i)<128)
    else:
        selection = str(text)
    url = url % selection.replace(" ", "+").replace("\n", "")
    browser_open(url)

class Search(MappingRule):
    mapping = {
        "<search> that":
            Function(lambda search: utilities.browser_search(url=search)),
        "<search> <dict>":
            Function(lambda search, dgndictation: utilities.browser_search(dgndictation, url=search)),
    }
    extras = [
        Dictation("dgndictation"),
        Choice("search", {
            "amazon"   : "https://smile.amazon.co.uk/s?k=%s",
            "kindle"   : "https://smile.amazon.co.uk/s?k=%s&rh=n%%3A341689031",
            "wikipedia": "https://en.wikipedia.org/w/index.php?search=%s",
            "google"   : "https://www.google.com/search?q=%s",
            }),
    ]
    defaults = {"n": 1}

grammar = Grammar("Search")
grammar.add_rule(Search())
grammar.load()
