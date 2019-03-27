from dragonfly import Function, Choice, IntegerRef, Dictation, Repeat, MappingRule, Playback, Clipboard, Mimic, Key, Text, Grammar

# https://github.com/reckoner/pyVirtualDesktopAccessor
import os
from ctypes import cdll
from win32gui import GetForegroundWindow
def load_vda():
    return cdll.LoadLibrary(os.path.dirname(os.path.realpath(__file__)) + "\\VirtualDesktopAccessor.dll")

def window_to_desktop(n=1, follow=False):
    vda = load_vda()
    wndh = GetForegroundWindow()
    vda.MoveWindowToDesktopNumber(wndh, n-1)
    if follow:
        vda.GoToDesktopNumber(n-1)

def window_to_new_desktop(follow=False):
    vda = load_vda()
    wndh = GetForegroundWindow()
    current = vda.GetCurrentDesktopNumber()
    total = vda.GetDesktopCount()
    Key("wc-d").execute()
    vda.MoveWindowToDesktopNumber(wndh, total)
    if not follow:
        vda.GoToDesktopNumber(current)

def go_to_desktop_number(n):
    vda = load_vda()
    return vda.GoToDesktopNumber(n-1)

def close_all_workspaces():
    vda = load_vda()
    total = vda.GetDesktopCount()
    go_to_desktop_number(total)
    Key("wc-f4/10:" + str(total-1)).execute()


class WindowMgmt(MappingRule):
    mapping = {
        "show work [spaces]":
            Key("w-tab"),
        "(create | new) work [space]":
            Key("wc-d"),
        "close work [space]":
            Key("wc-f4"),
        "next work [space] [<n>]":
            Key("wc-right")*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]":
            Key("wc-left")*Repeat(extra="n"),

        "go work [space] <n>":
            Function(lambda n: go_to_desktop_number(n)),
        "send work [space] <n>":
            Function(lambda n: window_to_desktop(n)),
        "move work [space] <n>":
            Function(lambda n: window_to_desktop(n, True)),
        "send work [space] new":
            Function(window_to_new_desktop, follow=False),
        "move work [space] new":
            Function(window_to_new_desktop, follow=True),
        "close all work [spaces]":
            Function(close_all_workspaces),


        "window <direction> [<direction2>]":
            Key("win:down, %(direction)s/15, %(direction2)s, win:up"),
        "minimize":
            Playback([(["minimize", "window"], 0.0)]),
        "maximize":
            Playback([(["maximize", "window"], 0.0)]),
    }
    extras = [
        IntegerRef("n", 1, 20),
        Choice("direction", {
            "left" : "left",
            "right": "right",
            "up"   : "up",
            "down" : "down"}),
        Choice("direction2", {
            "left" : "left",
            "right": "right",
            "up"   : "up",
            "down" : "down"}),
    ]
    defaults = {"n": 1, "direction2": ""}

grammar = Grammar("Window management")
grammar.add_rule(WindowMgmt())
grammar.load()
