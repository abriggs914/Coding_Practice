from pygame_utility import *
from object_main import *

if __name__ == "__main__":

    e_pot = Entity("**POT**", 0)
    e_avery = Entity("Avery", 0)
    e_kristen = Entity("Kristen", 0)
    e_emily = Entity("Emily", 0)
    e_hayley = Entity("Hayley", 0)
    logbook_3 = LogBook()
    logbook_3.create_transaction(100, e_avery,
                                 e_pot)  # Payment("Mother's Day Supper (Wingo's)", "A", "P", 100, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(17.58, e_kristen,
                                 e_pot)  # Payment("Mother's Day Supper (Wingo's)", "K", "P", 17.58, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(115.74, e_emily,
                                 e_pot)  # Payment("Mother's Day Present ()", "E", "P", 115.74, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(55, e_hayley,
                                 e_emily)  # Payment("Hayley paid Emily", "H", "E", 55, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(170.7, e_kristen,
                                 e_pot)  # Payment("Father's Day Present (Air Fryer)", "K", "P", 170.7, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(40, e_avery,
                                 e_emily)  # Payment("Father's Day Boating", "A", "E", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(50, e_emily,
                                 e_pot)  # Payment("Father's Day Boating", "E", "P", 50, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(40, e_hayley,
                                 e_pot)  # Payment("Father's Day Boating", "H", "P", 40, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(10, e_emily,
                                 e_avery)  # Payment("Father's Day Boating", "E", "A", 10, datetime.datetime.strptime("2021-05-24", "%Y-%m-%d")),
    logbook_3.create_transaction(180, e_kristen,
                                 e_pot)  # Payment("Spotify", "K", "P", 180, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d")),
    logbook_3.create_transaction(89.99, e_avery,
                                 e_pot)  # Payment("Disney+", "A", "P", 89.99, datetime.datetime.strptime("2021-08-04", "%Y-%m-%d"))

    print(dict_print({
        "e_pot": e_pot,
        "e_avery": e_avery,
        "e_kristen": e_kristen,
        "e_emily": e_emily,
        "e_hayley": e_hayley
    }, "VALUES"))

    w, h = 750, 500
    app = PygameApplication("Who Pays Who?", w, h)
    game = app.get_game()
    display = app.display
    margin = 30
    top_offset = 55
    bottom_chart_offset = 35
    top_chart_offset = 35
    top_name_space = 10
    title_height = 20

    largest_money = max([e.balance for e in logbook_3.entities_list])
    chart_rect = game.Rect(margin, margin + top_offset, (w - (2 * margin)) / 2, h - (2 * margin) - top_offset)
    n_entities = len(logbook_3.entities_list) - 1
    entity_col_w = chart_rect.w / max(1, n_entities)
    entity_col_offset = (entity_col_w * 0.15) / 2
    entity_col_w *= 0.85

    print("largest_money:", largest_money)


    def draw_chart():
        game.draw.rect(display, WHITE, chart_rect)

        c = 0
        border_width = 1
        for i, ent in enumerate(logbook_3.entities_list):
            if ent.id_num != e_pot.id_num:
                col_rect = game.Rect(
                    chart_rect.x + (c * (entity_col_w + entity_col_offset)) + (entity_col_offset / (1 / 3)),
                    chart_rect.y + top_chart_offset, entity_col_w,
                    chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height))
                col_rect.x += entity_col_offset  # not quite

                # print("ent.balance / largest_money", ent.balance / largest_money)
                col_rect.h *= abs(ent.balance / largest_money)
                col_rect.y = (chart_rect.y + chart_rect.h) - (col_rect.h + bottom_chart_offset)

                game.draw.rect(display, random_color(), col_rect)
                t_curr_y = col_rect.y
                for j, t in enumerate(ent.transactions_list):
                    # t_height = abs(t.amount / ent.spending_balance) * col_rect.h
                    t_height = (t.amount / largest_money) * chart_rect.h
                    # print("e", ent, "t", t, "t_height:", t_height)
                    t_rect = game.Rect(col_rect.x, t_curr_y, col_rect.w, t_height)
                    t_curr_y += t_height
                    t_in_rect = t_rect
                    t_in_rect.x += border_width
                    t_in_rect.y += border_width
                    t_in_rect.w -= 2 * border_width
                    t_in_rect.h -= 2 * border_width

                    if t.entity_to == e_pot:
                        game.draw.rect(display, RED, t_rect)
                        game.draw.rect(display, BLUE, t_in_rect)
                    else:
                        game.draw.rect(display, GREEN, t_rect)
                        game.draw.rect(display, LIMEGREEN, t_in_rect)

                c += 1
                name_rect = game.Rect(col_rect.x, col_rect.y + col_rect.h + top_name_space, col_rect.w, title_height)
                write_text(game, display, name_rect, ent.name, game.font.SysFont("Arial", 12))


    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        draw_chart()

        event_queue = app.run()
        for event in event_queue:
            # handle events

            pass

        app.clock.tick(30)

    pay_pairs = logbook_3.who_pays_who()
    for pair in pay_pairs:
        amount, p_0, p_1 = pair
        entity_from = logbook_3.entity_look_up(p_0["ID"])
        entity_to = logbook_3.entity_look_up(p_1["ID"])
        print("pair:", pair)
        transaction = Transaction(amount, entity_from, entity_to)
        print("\tT:", transaction)
        logbook_3.add_transaction(transaction)

    print("Entities:", logbook_3.entities_list)
    for ent in logbook_3.entities_list:
        print(dict_print(ent.info_dict()))
