#!/usr/bin/env python3
import curses
from random import randint


def main():
    """Main"""
    # set up the window
    screen = curses.initscr()
    curses.curs_set(0)
    n_rows, n_cols = screen.getmaxyx()
    win = curses.newwin(n_rows, n_cols, 0, 0)
    win.keypad(1)
    win.timeout(100)

    # draw a game boundary
    boundary_char = '#'
    boarder_top, boarder_bottom = 3, n_rows - 2
    boarder_left, boarder_right = 1, n_cols - 2
    board_h, board_w = boarder_bottom - boarder_top, boarder_right - boarder_left
    for x in range(boarder_left, boarder_right + 1):
        win.addch(boarder_top, x, boundary_char)
        win.addch(boarder_bottom, x, boundary_char)
    for y in range(boarder_top, boarder_bottom + 1):
        win.addch(y, boarder_left, boundary_char)
        win.addch(y, boarder_right, boundary_char)

    # initialize the snake
    snake_y, snake_x = board_h // 2, board_w // 4
    snake = [[snake_y, snake_x], [snake_y, snake_x - 1], [snake_y, snake_x - 2]]

    # set the first food location
    food = [board_h // 2, board_w // 2]
    win.addch(food[0], food[1], curses.ACS_PI)

    # set the initial movement direction
    key = curses.KEY_RIGHT

    # initialize the score
    score = 0
    score_y, score_x = 1, 2
    win.addstr(score_y, score_x, f"Score: {score}")

    # main game loop
    while True:
        # get the next key press
        next_key = win.getch()
        key = key if next_key == -1 else next_key

        # modify the snake movement direction
        new_head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        snake.insert(0, new_head)

        # check for game ending collisions with the wall and snake
        if (
            snake[0][0] in [boarder_top, boarder_bottom] or
            snake[0][1] in [boarder_left, boarder_right] or
            snake[0] in snake[1:]
        ):
            return

        # check for food consumption and move the snake
        if snake[0] == food:
            food = None
            while food is None:
                nf = [randint(boarder_top + 1, boarder_bottom - 1),
                      randint(boarder_left + 1, boarder_right - 1)]
                food = nf if nf not in snake else None
            win.addch(food[0], food[1], curses.ACS_PI)

            # modify the score display
            score += 1
            win.addstr(score_y, score_x, f"Score: {score}")
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')
        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)


if __name__ == '__main__':
    try:
        main()
    except:
        pass

    # cleanup
    curses.napms(300)
    curses.endwin()
