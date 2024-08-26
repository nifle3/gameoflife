from typing import Final, Tuple

import pygame

ROW_COUNT: Final[int] = 15
COL_COUNT: Final[int] = 15

CELL_BORDER_SIZE: Final[int] = 3

SCREEN_WIDTH_INIT: Final[int] = 1280
SCREEN_HEIGHT_INIT: Final[int] = 720

FPS: Final[int] = 5


def calcul_cell_size() -> Tuple[float]:
    cur_screen_width = screen.get_width()
    cur_screen_heigth = screen.get_height()

    cell_width = cur_screen_width / COL_COUNT
    cell_height = cur_screen_heigth / ROW_COUNT

    return (cell_width, cell_height)


def get_cell_drawer(width, height):
    def draw_cell(x, y, is_not_empty) -> None:
        x_screen = x * width
        y_screen = y * height

        rect = pygame.Rect(x_screen, y_screen, width, height)
        pygame.draw.rect(screen, color=(255, 100, 100), rect=rect, width=CELL_BORDER_SIZE)
        if is_not_empty:
            inner_rect = pygame.Rect(x_screen+CELL_BORDER_SIZE, y_screen+CELL_BORDER_SIZE, width-CELL_BORDER_SIZE, height-CELL_BORDER_SIZE)
            pygame.draw.rect(screen, color=(255, 255, 255), rect=inner_rect)

    return draw_cell


def init_empty_field():
    for i in range(ROW_COUNT):
        cells.append([])
        for _ in range(COL_COUNT):
            cells[i].append(False)


def init_start_value():
    cells[3][2] = True
    cells[3][3] = True
    cells[3][4] = True


def calcul_new_position():
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
screen = pygame.display.set_mode((SCREEN_WIDTH_INIT, SCREEN_HEIGHT_INIT,))
clock = pygame.time.Clock()
is_running = True

init_empty_field()
init_start_value()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False      

    width, heigth = calcul_cell_size()
    drawer = get_cell_drawer(width=width, height=heigth)
    screen.fill('purple')

    for i in range(len(cells)):
        for j in range(len(cells)):
            drawer(j, i, cells[i][j])

    calcul_new_position()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()