import os
import datetime
import pandas as pd
from dateutil.utils import today

from colour_utility import Colour
from nhl_utility import NHLAPIHandler, NHLSchedule, NHLGameDate, NHLBoxScore, NHLStandings
import pygame_utility as pgu
import pygame
# from json_utility import jsonify
import json


DB_FILE: str = "testing_save_file_2026_02_02.json"
key_selected_team: str = "k_selected_team"
key_save_date: str = "k_save_date"


def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)


def set_selected_team():

    df_team_name_ids = df_teams[["id", "fullName"]]
    teams_text = ""
    for i, row in df_team_name_ids.iterrows():
        teams_text += f"{str(row['id']).rjust(4)} - {row['fullName'].rjust(25)}\n"
    team = input(f"Enter the id of your favourite team:\n{teams_text}\n\t")
    try:
        team = int(team)
    except ValueError:
        team = 0
    return team


def save_session():
    db[key_save_date] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DB_FILE, "w") as f:
        json.dump(db, f)


if __name__ == "__main__":

    from customtkinter_utility import get_largest_monitors

    pygame.init()

    m0 = get_largest_monitors()[0]

    WIDTH, HEIGHT = m0.width * 0.9, m0.height * 0.9
    P_WIDTH, P_HEIGHT = 0.8, 0.8
    MARGIN_X_GRID = WIDTH - (WIDTH * P_WIDTH)
    MARGIN_Y_GRID = HEIGHT - (HEIGHT * P_HEIGHT)
    G_WIDTH, G_HEIGHT = WIDTH * P_WIDTH, HEIGHT * P_HEIGHT
    X_GRID, Y_GRID = 5, 5
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS_START = 5
    FPS = 60

    FONT_DEFAULT = pygame.font.Font(None, 36)

    score = 0
    running = True
    time_passed = 0
    ticks_passed = 0

    x, y = WIDTH / 2, HEIGHT / 2
    max_speed = 15
    x_change = 0
    y_change = 0
    x_accel_r = 0.2
    y_accel_r = 0.2
    x_decel_r = 0.92
    y_decel_r = 0.92
    x_accel = 0
    y_accel = 0
    m_width, m_height = 20, 40
    mallow_rect = pygame.Rect(0, 0, m_width, m_height)
    mallow_rect.center = x, y

    black = Colour("black")
    colour_mallow = Colour((0, 120, 250))
    bg_grid_cell = Colour((160, 160, 160))
    colour_snake = Colour((10, 210, 40))
    colour_food = Colour((210, 40, 10))

    api = NHLAPIHandler(init=True)
    db: dict = load_db()

    df_teams: pd.DataFrame = api.get_team_data()

    if key_selected_team not in db:
        db[key_selected_team] = set_selected_team()

    today: datetime.date = datetime.datetime.now().date()
    if datetime.datetime.now().hour < 3:
        today -= datetime.timedelta(days=1)
    sel_team_id = db.get(key_selected_team, 0)
    ser_sel_team: pd.Series = df_teams.loc[df_teams["id"] == sel_team_id].reset_index().iloc[0]

    print(f"Selected Team: {ser_sel_team['fullName']}")

    print("="*120)
    print("Teams")
    print(df_teams)

    standings: NHLStandings = api.get_standings(date_in=today)
    schedule: NHLSchedule = api.get_schedule(date_in=today)
    schedule_game_week: list[NHLGameDate] = schedule.game_week
    print("="*120)
    print("standings")
    print(standings.df_standings)
    print("="*120)
    print("schedule")
    print(schedule)
    print("="*120)

    for i, game_date in enumerate(schedule_game_week):
        if game_date.date == today:
            print(f"Game {i}: {game_date.date}")
            games: list[NHLBoxScore] = game_date.games
            team_plays_today = False
            for j, game in enumerate(games):
                # print(game)
                if sel_team_id in (game.away_team_id, game.home_team_id):
                    print(f"Selected Team Game: {game}")
                    team_plays_today = True
                    g_id = game.g_id
                    print(game.to_df_row())
                    landing = api.load_game_landing(g_id)
                    print("landing")
                    print(landing)
                    box_score = api.load_game_boxscore(g_id)
                    print("box_score")
                    print(box_score)
            if not team_plays_today:
                print(f"sel team does not play today {game_date.date}")

    print(api.check_game_status(sel_team_id, today))
    print("="*120)

    # def draw_table():
    #     table = pgu.Table(pygame, WINDOW, 20, 20, 800, 900, colour_mallow, FONT_DEFAULT, "Box Score Data", "Header")
    #     table.add_rows([[k, v] for k, v in box_score.__dict__.items()])
    #     table.draw()

    def draw_dates_nav_bar():
        bb = pgu.ButtonBar(
            pygame,
            WINDOW,
            rect_dates_nav_bar,
            FONT_DEFAULT,
            "#CCCCFF"
        )

        df_box_scores: pd.DataFrame = api.df_games_boxscore
        df_box_scores = df_box_scores[
            (df_box_scores["start_time_atl"].dt.date >= start)
            & (df_box_scores["start_time_atl"].dt.date <= end)
        ]
        df_box_scores.sort_values("start_time_atl", inplace=True)
        # dates = df_box_scores["start_time_atl"].unique().tolist()

        for i, date in enumerate(dates):
            bb.add_button(
                f"{date:%Y-%m-%d}",
                "#9898AA",
                "#BBBBCA",
                lambda date_=date: update
            )
        bb.draw()


    rect_dates_nav_bar = pygame.Rect(15, 15, WIDTH, 20)
    k_bxs_sel_id_date = None
    k_bxs_start_date: datetime.date = today + datetime.timedelta(days=-3)
    end: datetime.date = today + datetime.timedelta(days=3)
    dates = pd.date_range(start, end)

    while running:
        CLOCK.tick(FPS_START)
        time_passed += CLOCK.get_time()
        ticks_passed += 1

        # reset window
        WINDOW.fill(black.rgb_code)

        # # begin drawing
        # text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
        # text_rect = text_surface.get_rect()
        # text_rect.center = WINDOW.get_rect().center
        # WINDOW.blit(text_surface, text_rect)

        draw_dates_nav_bar()

        print(f"{ticks_passed=}, {time_passed} milliseconds")

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                # Set the acceleration value.
                if event.key == pygame.K_LEFT:
                    x_accel = -x_accel_r
                    snake_direction = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    x_accel = x_accel_r
                    snake_direction = (1, 0)
                if event.key == pygame.K_UP:
                    y_accel = -y_accel_r
                    snake_direction = (0, -1)
                if event.key == pygame.K_DOWN:
                    y_accel = y_accel_r
                    snake_direction = (0, 1)
            # elif event.type == pygame.KEYUP:
            #     if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            #         x_accel = 0
            #     if event.key in (pygame.K_UP, pygame.K_DOWN):
            #         y_accel = 0

        # if ticks_passed % 2 == 0:
        #     # do something every other game tick

        # # update the display
        # # draw everything
        # # pygame.display.flip()
        # # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()

    pygame.quit()

    save_session()