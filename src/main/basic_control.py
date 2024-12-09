from curses import wrapper

def main(stdscr):
    stdscr.clear()

    c = stdscr.getkey()

    if c == 'KEY_DOWN':
        stdscr.addstr(10, 2, 'key down detected')
    else:
        stdscr.addstr(10, 2, 'You pressed {}'.format(c))
        print("test")

    stdscr.refresh()
    stdscr.getkey()


wrapper(main)