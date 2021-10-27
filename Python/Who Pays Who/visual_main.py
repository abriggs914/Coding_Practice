from pygame_utility import *
from object_main import *

if __name__ == "__main__":

    # GSM for chart
    CHART_VIEW_MODE = None
    SUM_OF_MONEY_HANDLED = "SUM_OF_MONEY_HANDLED"
    SUM_OF_MONEY_SPENT = "SUM_OF_MONEY_SPENT"
    SUM_OF_MONEY_EARNED = "SUM_OF_MONEY_EARNED"
    SUM_OF_MONEY_EARNED_V_SPENT = "SUM_OF_MONEY_EARNED_V_SPENT"
    BALANCE = "BALANCE"
    ALL = "ALL"

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

    chart_rect = game.Rect(margin, margin + top_offset, (w - (2 * margin)) / 2, h - (2 * margin) - top_offset)
    n_entities = len(logbook_3.entities_list) - 1
    entity_col_w = chart_rect.w / max(1, n_entities)
    entity_col_offset = (entity_col_w * 0.15) / 2
    entity_col_w *= 0.85

    def change_chart(new_mode):
        global CHART_VIEW_MODE
        CHART_VIEW_MODE = new_mode

    def draw_chart():
        game.draw.rect(display, WHITE, chart_rect)

        c = 0
        border_width = 1
        col_rects = []
        smallest_money = 0
        largest_money = 0

        # draw these after the money gridlines are drawn
        drawables = []
        include_negatives = False  # True when the chart does not start at $0

        if CHART_VIEW_MODE == SUM_OF_MONEY_HANDLED:
            largest_money = max([abs(e.balance) for e in logbook_3.entities_list if e != e_pot])
            largest_money = max(largest_money, logbook_3.even_pot_split())
            for i, ent in enumerate(logbook_3.entities_list):
                if ent.id_num != e_pot.id_num:
                    col_rect_spent = game.Rect(
                        chart_rect.x + (c * (entity_col_w + entity_col_offset)) + (entity_col_offset / (1 / 3)),
                        chart_rect.y + top_chart_offset, entity_col_w,
                        chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height))
                    col_rect_spent.x += entity_col_offset  # not quite
                    col_rects.append((i, col_rect_spent))

                    # print("ent.balance / largest_money", ent.balance / largest_money)
                    money_handled = abs(ent.spending_balance) + abs(ent.earning_balance)
                    col_rect_spent.h *= abs(money_handled / largest_money)
                    col_rect_spent.y = (chart_rect.y + chart_rect.h) - (col_rect_spent.h + bottom_chart_offset)

                    # game.draw.rect(display, random_color(), col_rect_spent)
                    drawables.append((game.draw.rect, (display, BLACK, col_rect_spent)))
                    t_curr_y_spent = col_rect_spent.y
                    for j, t in enumerate(ent.transactions_list):
                        t_height_spent = abs(t.amount / money_handled) * col_rect_spent.h
                        # t_height_spent = (t.amount / largest_money) * chart_rect.h
                        # print("e", ent, "t", t, "t_height_spent:", t_height_spent)
                        t_rect_spent = game.Rect(col_rect_spent.x, t_curr_y_spent, col_rect_spent.w, t_height_spent)
                        t_curr_y_spent += t_height_spent
                        t_in_rect_spent = t_rect_spent
                        t_in_rect_spent.x += border_width
                        t_in_rect_spent.y += border_width
                        t_in_rect_spent.w -= 2 * border_width
                        t_in_rect_spent.h -= 2 * border_width

                        if t.entity_from == ent:
                            drawables.append((game.draw.rect, (display, RED, t_rect_spent)))
                            drawables.append((game.draw.rect, (display, BLUE, t_in_rect_spent)))
                        else:
                            drawables.append((game.draw.rect, (display, GREEN, t_rect_spent)))
                            drawables.append((game.draw.rect, (display, LIMEGREEN, t_in_rect_spent)))

                    drawables.append((write_text, (game, display, game.Rect(col_rect_spent.x, col_rect_spent.y - 20, col_rect_spent.w, 20), money(abs(ent.spending_balance) + abs(ent.earning_balance)), game.font.SysFont("Arial", 12))))

                    c += 1
                    name_rect_spent = game.Rect(col_rect_spent.x, col_rect_spent.y + col_rect_spent.h + top_name_space, col_rect_spent.w, title_height)
                    drawables.append((write_text, (game, display, name_rect_spent, ent.name, game.font.SysFont("Arial", 12))))
        elif CHART_VIEW_MODE == SUM_OF_MONEY_SPENT:
            largest_money = max([abs(e.spending_balance) for e in logbook_3.entities_list if e != e_pot])
            largest_money = max(largest_money, logbook_3.even_pot_split())
            for i, ent in enumerate(logbook_3.entities_list):
                if ent.id_num != e_pot.id_num:
                    col_rect_spent = game.Rect(
                        chart_rect.x + (c * (entity_col_w + entity_col_offset)) + (entity_col_offset / (1 / 3)),
                        chart_rect.y + top_chart_offset, entity_col_w,
                        chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height))
                    col_rect_spent.x += entity_col_offset  # not quite
                    col_rects.append((i, col_rect_spent))

                    # print("ent.balance / largest_money", ent.balance / largest_money)
                    money_handled = abs(ent.spending_balance)
                    col_rect_spent.h *= abs(money_handled / largest_money)
                    col_rect_spent.y = (chart_rect.y + chart_rect.h) - (col_rect_spent.h + bottom_chart_offset)

                    # game.draw.rect(display, random_color(), col_rect_spent)
                    drawables.append((game.draw.rect, (display, BLACK, col_rect_spent)))
                    t_curr_y_spent = col_rect_spent.y
                    for j, t in enumerate(ent.transactions_list):
                        t_height_spent = abs(t.amount / money_handled) * col_rect_spent.h
                        # t_height_spent = (t.amount / largest_money) * chart_rect.h
                        # print("e", ent, "t", t, "t_height_spent:", t_height_spent)
                        t_rect_spent = game.Rect(col_rect_spent.x, t_curr_y_spent, col_rect_spent.w, t_height_spent)
                        t_in_rect_spent = t_rect_spent
                        t_in_rect_spent.x += border_width
                        t_in_rect_spent.y += border_width
                        t_in_rect_spent.w -= 2 * border_width
                        t_in_rect_spent.h -= 2 * border_width

                        if t.entity_from == ent:
                            t_curr_y_spent += t_height_spent
                            drawables.append((game.draw.rect, (display, RED, t_rect_spent)))
                            drawables.append((game.draw.rect, (display, BLUE, t_in_rect_spent)))
                        # else:
                        #     drawables.append((game.draw.rect, (display, GREEN, t_rect)))
                        #     drawables.append((game.draw.rect, (display, LIMEGREEN, t_in_rect_spent)))

                    drawables.append((write_text, (game, display, game.Rect(col_rect_spent.x, col_rect_spent.y - 20, col_rect_spent.w, 20), money(abs(ent.spending_balance)), game.font.SysFont("Arial", 12))))

                    c += 1
                    name_rect_spent = game.Rect(col_rect_spent.x, col_rect_spent.y + col_rect_spent.h + top_name_space, col_rect_spent.w, title_height)
                    drawables.append((write_text, (game, display, name_rect_spent, ent.name, game.font.SysFont("Arial", 12))))
        elif CHART_VIEW_MODE == SUM_OF_MONEY_EARNED:
            largest_money = max([abs(e.earning_balance) for e in logbook_3.entities_list if e != e_pot])
            largest_money = max(largest_money, logbook_3.even_pot_split())
            for i, ent in enumerate(logbook_3.entities_list):
                if ent.id_num != e_pot.id_num:
                    col_rect_spent = game.Rect(
                        chart_rect.x + (c * (entity_col_w + entity_col_offset)) + (entity_col_offset / (1 / 3)),
                        chart_rect.y + top_chart_offset, entity_col_w,
                        chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height))
                    col_rect_spent.x += entity_col_offset  # not quite
                    col_rects.append((i, col_rect_spent))

                    # print("ent.balance / largest_money", ent.balance / largest_money)
                    money_handled = abs(ent.earning_balance)
                    col_rect_spent.h *= abs(money_handled / largest_money)
                    col_rect_spent.y = (chart_rect.y + chart_rect.h) - (col_rect_spent.h + bottom_chart_offset)

                    # game.draw.rect(display, random_color(), col_rect_spent)
                    drawables.append((game.draw.rect, (display, BLACK, col_rect_spent)))
                    t_curr_y_spent = col_rect_spent.y
                    for j, t in enumerate(ent.transactions_list):
                        t_height_spent = abs(t.amount / max(1, money_handled)) * col_rect_spent.h
                        # t_height_spent = (t.amount / largest_money) * chart_rect.h
                        # print("e", ent, "t", t, "t_height_spent:", t_height_spent)
                        t_rect_spent = game.Rect(col_rect_spent.x, t_curr_y_spent, col_rect_spent.w, t_height_spent)
                        t_in_rect_spent = t_rect_spent
                        t_in_rect_spent.x += border_width
                        t_in_rect_spent.y += border_width
                        t_in_rect_spent.w -= 2 * border_width
                        t_in_rect_spent.h -= 2 * border_width

                        if t.entity_to == ent:
                            t_curr_y_spent += t_height_spent
                            drawables.append((game.draw.rect, (display, RED, t_rect_spent)))
                            drawables.append((game.draw.rect, (display, BLUE, t_in_rect_spent)))
                        # else:
                        #     drawables.append((game.draw.rect, (display, GREEN, t_rect)))
                        #     drawables.append((game.draw.rect, (display, LIMEGREEN, t_in_rect_spent)))

                    drawables.append((write_text, (game, display, game.Rect(col_rect_spent.x, col_rect_spent.y - 20, col_rect_spent.w, 20), money(abs(ent.earning_balance)), game.font.SysFont("Arial", 12))))

                    c += 1
                    name_rect_spent = game.Rect(col_rect_spent.x, col_rect_spent.y + col_rect_spent.h + top_name_space, col_rect_spent.w, title_height)
                    drawables.append((write_text, (game, display, name_rect_spent, ent.name, game.font.SysFont("Arial", 12))))
        elif CHART_VIEW_MODE == BALANCE:
            include_negatives = True
            largest_money = max([e.balance for e in logbook_3.entities_list if e != e_pot])
            lg1 = largest_money
            smallest_money = min([e.balance for e in logbook_3.entities_list if e != e_pot])
            largest_money = max(abs(largest_money) + abs(smallest_money), logbook_3.even_pot_split())
            print("largest: {}, smallest: {}, largest2: {}".format(lg1, smallest_money, largest_money))
            for i, ent in enumerate(logbook_3.entities_list):
                if ent.id_num != e_pot.id_num:
                    col_rect_spent = game.Rect(
                        chart_rect.x + (c * (entity_col_w + entity_col_offset)) + (entity_col_offset / (1 / 3)),
                        chart_rect.y + top_chart_offset, entity_col_w,
                        chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height))
                    col_rect_spent.x += entity_col_offset  # not quite
                    col_rects.append((i, col_rect_spent))

                    # print("ent.balance / largest_money", ent.balance / largest_money)
                    money_handled = ent.balance
                    col_rect_spent.h *= abs(money_handled / largest_money)
                    col_rect_spent.y = (chart_rect.y + chart_rect.h) - (col_rect_spent.h + bottom_chart_offset)

                    # game.draw.rect(display, random_color(), col_rect_spent)
                    drawables.append((game.draw.rect, (display, VIOLETRED, col_rect_spent)))
                    t_curr_y_spent = col_rect_spent.y
                    # for j, t in enumerate(ent.transactions_list):
                    #     t_height_spent = abs(t.amount / max(1, money_handled)) * col_rect_spent.h
                    #     # t_height_spent = (t.amount / largest_money) * chart_rect.h
                    #     # print("e", ent, "t", t, "t_height_spent:", t_height_spent)
                    #     t_rect_spent = game.Rect(col_rect_spent.x, t_curr_y_spent, col_rect_spent.w, t_height_spent)
                    #     t_in_rect_spent = t_rect_spent
                    #     t_in_rect_spent.x += border_width
                    #     t_in_rect_spent.y += border_width
                    #     t_in_rect_spent.w -= 2 * border_width
                    #     t_in_rect_spent.h -= 2 * border_width
                    #
                    #     # if t.entity_to == ent:
                    #     t_curr_y_spent += t_height_spent
                    #     drawables.append((game.draw.rect, (display, RED, t_rect_spent)))
                    #     drawables.append((game.draw.rect, (display, BLUE, t_in_rect_spent)))
                    #     # else:
                    #     #     drawables.append((game.draw.rect, (display, GREEN, t_rect)))
                    #     #     drawables.append((game.draw.rect, (display, LIMEGREEN, t_in_rect_spent)))

                    drawables.append((write_text, (game, display, game.Rect(col_rect_spent.x, col_rect_spent.y - 20, col_rect_spent.w, 20), money(ent.balance), game.font.SysFont("Arial", 12))))

                    c += 1
                    name_rect_spent = game.Rect(col_rect_spent.x, col_rect_spent.y + col_rect_spent.h + top_name_space, col_rect_spent.w, title_height)
                    drawables.append((write_text, (game, display, name_rect_spent, ent.name, game.font.SysFont("Arial", 12))))
        elif CHART_VIEW_MODE == SUM_OF_MONEY_EARNED_V_SPENT:
            largest_money = max([max(abs(e.spending_balance), abs(e.earning_balance)) for e in logbook_3.entities_list if e != e_pot])
            largest_money = max(largest_money, logbook_3.even_pot_split())
            for i, ent in enumerate(logbook_3.entities_list):
                if ent.id_num != e_pot.id_num:
                    col_rect_spent = game.Rect(
                        chart_rect.x + (c * ((entity_col_w / 1) + entity_col_offset)) + (entity_col_offset / (1 / 3)),
                        chart_rect.y + top_chart_offset, (entity_col_w / 2),
                        chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height))
                    col_rect_spent.x += entity_col_offset  # not quite
                    col_rect_earned = game.Rect(
                        chart_rect.x + (c * ((entity_col_w / 1) + entity_col_offset)) + (entity_col_offset / (1 / 3)) + (entity_col_w / 2),
                        chart_rect.y + top_chart_offset, (entity_col_w / 2),
                        chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height))
                    col_rect_earned.x += entity_col_offset  # not quite
                    col_rects.append((i, col_rect_spent))
                    col_rects.append((i, col_rect_earned))

                    # print("ent.balance / largest_money", ent.balance / largest_money)
                    money_spent = abs(ent.spending_balance)
                    money_earned = abs(ent.earning_balance)
                    col_rect_spent.h *= abs(money_spent / largest_money)
                    col_rect_earned.h *= abs(money_earned / largest_money)
                    col_rect_spent.y = (chart_rect.y + chart_rect.h) - (col_rect_spent.h + bottom_chart_offset)
                    col_rect_earned.y = (chart_rect.y + chart_rect.h) - (col_rect_earned.h + bottom_chart_offset)

                    # game.draw.rect(display, random_color(), col_rect_spent)
                    drawables.append((game.draw.rect, (display, BLACK, col_rect_spent)))
                    drawables.append((game.draw.rect, (display, BLACK, col_rect_earned)))
                    t_curr_y_spent = col_rect_spent.y
                    t_curr_y_earned = col_rect_earned.y
                    for j, t in enumerate(ent.transactions_list):
                        t_height_spent = abs(t.amount / max(1, money_spent)) * col_rect_spent.h
                        t_height_earned = abs(t.amount / max(1, money_earned)) * col_rect_earned.h
                        # t_height_spent = (t.amount / largest_money) * chart_rect.h
                        # print("e", ent, "t", t, "t_height_spent:", t_height_spent)
                        t_rect_spent = game.Rect(col_rect_spent.x, t_curr_y_spent, col_rect_spent.w, t_height_spent)
                        t_rect_earned = game.Rect(col_rect_earned.x, t_curr_y_earned, col_rect_earned.w, t_height_earned)
                        t_in_rect_spent = t_rect_spent
                        t_in_rect_spent.x += border_width
                        t_in_rect_spent.y += border_width
                        t_in_rect_spent.w -= 2 * border_width
                        t_in_rect_spent.h -= 2 * border_width
                        t_in_rect_earned = t_rect_earned
                        t_in_rect_earned.x += border_width
                        t_in_rect_earned.y += border_width
                        t_in_rect_earned.w -= 2 * border_width
                        t_in_rect_earned.h -= 2 * border_width

                        if t.entity_from == ent:
                            t_curr_y_spent += t_height_spent
                            drawables.append((game.draw.rect, (display, RED, t_rect_spent)))
                            drawables.append((game.draw.rect, (display, BLUE, t_in_rect_spent)))
                        else:
                            t_curr_y_earned += t_height_earned
                            drawables.append((game.draw.rect, (display, GREEN, t_rect_earned)))
                            drawables.append((game.draw.rect, (display, LIMEGREEN, t_in_rect_earned)))

                    drawables.append((write_text, (game, display, game.Rect(col_rect_spent.x, col_rect_spent.y - 20, col_rect_spent.w, 20), money(abs(ent.spending_balance)), game.font.SysFont("Arial", 12))))
                    drawables.append((write_text, (game, display, game.Rect(col_rect_earned.x, col_rect_earned.y - 20, col_rect_earned.w, 20), money(abs(ent.earning_balance)), game.font.SysFont("Arial", 12))))

                    c += 1
                    name_rect_spent = game.Rect(col_rect_spent.x, col_rect_spent.y + col_rect_spent.h + top_name_space, col_rect_spent.w + col_rect_earned.w, title_height)
                    drawables.append((write_text, (game, display, name_rect_spent, ent.name, game.font.SysFont("Arial", 12))))

        if col_rects:
            if include_negatives:
                even_y = (chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height)) * abs(logbook_3.even_pot_split() / largest_money)
                even_y = (chart_rect.y + chart_rect.h) - (even_y + bottom_chart_offset)
                even_paid_line = Line(col_rects[0][1].x, even_y, col_rects[-1][1].right, even_y)
                drawables.append((game.draw.line, (display, ORANGE, even_paid_line.p1, even_paid_line.p2, 3)))

                space_tick = (chart_rect.h - bottom_chart_offset - top_offset) / largest_money
                t_rect_h = (chart_rect.h - bottom_chart_offset - top_chart_offset) / max(1, ((largest_money // 100) + 1))
                for i in range(0, ceil(largest_money + 100) + int(smallest_money), 100):
                    tick_rect = game.Rect(chart_rect.x + 5, i * space_tick, 2 * entity_col_offset, t_rect_h)
                    tick_rect.y = (chart_rect.y + chart_rect.h) - (tick_rect.y + bottom_chart_offset) - (t_rect_h / 2)
                    i += smallest_money
                    drawables.insert(0, (write_text, (game, display, tick_rect, str(i), game.font.SysFont("Arial", 12))))
                    drawables.insert(0, (game.draw.line, (display, GRAY_69, (col_rects[0][1].x, tick_rect.y + (tick_rect.h / 2)), (col_rects[-1][1].x + col_rects[-1][1].w, tick_rect.y + (tick_rect.h / 2)))))
            else:
                even_y = (chart_rect.h - (bottom_chart_offset + top_chart_offset + title_height)) * abs(logbook_3.even_pot_split() / largest_money)
                even_y = (chart_rect.y + chart_rect.h) - (even_y + bottom_chart_offset)
                even_paid_line = Line(col_rects[0][1].x, even_y, col_rects[-1][1].right, even_y)
                drawables.append((game.draw.line, (display, ORANGE, even_paid_line.p1, even_paid_line.p2, 3)))

                space_tick = (chart_rect.h - bottom_chart_offset - top_offset) / largest_money
                t_rect_h = (chart_rect.h - bottom_chart_offset - top_chart_offset) / max(1, ((largest_money // 100) + 1))
                for i in range(0, ceil(largest_money + 100), 100):
                    tick_rect = game.Rect(chart_rect.x + 5, i * space_tick, 2 * entity_col_offset, t_rect_h)
                    tick_rect.y = (chart_rect.y + chart_rect.h) - (tick_rect.y + bottom_chart_offset) - (t_rect_h / 2)
                    drawables.insert(0, (write_text, (game, display, tick_rect, str(i), game.font.SysFont("Arial", 12))))
                    drawables.insert(0, (game.draw.line, (display, GRAY_69, (col_rects[0][1].x, tick_rect.y + (tick_rect.h / 2)), (col_rects[-1][1].x + col_rects[-1][1].w, tick_rect.y + (tick_rect.h / 2)))))

        if drawables:
            for f, args in drawables:
                f(*args)

        print(dict_print({
            "largest_money": largest_money,
            "smallest_money": smallest_money,
        }))


    chart_view_ctrl_bar = ButtonBar(game, display, game.Rect(chart_rect.right + 30, chart_rect.y, 200, chart_rect.h), is_horizontal=False)
    chart_view_ctrl_bar.add_button("Sum of Money Handled", GOLD_3, YELLOW_2, change_chart, (SUM_OF_MONEY_HANDLED))
    chart_view_ctrl_bar.add_button("Sum of Money Earned", FORESTGREEN, GREEN_4, change_chart, (SUM_OF_MONEY_EARNED))
    chart_view_ctrl_bar.add_button("Sum of Money Spent", BWS_RED, RED_3, change_chart, (SUM_OF_MONEY_SPENT))
    chart_view_ctrl_bar.add_button("Sum of Money Spent VS Earned", GRAY_36, GRAY_60, change_chart, (SUM_OF_MONEY_EARNED_V_SPENT))
    chart_view_ctrl_bar.add_button("Balance", GRAY_36, GRAY_60, change_chart, (BALANCE))
    chart_view_ctrl_bar.add_button("All", GRAY_26, GRAY_50, change_chart, (ALL))


    # Main Loop
    change_chart(BALANCE)

    while app.is_playing:
        display.fill(BLACK)

        # draw widgets and objects here
        draw_chart()
        chart_view_ctrl_bar.draw()

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
    print("Even split::", money(logbook_3.even_pot_split()))
    for ent in logbook_3.entities_list:
        print(dict_print(ent.info_dict()))
