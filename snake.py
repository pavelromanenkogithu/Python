import curses
import random

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def opposite(a, b):
    return a[0] == -b[0] and a[1] == -b[1]

def spawn_food(snake, h, w):
    while True:
        y = random.randint(1, h - 2)
        x = random.randint(1, w - 2)
        if (y, x) not in snake:
            return (y, x)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    h, w = stdscr.getmaxyx()

    h = h - 2
    w = w - 2

    if h < 20 or w < 40:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small. Rotate screen / zoom out.")
        stdscr.refresh()
        stdscr.getch()
        return

    snake = [(h // 2, w // 2)]
    direction = RIGHT
    food = spawn_food(snake, h, w)
    score = 0

    while True:
        key = stdscr.getch()

        new_dir = direction

        if key == 27:
            break
        elif key in [curses.KEY_UP, ord('w')]:
            new_dir = UP
        elif key in [curses.KEY_DOWN, ord('s')]:
            new_dir = DOWN
        elif key in [curses.KEY_LEFT, ord('a')]:
            new_dir = LEFT
        elif key in [curses.KEY_RIGHT, ord('d')]:
            new_dir = RIGHT

        if not opposite(new_dir, direction):
            direction = new_dir

        head_y, head_x = snake[0]
        dy, dx = direction
        new_head = (head_y + dy, head_x + dx)

        if (
            new_head[0] <= 0 or new_head[0] >= h - 1 or
            new_head[1] <= 0 or new_head[1] >= w - 1 or
            new_head in snake
        ):
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = spawn_food(snake, h, w)
        else:
            snake.pop()

        stdscr.clear()

        for i in range(w):
            if 0 < h < curses.LINES:
                stdscr.addch(0, i, "#")
            if h - 1 > 0 and h - 1 < curses.LINES:
                stdscr.addch(h - 1, i, "#")

        for i in range(h):
            if i < curses.LINES:
                stdscr.addch(i, 0, "#")
                stdscr.addch(i, w - 1, "#")

        if 0 < food[0] < h and 0 < food[1] < w:
            stdscr.addch(food[0], food[1], "*")

        for i, (y, x) in enumerate(snake):
            if 0 < y < h and 0 < x < w:
                stdscr.addch(y, x, "O" if i == 0 else "o")

        stdscr.addstr(0, 2, f" Score: {score} ")

        stdscr.refresh()

    stdscr.nodelay(0)
    stdscr.clear()
    stdscr.addstr(min(h // 2, curses.LINES - 1), max(0, w // 2 - 5), "GAME OVER")
    stdscr.addstr(min(h // 2 + 1, curses.LINES - 1), max(0, w // 2 - 5), f"Score: {score}")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
