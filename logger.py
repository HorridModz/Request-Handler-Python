"""
Custom logger by me, since I'm not a fan of the standard logging module
"""

import os
import json
from enum import Enum
from colorama import just_fix_windows_console

__all__ = ["LoggingLevel", "Logging", "logging"]


class LoggingLevel(Enum):
    Debug = 1
    Info = 2
    Important = 3
    VeryImportant = 4
    SuperImportant = 5
    Warning = 6


class Logging:

    def __init__(self, usedefaults=True, **kwargs):
        if usedefaults:
            self._fromoptions(**_loadconfig())
        else:
            self._fromoptions(**kwargs)

    def _fromoptions(self,
                     colorized=True,
                     printwarnings=True,
                     printdebug=False,
                     printinfo=True,
                     printimportant=True,
                     printveryimportant=True,
                     printsuperimportant=True,
                     printspecial=True,
                     donotprintspecial=False,
                     donotprintsuccessinfo=False,
                     allowoverride=True,
                     printall=True,
                     printnone=False
                     ):
        self.colorized = colorized
        self.printwarnings = printwarnings
        self.printdebug = printdebug
        self.printinfo = printinfo
        self.printimportant = printimportant
        self.printveryimportant = printveryimportant
        self.printsuperimportant = printsuperimportant
        self.printspecial = printspecial
        self.donotprintspecial = donotprintspecial
        self.donotprintsuccessinfo = donotprintsuccessinfo
        self.allowoverride = allowoverride
        self.printall = printall
        self.printnone = printnone
        self.Log = []

    def log(self, message: str, level: LoggingLevel = LoggingLevel.Info, override=False, successinfo=False,
            special=False):
        self.Log.append(message)
        if self.printnone:
            return
        if not (override and self.allowoverride):
            if successinfo and self.donotprintsuccessinfo:
                return
            if special and self.donotprintspecial:
                return
        if self.printall:
            toprint = True
        elif level == LoggingLevel.Debug and self.printdebug:
            toprint = True
        elif level == LoggingLevel.Info and self.printinfo:
            toprint = True
        elif level == LoggingLevel.Important and self.printimportant:
            toprint = True
        elif level == LoggingLevel.VeryImportant and self.printveryimportant:
            toprint = True
        elif level == LoggingLevel.SuperImportant and self.printsuperimportant:
            toprint = True
        elif special and self.printspecial:
            toprint = True
        else:
            toprint = False
        if toprint:
            self.printmessage(message, level, special, self.colorized)

    def printlog(self):
        print(self.Log)

    @staticmethod
    def printmessage(message: str, level: LoggingLevel, special, colorized):
        colors = {
            "Debug": "\033[0m",
            "Info": "\033[94m",
            "Important": "\033[95m",
            "VeryImportant": "\033[96m",
            "SuperImportant": "\033[93m",
            "Warning": "\033[91m",
            "Special": "\033[92m",
            "reset": "\033[0m"
        }
        if colorized:
            if special:
                print(f"{colors['Special']}[{level.name}] [Special]: {message}{colors['reset']}")
            else:
                if level.name in colors:
                    print(f"{colors[level.name]}[{level.name}]: {message}{colors['reset']}")
                else:
                    print(f"[{level.name}]: {message}")
        else:
            if special:
                print(f"[{level.name}] [Special]: {message}")
            else:
                print(f"[{level.name}]: {message}")

    def warning(self, message: str, warningtype=None):
        if warningtype:
            self.Log.append(f"[Warning]: {warningtype}: {message}")
            if self.printwarnings:
                self.printmessage(f"{warningtype}: {message}", LoggingLevel.Warning, False, self.colorized)
        else:
            self.Log.append(f"[Warning]: {message}")
            if self.printwarnings:
                self.printmessage(message, LoggingLevel.Warning, False, self.colorized)


def _loadconfig():
    configpath = os.path.join(os.path.dirname(__file__), "loggingconfig.json")
    with open(configpath, "r") as f:
        return json.load(f)


def _writeconfig(**kwargs):
    """
    This is a neat trick that allows me to write logging options to the config file just by calling
    this function with the options as arguments!
    """
    configpath = os.path.join(os.path.dirname(__file__), "loggingconfig.json")
    with open(configpath, "w") as f:
        json.dump(kwargs, f, indent=4)


if __name__ != "__main__":
    just_fix_windows_console()
    logging = Logging(usedefaults=True)

if __name__ == "__main__":
    _writeconfig(colorized=True,
                 printwarnings=True,
                 printdebug=False,
                 printinfo=True,
                 printimportant=True,
                 printveryimportant=True,
                 printsuperimportant=True,
                 printspecial=True,
                 donotprintspecial=False,
                 donotprintsuccessinfo=False,
                 allowoverride=True,
                 printall=True,
                 printnone=False
                 )
