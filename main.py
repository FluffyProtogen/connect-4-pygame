import sys
import pygame
from enum import Enum
import math

pygame.init()
Color = Enum('Color', ['RED', 'YELLOW'])
grid = [[None for x in range(7)] for y in range(6)]

red_turn = True
clicked_last_frame = False

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
yellow = 255, 238, 0

screen_size = 600, 600

ROW_HEIGHT = 500 / 6
COLUMN_WIDTH = 600 / 7

small_font = pygame.font.SysFont(None, 75)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Tic Tac Toe")


def draw_board(screen, grid):
    pygame.draw.line(screen, black, (0, 100), (600, 100), 5)

    for i in range(5):
        pygame.draw.line(screen, black, (0, 100 + (i + 1) * ROW_HEIGHT),
                         (600, 100 + (i + 1) * ROW_HEIGHT), 5)
    for i in range(6):
        pygame.draw.line(screen, black, ((i + 1) * COLUMN_WIDTH,
                         700), ((i + 1) * COLUMN_WIDTH, 100), 5)

    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            if item != None:
                color = red if item == Color.RED else yellow
                pygame.draw.circle(
                    screen, color, (x * COLUMN_WIDTH + COLUMN_WIDTH / 2, 100 + y * ROW_HEIGHT + ROW_HEIGHT / 2), 40)

                # add sin timer for glow on placeable tiles


def is_valid_tile(x, y, grid):
    if grid[y][x] == None:
        if y < 5:
            if grid[y + 1][x] != None:
                return True
        else:
            return True
    else:
        return False


def lerp(a, b, t):
    return a + (b - a) * t


def highlight_placeable_tiles(screen, grid, red_turn):
    sine = (math.sin(pygame.time.get_ticks() / 240) + 1) / 2

    if red_turn:
        color = lerp(252, 255, sine), lerp(
            111, 255, sine), lerp(101, 255, sine)
    else:
        color = 255, lerp(238, 255, sine), lerp(10, 255, sine)

    for x in range(7):
        for y in range(6):
            if is_valid_tile(x, y, grid):
                pygame.draw.rect(screen, color, pygame.Rect(
                    x * COLUMN_WIDTH, 100 + y * ROW_HEIGHT, COLUMN_WIDTH, ROW_HEIGHT))
                break


def has_won(grid):
    for x in range(7):
        for y in range(3):
            if grid[y][x] == grid[y + 1][x] == grid[y + 2][x] == grid[y + 3][x] != None:
                return True

    for y in range(6):
        for x in range(4):
            if grid[y][x] == grid[y][x + 1] == grid[y][x + 2] == grid[y][x + 3] != None:
                return True

    for x in range(4):
        for y in range(3):
            if grid[y][x] == grid[y + 1][x + 1] == grid[y + 2][x + 2] == grid[y + 3][x + 3] != None:
                return True
            elif grid[5 - y][6 - x] == grid[4 - y][5 - x] == grid[3 - y][4 - x] == grid[2 - y][3 - x] != None:
                return True

    return False


def retry_pressed(screen, clicked_this_frame):
    rect = pygame.draw.rect(screen, black, [380, 15, 200, 70])
    retry_text = small_font.render("Retry", True, white)
    screen.blit(retry_text, (410, 28))
    if clicked_this_frame and rect.collidepoint(pygame.mouse.get_pos()):
        return True
    else:
        return False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(white)

    click = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()

    clicked_this_frame = click and not clicked_this_frame
    clicked_last_frame = click

    if has_won(grid):
        text = "Yellow" if red_turn else "Red"
        win_text = small_font.render(
            f"{text} Won!", True, yellow if red_turn else red)
        screen.blit(win_text, (20, 30))
    else:
        if clicked_this_frame:
            grid_x = int(mouse_x // COLUMN_WIDTH)
            grid_y = int((mouse_y - 100) // ROW_HEIGHT)

            if is_valid_tile(grid_x, grid_y, grid):
                if red_turn:
                    grid[grid_y][grid_x] = Color.RED
                else:
                    grid[grid_y][grid_x] = Color.YELLOW
                red_turn = not red_turn
        highlight_placeable_tiles(screen, grid, red_turn)
    draw_board(screen, grid)

    if retry_pressed(screen, clicked_this_frame):
        grid = [[None for x in range(7)] for y in range(6)]
        red_turn = True

    pygame.display.flip()
