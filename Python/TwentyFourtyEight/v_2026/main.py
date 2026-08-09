# from colour_utility import *
# from utility import *
import pygame
import random

#	General main loop structure for pygame.
#	Includes 2D motion + gravity + acceleration controls.
#	Version............1.0
#	Date........2022-03-29
#	Author....Avery Briggs


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 750, 550
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60

    FONT_SCORE = pygame.font.Font(None, 28)
    FONT_GRID_SCORE = pygame.font.Font(None, 36)

    running = True
    debug = False
    mode = ""
    score = 0
    pts = {}
    
    n_rows = 10
    n_cols = n_rows
    
    f_moves_per_sec = 1
    f_other_corner_per_s = 1 / 12
    f_other_edge_per_s = 1 / (4 * 60)
    
    f_mspq = 1 / (f_moves_per_sec / 1000)
    f_mspy = 1 / (f_other_corner_per_s / 1000)
    f_mspz = 1 / (f_other_edge_per_s / 1000)
    
    print(f"{f_mspq=}, {f_mspy=}, {f_mspz=}")
    
    rect_score = pygame.Rect(WIDTH - 20 - 100, 10, 100, 20)
    colour_rect_score = "#989898"
    colour_font_score = "#000000"
    
    rect_time = pygame.Rect(rect_score.left - 20 - 100, 10, 100, 20)
    colour_rect_time = "#989898"
    colour_font_time = "#000000"
    
    rect_moves = pygame.Rect(rect_time.left - 20 - 100, 10, 100, 20)
    colour_rect_moves = "#989898"
    colour_font_moves = "#000000"

    mrg = 20
    rect_grid = pygame.Rect(mrg, rect_score.bottom + mrg, WIDTH - (2 * mrg), HEIGHT - (2 * mrg) - rect_score.bottom)
    colour_rect_grid = "#CCCCCC"
    colour_rect_grid_cell = "#5151A7"
    colour_font_grid_score = "#000000"
    
    colour_scheme = {
        None: colour_rect_grid_cell,
        2: "#7F51A7",
        4: "#A451A7",
        8: "#CC51A7",
        16: "#EE51A7",
        
        32: "#EE4271",
        64: "#EE2251",
        128: "#EE0230",
        256: "#FF0000",
        
        512: "#CCFFFF",
        1024: "#7FDDA7",
        2048: "#7FFFA7",
        4096: "#52FF88",
        8192: "#32FF60",
        16384: "#08FF20",
        32768: "#00FF00",
        65536: "#5FA0BF",
        131072: "#5FA0E4",
        262144: "#5F87FF",
        524288: "#4262FF",
        1048576: "#3F30FF",
        2097152: "#2323FF",
        4194304: "#0000FF",
        
        8388608: "#AAAAFF",
        16777216: "#FFFFFF",
    }
    
    mgl = 5
    wpc = (rect_grid.width - ((n_cols - 1) * mgl)) / n_cols
    wpr = (rect_grid.height - ((n_rows - 1) * mgl)) / n_rows
    print(f"{wpc=}, {wpr=}")
    
    grid_scores = []
    grid_rects = []
    for i in range(n_rows):
        r_grid_rects = []
        r_grid_scores = []
        for j in range(n_cols):
            r_grid_rects.append(
                pygame.Rect(
                    (j * (mgl + wpc)) + rect_grid.left,
                    (i * (mgl + wpr)) + rect_grid.top,
                    wpc,
                    wpr
                )
            )
            r_grid_scores.append(None)
        grid_rects.append(r_grid_rects)
        grid_scores.append(r_grid_scores)
        
    move_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    
    
    def compress_rl(gs):
        none_idxs = []
        new_grid = []
        for i in range(n_rows):
            new_row = []
            for j in range(n_cols):
                val = gs[i][j]
                if val is None:
                    none_idxs.append((i, j))
                else:
                    new_row.append(val)
            new_row = (([None] * n_cols) + new_row)[-n_cols:]
            
            j = n_cols - 1
            while j > 0:
                val = new_row[j]
                left = new_row[j - 1]
                if val and (val == left):
                    new_val = new_row[j] * 2
                    pts.update({new_val: pts.setdefault(new_val, 0) + 1})
                    new_row[j] = new_val
                    new_row[j - 1] = None
                j -= 1
            
            new_row = (([None] * n_cols) + [v for v in new_row if v])[-n_cols:]
            new_grid.append(new_row)
        return new_grid, gs != new_grid
    
    
    def transpose(grid):
        new_grid = []            
        for j in range(n_cols):
            new_row = []
            for i in range(n_rows):
                new_row.append(grid[i][j])
            new_grid.append(new_row)
        return new_grid                    
        
                    
        # print("A -> ", gs)
        # comb = []
        # for i in range(n_rows):
        #     skip_val = None
        #     for j in range(n_cols - 2, -1, -1):
        #         val = gs[i][j]
        #         if (val is not None) and (skip_val is None):
        #             val_left = gs[i][j + 1]
        #             if val == val_left:
        #                 comb.append((i, j))
        #                 skip_val = val
        #             elif val is None:
        #                 pass
        #             else:
        #                 skip_val = None
                        
        # print(f"{comb=}")
        
        # for i, j in comb:
        #     gs[i][j + 1] = gs[i][j + 1] * 2
        #     gs[i][j] = None
            
        # new_grid = []
        # for i in range(n_rows):
        #     skip_val = None
        #     keep_cells = [v for v in gs[i] if v]
        #     keep_idxs = [j for j in range(len(gs[i])) if gs[i][j]]
        #     if not comb:
        #         idx_none = -1 if (None not in gs[i]) else gs[i][::-1].index(None)
        #         comb = keep_cells and (idx_none < max(keep_idxs))
        #         print(f"{i=}, kc={keep_cells}, ki={keep_idxs}, {idx_none=}, {comb=}")
        #     row = (([None] * n_cols) + keep_cells)[-n_cols:]
        #     new_grid.append(row)
        
        # print("B -> ", new_grid)
        # return new_grid, comb
    

    n_moves = 0
    invalid_moves = 0
    total_time = CLOCK.get_time()
    while running:
        total_time += CLOCK.tick(FPS)
        s, ms = divmod(total_time, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        # if debug:
        if ms < 20:
            print(f"{total_time=}, {n_moves=}, {mode=}, {h=}, {m=}, {s=}, {ms=}")
            print(f"{f_mspq=}, a={n_moves * f_mspq}")
            if (s % 10) == 1:
                print(f"{pts=}")
        if pts and (mode == "idle"):
            mode = pygame.K_RIGHT if (n_moves % 2) == 0 else pygame.K_DOWN
            if (n_moves % 125) == 0 == 0:
                mode = pygame.K_LEFT
                print(f"L {mode=}")
            if (n_moves % 1600) == 0:
                mode = pygame.K_UP
                print(f"U {mode=}")
                # qd = divmod(total_time, max(1, int(n_moves * f_mspq)))
                # q = qd[0] >= 1
                # if q:
                #     d = mode in ["idle", pygame.K_DOWN]
                #     mode = pygame.K_RIGHT if d else pygame.K_DOWN
                #     print(f"{'R' if d else 'D'} {q=}, {qd=}")
                # if (ms % f_mspy) == 0 == 0:
                #     mode = pygame.K_LEFT
                #     print(f"L {mode=}")
                # if (ms % f_mspz) == 0:
                #     mode = pygame.K_UP
                #     print(f"U {mode=}")

        # reset window
        WINDOW.fill("#000000")

        # # begin drawing
        # text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
        # text_rect = text_surface.get_rect()
        # text_rect.center = WINDOW.get_rect().center
        # WINDOW.blit(text_surface, text_rect)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYUP:
                if event.key in move_keys + [pygame.K_PERIOD]:
                    mode = event.key
                    break
            # elif event.type == pygame.KEYDOWN:
            #     # Set the acceleration value.
            #     if event.key == pygame.K_LEFT:
            #         x_acceleration = -x_acceleration_rate
            #     if event.key == pygame.K_RIGHT:
            #         x_acceleration = x_acceleration_rate
            #     if event.key == pygame.K_UP:
            #         y_acceleration = -y_acceleration_rate
            #     if event.key == pygame.K_DOWN:
            #         y_acceleration = y_acceleration_rate
            # elif event.type == pygame.KEYUP:
            #     if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            #         x_acceleration = 0
            #     if event.key in (pygame.K_UP, pygame.K_DOWN):
            #         y_acceleration = 0

        # x_change += x_acceleration  # Accelerate.
        # y_change += y_acceleration  # Accelerate.
        # if abs(x_change) >= max_speed:  # If max_speed is exceeded.
        #     # Normalize the x_change and multiply it with the max_speed.
        #     x_change = x_change / abs(x_change) * max_speed
        # if abs(y_change) >= max_speed:  # If max_speed is exceeded.
        #     # Normalize the x_change and multiply it with the max_speed.
        #     y_change = y_change / abs(y_change) * max_speed

        # # Decelerate if no key is pressed.
        # if x_acceleration == 0:
        #     x_change *= x_de_acceleration_rate
        # if y_acceleration == 0:
        #     y_change *= y_de_acceleration_rate

        # # Add effect of gravity
        # x_change += x_gravity
        # y_change += y_gravity

        # # Move the object
        # win_rect = WINDOW.get_rect()
        # x = clamp(win_rect.left + (m_width / 2), x + x_change, win_rect.right - (m_width / 2))  # Move the object.
        # y = clamp(win_rect.top + (m_height / 2), y + y_change, win_rect.bottom - (m_height / 2))  # Move the object.

        # rect.center = x, y
        # pygame.draw.rect(WINDOW, (0, 120, 250), rect)
        
        cpr = 1
        if mode == "idle":
            pass
        elif mode == pygame.K_PERIOD:
            mode = "step"
        elif mode in move_keys:
            comb = []
            if mode == pygame.K_RIGHT:
                new_grid, comb = compress_rl(grid_scores)
                grid_scores = new_grid
                n_moves += 1
                if debug:
                    print("-> RIGHT")
            elif mode == pygame.K_LEFT:
                # print("LEFT")
                # print(grid_scores)
                gs = [row[::-1] for row in grid_scores]
                # print("gs 1")
                # print(gs)
                new_grid, comb = compress_rl(gs)
                new_grid = [row[::-1] for row in new_grid]
                grid_scores = new_grid
                n_moves += 1
                if debug:
                    print("-> LEFT")
            elif mode == pygame.K_UP:
                # print("UP 0", grid_scores)
                gs = transpose(grid_scores)
                # print("UP 1", gs)
                new_grid, comb = compress_rl(gs)
                # print("UP 2", new_grid)
                # new_grid = [row[::-1] for row in new_grid]
                
                gs = []
                for i in range(n_rows):
                    row = new_grid[i]
                    gs.append(([v for v in new_grid[i] if v] + ([None] * n_cols))[:n_cols])
                new_grid = gs
                
                # print("UP 3", new_grid)
                new_grid = transpose(new_grid)
                # print("UP 4", new_grid)
                comb = grid_scores != new_grid
                grid_scores = new_grid
                n_moves += 1
                if debug:
                    print("-> UP")
            elif mode == pygame.K_DOWN:
                # print("DOWN 0", grid_scores)
                gs = transpose(grid_scores)
                # print("DOWN 1", gs)
                new_grid, comb = compress_rl(gs)
                # print("DOWN 2", new_grid)
                # new_grid = [row[::-1] for row in new_grid]
                
                # gs = []
                # for i in range(n_rows):
                #     row = new_grid[i]
                #     gs.append(([v for v in new_grid[i] if v] + ([None] * n_cols))[:n_cols])
                # new_grid = gs
                
                # print("DOWN 3", new_grid)
                new_grid = transpose(new_grid)
                # print("DOWN 3", new_grid)
                comb = grid_scores != new_grid
                grid_scores = new_grid
                n_moves += 1
                if debug:
                    print("-> DOWN")
                            
            if comb:
                mode = None                        
            else:
                mode = "idle"
                invalid_moves += 1
                
        else:
            available = [(i, j) for j in range(n_cols) for i in range(n_rows) if grid_scores[i][j] is None]
            if len(available) >= cpr:
                choices = []
                for i in range(cpr):
                    choices.append(random.choice(available))
                    available.remove(choices[-1])
                for i, idx in enumerate(choices):
                    new_val = random.choice([2, 4])
                    grid_scores[idx[0]][idx[1]] = new_val
                    pts.update({new_val: pts.setdefault(new_val, 0) + 1})
                    # score += new_val
                mode = "idle"
            else:
                raise ValueError("GameOver")
        
        # draw score
        pygame.draw.rect(WINDOW, colour_rect_score, rect_score)
        score = sum([k * v for k, v in pts.items()])
        text_surface = FONT_SCORE.render(f"{score}", True, colour_font_score, "#FF2323")
        text_rect = text_surface.get_rect()
        text_rect.center = rect_score.center
        WINDOW.blit(text_surface, text_rect)
    
        # draw time
        pygame.draw.rect(WINDOW, colour_rect_time, rect_time)
        time = (f"{h}h " if h else "") + (f"{m}m " if m else "") + (f"{s}s " if s else "")
        text_surface = FONT_SCORE.render(time, True, colour_font_time, "#FF2323")
        text_rect = text_surface.get_rect()
        text_rect.center = rect_time.center
        WINDOW.blit(text_surface, text_rect)
    
        # draw moves
        pygame.draw.rect(WINDOW, colour_rect_moves, rect_moves)
        moves = f"# moves: {n_moves - invalid_moves}"
        text_surface = FONT_SCORE.render(moves, True, colour_font_moves, "#FF2323")
        text_rect = text_surface.get_rect()
        text_rect.center = rect_moves.center
        WINDOW.blit(text_surface, text_rect)
        
        # draw grid
        pygame.draw.rect(WINDOW, colour_rect_grid, rect_grid)
        
        for i in range(n_rows):
            for j in range(n_cols):
                cell_rect = grid_rects[i][j]
                cell_score = grid_scores[i][j]
                pygame.draw.rect(WINDOW, colour_scheme[cell_score], cell_rect)
                if cell_score:
                    text_surface = FONT_GRID_SCORE.render(f"{cell_score}", True, colour_font_grid_score, "#54B613")
                    text_rect = text_surface.get_rect()
                    text_rect.center = cell_rect.center
                    WINDOW.blit(text_surface, text_rect)

        # update the display
        # draw everything
        # pygame.display.flip()
        # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()

    pygame.quit()
