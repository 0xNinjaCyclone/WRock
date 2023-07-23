
import time


def banner():
    Print.normal( Color.Bold +
        """
            Fight Bugs                      |     |
                                            \\\_V_//
                                            \/=|=\/
                                             [=v=]
                                           __\___/_____
                                          /..[  _____  ]
                                         /_  [ [  M /] ]
                                        /../.[ [ M /{0}K{1}] ]
                                       <-->[_[ [M /{0}C{1}/] ]
                                      /../ [.[ [ /{0}O{1}/ ] ]
                 _________________]\ /__/  [_[ [/{0}R{1}/ C] ]
                <_________________>>0---]  [=\ \{0}W{1}/ C / /
                   ___      ___   ]/000o   /__\ \ C / /
                      \    /              /....\ \_/ /
                   ....\||/....           [___/=\___/
                  .    .  .    .          [...] [...]
                 .      ..      .         [___/ \___]
                 .    0 .. 0    .         <---> <--->
              /\/\.    .  .    ./\/\      [..]   [..]
             / / / .../|  |\... \ \ \    _[__]   [__]_
            / / /       \/       \ \ \  [____>   <____]
        """.format(Color.Red, Color.NC + Color.Bold)
    + Color.NC )


class Color:
    Red     = "\033[0;31m"
    Yellow  = "\033[0;33m"
    Green   = "\033[0;32m"
    Blue    = "\033[0;34m"
    Bold    = "\033[1m"
    NC      = "\033[0m"   # No Color


class Print:

    display = True

    @classmethod
    def show(cls, text="", endl = "\n", verbose = True):
        if Print.display and verbose:
            print(text, end = endl)

    @classmethod
    def normal(cls, text="", endl = "\n", startl = "", verbose = True):
        Print.show(f"{startl}{text}", endl, verbose)

    @classmethod
    def success(cls, text="", endl = "\n", startl = "", verbose = True):
        Print.show(f"{startl}{Color.Green}[+]{Color.NC} {text}", endl, verbose)

    @classmethod
    def status(cls, text="", endl = "\n", startl = "", verbose = True):
        Print.show(f"{startl}{Color.Blue}[*]{Color.NC} {text}", endl, verbose)

    @classmethod
    def fail(cls, text="", endl = "\n", startl = "", verbose = True):
        Print.show(f"{startl}{Color.Red}[-]{Color.NC} {text}", endl, verbose)

    @classmethod
    def warn(cls, text="", endl = "\n", startl = "", verbose = True):
        Print.show(f"{startl}{Color.Yellow}[!]{Color.NC} {text}", endl, verbose)

    @classmethod
    def highlight(cls, text="", endl = "\n", startl = "", verbose = True):
        Print.show(f"{Color.Bold}{startl}{text}{Color.NC}", endl, verbose)


class RockTime:
    
    def __init__(self) -> None:
        self.start_time = time.perf_counter()
        Print.highlight(f"Starting WebRock {time.ctime()}", endl="\n\n", startl="\n")

    def finish(self, mode):
        end_time = time.perf_counter() - self.start_time

        if float(end_time) >= 3600:
            t_format = "{0:0.2f}h".format(end_time / 3600)

        elif float(end_time) >= 60:
            t_format = "{0:0.2f}m".format(end_time / 60)

        else:
            t_format = "{0:0.2f}s".format(end_time)

        Print.highlight(f"Finished {mode} at {t_format}", startl="\n\n", endl="\n")
