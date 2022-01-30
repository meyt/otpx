import curses


class CliScreen:
    def __init__(self):
        self.rowidx = 0
        self.stdscr = None

    def start(self):
        self.stdscr = curses.initscr()

    def end(self, *_, **__):
        if not self.stdscr:
            return
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def addline(self, ch):
        _, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(self.rowidx, 0, ch * width)
        self.rowidx += 1

    def addrow(self, val, colwidths=None):
        _, width = self.stdscr.getmaxyx()
        if colwidths:
            val = "".join(
                map(
                    lambda x: str(x[1])[: colwidths[x[0]]].ljust(
                        colwidths[x[0]] + 1
                    ),
                    enumerate(val),
                )
            )
        self.stdscr.addstr(self.rowidx, 0, val.ljust(width))
        self.rowidx += 1

    def fillrows(self):
        height, width = self.stdscr.getmaxyx()
        for y in range(self.rowidx, height - 1):
            self.stdscr.addstr(y, 0, " " * width)

    def refresh(self):
        self.stdscr.refresh()
        self.fillrows()
        self.rowidx = 0
