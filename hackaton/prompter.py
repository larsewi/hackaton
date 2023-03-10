from unicurses import *
import string

def select(prompt, choices):
    stdscr = initscr()
    clear()
    noecho()
    cbreak()
    curs_set(0)
    keypad(stdscr, True)
    refresh()

    highlight = 0
    filter = ""
    filtered = choices
    choice = None

    while True:
        clear()
        mvaddstr(0, 0, "? %s %s [Use arrows to move, type to filter]" % (prompt, filter))
        for i in range(len(filtered)):
            if highlight == i:
                attron(A_REVERSE)
                mvaddstr(i + 1, 0, "> %s" % filtered[i])
                attroff(A_REVERSE)
            else:
                mvaddstr(i + 1, 0, "  %s" % filtered[i])
        refresh()

        ch = getch()
        if ch == KEY_UP and len(filtered) > 0:
            highlight = (highlight - 1) % len(filtered)
        elif ch == KEY_DOWN and len(filtered) > 0:
            highlight = (highlight + 1) % len(filtered)
        elif ch in (10, KEY_RIGHT):
            if len(filtered) > 0:
                choice = filtered[highlight]
                break
        elif ch in (27, 4, KEY_LEFT):
            break
        elif chr(ch) in string.printable or ch == 127:
            filter = filter[:-1] if ch == 127 else filter + chr(ch)
            highlight = 0
            filtered = [c for c in choices if c.lower().startswith(filter.lower())]

    refresh()
    endwin()

    return choice