from typing import Final, Tuple, Callable
from functools import lru_cache

import pygame

ROW_COUNT: Final[int] = 15
COL_COUNT: Final[int] = 15

BACKGROUND_COLOR = (76, 86, 106)
CELL_COLOR = (94, 129, 172)
BORDER_COLOR = (235, 203, 139)

SCREEN_WIDTH_INIT: Final[int] = 1280
SCREEN_HEIGHT_INIT: Final[int] = 720

BORDER_THICK: Final[int] = 3

FPS: Final[int] = 10


def calcul_cell_size() -> Tuple[float]:
    cur_screen_width = screen.get_width()
    cur_screen_heigth = screen.get_height()

    cell_width = cur_screen_width / COL_COUNT
    cell_height = cur_screen_heigth / ROW_COUNT

    return (cell_width, cell_height)

@lru_cache
def get_cell_drawer(width, height) -> Callable:
    def draw_cell(x, y, is_not_empty) -> None:
        x_screen = x * width
        y_screen = y * height

        if is_not_empty:
            # -1 and +2 are the hack that fix diveded gap between two cells 
            rect = pygame.Rect(x_screen-1, y_screen-1, width+2, height+2)
            pygame.draw.rect(screen, color=CELL_COLOR, rect=rect)

    return draw_cell


@lru_cache
def get_border_drawer(width, height) -> Callable:
    def draw_cell(x, y) -> None:
        x_screen = x * width
        y_screen = y * height

        rect = pygame.Rect(x_screen-1, y_screen-1, width+2, height+2)
        pygame.draw.rect(screen, color=BORDER_COLOR, rect=rect, width=BORDER_THICK)

    return draw_cell


def init_empty_field() -> None:
    for i in range(ROW_COUNT):
        cells.append([])
        for _ in range(COL_COUNT):
            cells[i].append(False)


def init_start_value() -> None:
    cells[3][2] = True
    cells[3][3] = True
    cells[3][4] = True


def calcul_new_position() -> None:
    global cells 
    new_state = _get_new_state_cells()
    for i in range(ROW_COUNT):
        for j in range(COL_COUNT):
            neighbor_count = 0

            if i+1 < ROW_COUNT and cells[i+1][j]:
                neighbor_count += 1
            if i+1 < ROW_COUNT and j-1 > 0 and cells[i+1][j-1]:
                neighbor_count += 1
            if i+1 < ROW_COUNT and j+1 < COL_COUNT and cells[i+1][j+1]:
                neighbor_count += 1
            if i-1 > 0 and cells[i-1][j]:
                neighbor_count += 1
            if i-1 > 0 and j-1 > 0 and cells[i-1][j-1]:
                neighbor_count += 1
            if i-1 > 0 and j+1 < COL_COUNT and cells[i-1][j+1]:
                neighbor_count += 1
            if j-1 > 0 and cells[i][j-1]:
                neighbor_count += 1
            if j+1 < COL_COUNT and cells[i][j+1]:
                neighbor_count += 1

            if cells[i][j] and (neighbor_count == 3 or neighbor_count == 2):
                new_state[i][j] = True
            if not cells[i][j] and neighbor_count >= 3:
                new_state[i][j] = True

    cells = new_state


def _get_new_state_cells() -> list[list[bool]]:
    new_state: list[list[bool]] = []

    for i in range(ROW_COUNT):
        new_state.append([])
        for _ in range(COL_COUNT):
            new_state[i].append(False)

    return new_state

cells: list[list[bool]] = list(list())


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH_INIT, SCREEN_HEIGHT_INIT,), pygame.RESIZABLE)
clock = pygame.time.Clock()
is_running = True

init_empty_field()
init_start_value()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False            

    screen.fill(BACKGROUND_COLOR)
    width, heigth = calcul_cell_size()

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()

        x /= width
        y /= heigth

        col = int(x)
        row = int(y)

        cells[row][col] = not cells[row][col]


    drawer = get_cell_drawer(width=width, height=heigth)

    for i in range(len(cells)):
        for j in range(len(cells)):
            drawer(j, i, cells[i][j])

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_SPACE]:
        drawer = get_border_drawer(width=width, height=heigth)
        for i in range(len(cells)):
            for j in range(len(cells)):
                drawer(j, i)
        
        pygame.display.flip()
        clock.tick(FPS)
        continue

    calcul_new_position()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
