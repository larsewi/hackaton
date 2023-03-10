from unicurses import *
import string

KEY_CODE_DEL = 127
KEY_CODE_ENT = 10
KEY_CODE_EOF = 4
KEY_CODE_ESC = 27


def select(prompt, choices):
    stdscr = initscr()
    noecho()
    cbreak()
    curs_set(0)
    keypad(stdscr, True)

    highlight = 0
    filter = ""
    filtered = choices
    choice = None

    while True:
        # Draw menu
        clear()
        mvaddstr(
            0, 0, "? %s %s [Use arrows to move, type to filter]" % (prompt, filter)
        )
        for i in range(len(filtered)):
            if highlight == i:
                attron(A_REVERSE)
                mvaddstr(i + 1, 0, "> %s" % filtered[i])
                attroff(A_REVERSE)
            else:
                mvaddstr(i + 1, 0, "  %s" % filtered[i])
        refresh()

        # Handle input
        ch = getch()
        if ch == KEY_UP and len(filtered) > 0:
            # Move highlight up
            highlight = (highlight - 1) % len(filtered)
        elif ch == KEY_DOWN and len(filtered) > 0:
            # Move highlight down
            highlight = (highlight + 1) % len(filtered)
        elif ch in (KEY_CODE_ENT, KEY_RIGHT):
            # Select highlighted
            if len(filtered) > 0:
                choice = filtered[highlight]
                break
        elif ch in (KEY_CODE_ESC, KEY_CODE_EOF, KEY_LEFT):
            # Cancel selection
            break
        elif chr(ch) in string.printable or ch == KEY_CODE_DEL:
            # Filter results
            filter = filter[:-1] if ch == KEY_CODE_DEL else filter + chr(ch)
            highlight = 0
            filtered = [c for c in choices if c.lower().startswith(filter.lower())]

    endwin()
    return choice
