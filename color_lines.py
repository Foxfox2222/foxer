import pygame
import random

# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 450, 450
CELL_SIZE = WIDTH // 9

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Lines 98")

# Частота обновления экрана
clock = pygame.time.Clock()
FPS = 60

# Игровое поле — 9x9 клеток
grid = [[None for _ in range(9)] for _ in range(9)]

# Класс для шара
class Ball:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (self.pos[0] * CELL_SIZE + CELL_SIZE // 2, 
                            self.pos[1] * CELL_SIZE + CELL_SIZE // 2), 
                           CELL_SIZE // 3)

# Функция для отрисовки игрового поля
def draw_grid():
    for row in range(9):
        for col in range(9):
            pygame.draw.rect(screen, WHITE, 
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Добавление новых шаров
def add_new_balls(grid, count=3):
    empty_cells = [(r, c) for r in range(9) for c in range(9) if grid[r][c] is None]
    for _ in range(count):
        if empty_cells:
            row, col = random.choice(empty_cells)
            grid[row][col] = Ball(random.choice(COLORS), (col, row))
            empty_cells.remove((row, col))

# Логика перемещения шара
selected_ball = None

def handle_click(pos):
    global selected_ball
    row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE

    if selected_ball:
        if grid[row][col] is None:
            grid[row][col] = Ball(selected_ball.color, (col, row))
            grid[selected_ball.pos[1]][selected_ball.pos[0]] = None
            selected_ball = None
            add_new_balls(grid)
        else:
            selected_ball = None
    elif grid[row][col]:
        selected_ball = grid[row][col]

# Обработка событий
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())
    return True

# Проверка формирования линий
def check_lines(grid):
    def check_direction(start, direction):
        r, c = start
        dr, dc = direction
        color = grid[r][c].color
        count = 0
        line = []

        while 0 <= r < 9 and 0 <= c < 9 and grid[r][c] and grid[r][c].color == color:
            count += 1
            line.append((r, c))
            r += dr
            c += dc

        return line if count >= 5 else []

    for row in range(9):
        for col in range(9):
            if grid[row][col]:
                for direction in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    line = check_direction((row, col), direction)
                    if line:
                        for r, c in line:
                            grid[r][c] = None
                        return True
    return False

# Подсчет очков
score = 0

# Проверка окончания игры
def check_game_over():
    for row in grid:
        if any(cell is None for cell in row):
            return False
    return True

# Отрисовка счета
def draw_score():
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Экран окончания игры
def game_over_screen():
    font = pygame.font.SysFont("Arial", 48)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

# Инициализация и первый запуск игры с добавлением шаров
add_new_balls(grid)

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)

    draw_grid()

    for row in grid:
        for ball in row:
            if ball:
                ball.draw(screen)

    draw_score()

    running = handle_events()

    if check_lines(grid):
        score += 10

    if check_game_over():
        game_over_screen()
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
