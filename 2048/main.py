import pygame
import sys
import random

SIZE = WIDTH, HEIGHT = 400, 400
TILE_MARGIN = 10
TILE_SIZE = (WIDTH - TILE_MARGIN * 5) // 4

GRID_WIDTH = 4 * TILE_SIZE + 5 * TILE_MARGIN
GRID_HEIGHT = 4 * TILE_SIZE + 5 * TILE_MARGIN
GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT) // 2

FONT_COLOR = (119, 110, 101)
BG_COLOR = (250, 248, 239)
GRID_BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (237, 229, 218),
    4: (238, 225, 201),
    8: (243, 178, 122),
    16: (246, 150, 101),
    32: (247, 124, 95),
    64: (247, 95, 59),
    128: (247, 208, 115),
    256: (237, 204, 99),
    512: (236, 204, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32, bold=True)

board = [[0] * 4 for _ in range(4)]

def drawing(board):
    screen.fill(BG_COLOR)

    grid_rect = pygame.Rect(GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT)
    pygame.draw.rect(screen, GRID_BG_COLOR, grid_rect, border_radius=12)

    for r in range(4):
        for c in range(4):
            value = board[r][c]
            x = GRID_X + c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
            y = GRID_Y + r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect, border_radius=8)
            if value != 0:
                text = font.render(str(value), True, FONT_COLOR if value <= 4 else (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def random_tile(board):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if not empty_cells:
        return None
    r, c = random.choice(empty_cells)
    board[r][c] = 4 if random.random() < 0.1 else 2
    return(r, c)

def compress_and_merge(row):
    new_row = [i for i in row if i != 0]
    merge_positions = []
    
    for i in range(len(new_row)-1):
        if new_row[i] == new_row[i+1]:
            new_row[i] *= 2
            new_row[i+1] = 0
            merge_positions.append(i)
    
    new_row = [i for i in new_row if i != 0]
    return new_row + [0] * (4 - len(new_row)), merge_positions


def merge_animation(board, merge_positions):
    for frame in range(10):
        screen.fill(BG_COLOR)

        grid_rect = pygame.Rect(GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT)
        pygame.draw.rect(screen, GRID_BG_COLOR, grid_rect, border_radius=12)

        for r in range(4):
            for c in range(4):
                value = board[r][c]
                x = GRID_X + c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                y = GRID_Y + r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                
                if (r, c) in merge_positions:
                    scale = 1.0 + 0.2 * (1 - abs(frame - 5) / 5) 
                    size = int(TILE_SIZE * scale)
                    offset = (TILE_SIZE - size) // 2
                    rect = pygame.Rect(x + offset, y + offset, size, size)
                else:
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect, border_radius=8)
                if value != 0:
                    text = font.render(str(value), True, FONT_COLOR if value <= 4 else (255, 255, 255))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)


def spawn_animation(board, pos):
    r, c = pos
    value = board[r][c]

    for frame in range(10):
        screen.fill(BG_COLOR)

        grid_rect = pygame.Rect(GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT)
        pygame.draw.rect(screen, GRID_BG_COLOR, grid_rect, border_radius=12)

        for row in range(4):
            for col in range(4):
                tile_value = board[row][col]
                x = GRID_X + col * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                y = GRID_Y + row * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                if (row, col) == (r, c):
                    continue 

                color = TILE_COLORS.get(tile_value, (60, 58, 50))
                pygame.draw.rect(screen, color, rect, border_radius=8)
                if tile_value != 0:
                    text = font.render(str(tile_value), True, FONT_COLOR if tile_value <= 4 else (255, 255, 255))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        # New tile scale animation
        scale = frame / 9 
        size = int(TILE_SIZE * scale)
        offset = (TILE_SIZE - size) // 2
        x = GRID_X + c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN + offset
        y = GRID_Y + r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN + offset
        rect = pygame.Rect(x, y, size, size)

        pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect, border_radius=8)
        if value != 0 and scale > 0.3: 
            text = font.render(str(value), True, FONT_COLOR if value <= 4 else (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


        pygame.display.flip()
        clock.tick(60)


def slide_animation(prev_board, movements):
    for frame in range(10):
        screen.fill(BG_COLOR)

        grid_rect = pygame.Rect(GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT)
        pygame.draw.rect(screen, GRID_BG_COLOR, grid_rect, border_radius=12)

        animated_sources = set()
        for dest in movements:
            for src in movements[dest]:
                animated_sources.add(src)

        # Stationary tiles drawing
        for r in range(4):
            for c in range(4):    
                x = GRID_X + c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                y = GRID_Y + r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    
                value = prev_board[r][c]
                if (r, c) in animated_sources:
                    pygame.draw.rect(screen, TILE_COLORS.get(0), rect, border_radius=8)
                else:
                    pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect, border_radius=8)
                    if value != 0:
                        text = font.render(str(value), True, FONT_COLOR if value <= 4 else (255, 255, 255))
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)

        # Movements animations
        for (end_r, end_c), sources in movements.items():
            if not isinstance(sources, list):
                sources = [sources]
            for start_r, start_c in sources:
                value = prev_board[start_r][start_c]

                start_x = GRID_X + start_c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                start_y = GRID_Y + start_r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN

                end_x = GRID_X + end_c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                end_y = GRID_Y + end_r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN

                x = start_x + (end_x - start_x) * frame / 9
                y = start_y + (end_y - start_y) * frame / 9

                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect, border_radius=8)
                if value != 0:
                    text = font.render(str(value), True, FONT_COLOR if value <= 4 else (255, 255, 255))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

def move_left(board):
    movements = {}
    merge_positions = set()
    moved = False
    prev_board = [row[:] for row in board]

    for r in range(4):
        original_row = board[r][:]
        new_row, merges = compress_and_merge(original_row)
        if new_row != original_row:
            moved = True
            used = [False] * 4
            temp_row = [i for i in original_row if i != 0]

            i = j = 0
            while i < len(temp_row):
                if i + 1 < len(temp_row) and temp_row[i] == temp_row[i + 1]:
                    sources = []
                    for k in range(4):
                        if not used[k] and original_row[k] == temp_row[i]:
                            sources.append((r, k))
                            used[k] = True
                            break
                    for k in range(4):
                        if not used[k] and original_row[k] == temp_row[i + 1]:
                            sources.append((r, k))
                            used[k] = True
                            break
                    movements[(r, j)] = sources
                    merge_positions.add((r, j))
                    i += 2
                else:
                    for k in range(4):
                        if not used[k] and original_row[k] == temp_row[i]:
                            movements[(r, j)] = [(r, k)]
                            used[k] = True
                            break
                    i += 1
                j += 1
            board[r] = new_row

    if moved:
        slide_animation(prev_board, movements)
        if merge_positions:
            merge_animation(board, merge_positions)
    return moved

def move_right(board):
    movements = {}
    merge_positions = set()
    moved = False
    prev_board = [row[:] for row in board]

    for r in range(4):
        original_row = board[r][:]
        reversed_row = original_row[::-1]
        new_row, merges = compress_and_merge(reversed_row)
        new_row = new_row[::-1]
        if new_row != original_row:
            moved = True
            used = [False] * 4
            temp_row = [i for i in reversed_row if i != 0]

            i = j = 0
            while i < len(temp_row):
                col = 3 - j
                if i + 1 < len(temp_row) and temp_row[i] == temp_row[i + 1]:
                    sources = []
                    for k in range(3, -1, -1):
                        if not used[k] and original_row[k] == temp_row[i]:
                            sources.append((r, k))
                            used[k] = True
                            break
                    for k in range(3, -1, -1):
                        if not used[k] and original_row[k] == temp_row[i + 1]:
                            sources.append((r, k))
                            used[k] = True
                            break
                    movements[(r, col)] = sources
                    merge_positions.add((r, col))
                    i += 2
                else:
                    for k in range(3, -1, -1):
                        if not used[k] and original_row[k] == temp_row[i]:
                            movements[(r, col)] = [(r, k)]
                            used[k] = True
                            break
                    i += 1
                j += 1
            board[r] = new_row

    if moved:
        slide_animation(prev_board, movements)
        if merge_positions:
            merge_animation(board, merge_positions)
    return moved

def move_up(board):
    movements = {}
    merge_positions = set()
    moved = False
    prev_board = [row[:] for row in board]

    for c in range(4):
        original_col = [board[r][c] for r in range(4)]
        new_col, merges = compress_and_merge(original_col)
        if new_col != original_col:
            moved = True
            used = [False] * 4
            temp_col = [i for i in original_col if i != 0]

            i = j = 0
            while i < len(temp_col):
                row = j
                if i + 1 < len(temp_col) and temp_col[i] == temp_col[i + 1]:
                    sources = []
                    for k in range(4):
                        if not used[k] and original_col[k] == temp_col[i]:
                            sources.append((k, c))
                            used[k] = True
                            break
                    for k in range(4):
                        if not used[k] and original_col[k] == temp_col[i + 1]:
                            sources.append((k, c))
                            used[k] = True
                            break
                    movements[(row, c)] = sources
                    merge_positions.add((row, c))
                    i += 2
                else:
                    for k in range(4):
                        if not used[k] and original_col[k] == temp_col[i]:
                            movements[(row, c)] = [(k, c)]
                            used[k] = True
                            break
                    i += 1
                j += 1
            for r in range(4):
                board[r][c] = new_col[r]

    if moved:
        slide_animation(prev_board, movements)
        if merge_positions:
            merge_animation(board, merge_positions)
    return moved

def move_down(board):
    movements = {}
    merge_positions = set()
    moved = False
    prev_board = [row[:] for row in board]

    for c in range(4):
        original_col = [board[r][c] for r in range(4)]
        reversed_col = original_col[::-1]
        new_col, merges = compress_and_merge(reversed_col)
        new_col = new_col[::-1]
        if new_col != original_col:
            moved = True
            used = [False] * 4
            temp_col = [i for i in reversed_col if i != 0]

            i = j = 0
            while i < len(temp_col):
                row = 3 - j
                if i + 1 < len(temp_col) and temp_col[i] == temp_col[i + 1]:
                    sources = []
                    for k in range(3, -1, -1):
                        if not used[k] and original_col[k] == temp_col[i]:
                            sources.append((k, c))
                            used[k] = True
                            break
                    for k in range(3, -1, -1):
                        if not used[k] and original_col[k] == temp_col[i + 1]:
                            sources.append((k, c))
                            used[k] = True
                            break
                    movements[(row, c)] = sources
                    merge_positions.add((row, c))
                    i += 2
                else:
                    for k in range(3, -1, -1):
                        if not used[k] and original_col[k] == temp_col[i]:
                            movements[(row, c)] = [(k, c)]
                            used[k] = True
                            break
                    i += 1
                j += 1
            for r in range(4):
                board[r][c] = new_col[r]

    if moved:
        slide_animation(prev_board, movements)
        if merge_positions:
            merge_animation(board, merge_positions)
    return moved 

def is_game_over(board):
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                return False
            if c < 3 and board[r][c] == board[r][c+1]:
                return False
            if r < 3 and board[r][c] == board[r+1][c]:
                return False
    return True

def show_game_over():
    overlay = pygame.Surface(SIZE)
    overlay.set_alpha(180)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))
    text = font.render("Game Over!", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)


random_tile(board)
random_tile(board)

# Game loop
game_over = False
running = True
while running:
    screen.fill(BG_COLOR)
    drawing(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            moved = False
            if event.key == pygame.K_LEFT:
                moved = move_left(board)
            elif event.key == pygame.K_RIGHT:
                moved = move_right(board)
            elif event.key == pygame.K_UP:
                moved = move_up(board)
            elif event.key == pygame.K_DOWN:
                moved = move_down(board)

            if moved:
                new_tile_pos = random_tile(board)
                if new_tile_pos:
                    spawn_animation(board, new_tile_pos)
                if is_game_over(board):
                    game_over = True

    if game_over:
        show_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

