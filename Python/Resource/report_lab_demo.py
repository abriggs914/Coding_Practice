import datetime

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import String
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import nhl_api_utility

if __name__ == '__main__':

    def test_1():
        def generate_pdf(data, title):
            # Create a PDF document
            doc = SimpleDocTemplate("output.pdf", pagesize=letter)

            # Define the data for your table (4 columns by 8 rows)
            table_data = [data[i:i + 4] for i in range(0, len(data), 4)]

            # Define styles for the table and title
            styles = getSampleStyleSheet()
            title_style = styles["Title"]
            table_style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])

            # Create a title
            title_text = Paragraph(title, title_style)

            # Create a table
            table = Table(table_data)

            # Apply styles to the table
            table.setStyle(table_style)

            # Add title and table to the document
            doc.build([title_text, table])


        # Example data and title
        data = ["Data1", "Data2", "Data3", "Data4",
                "Data5", "Data6", "Data7", "Data8",
                "Data9", "Data10", "Data11", "Data12",
                "Data13", "Data14", "Data15", "Data16",
                "Data17", "Data18", "Data19", "Data20",
                "Data21", "Data22", "Data23", "Data24",
                "Data25", "Data26", "Data27", "Data28",
                "Data29", "Data30", "Data31", "Data32",
                "Data33", "Data34", "Data35", "Data36",
                "Data37", "Data38", "Data39", "Data40",
                "Data41", "Data42", "Data43", "Data44",
                "Data45", "Data46", "Data47", "Data48"]

        title = "Sample PDF"

        # Generate the PDF
        generate_pdf(data, title)


    def test_2():
        def generate_pdf(data, title):
            # Create a PDF document
            doc = SimpleDocTemplate("output.pdf", pagesize=letter)

            # Define the data for your table (4 columns by 8 rows)
            table_data = [data[i:i + 4] for i in range(0, len(data), 4)]

            # Define styles for the table and title
            styles = getSampleStyleSheet()
            title_style = styles["Title"]
            table_style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])

            # Create a title
            title_text = Paragraph(title, title_style)

            # Create a table
            table = Table(table_data)

            # Apply styles to the table
            table.setStyle(table_style)

            # Add title and table to the document
            doc.build([title_text, table])

            # Add checkboxes
            checkbox_symbol = "☐"  # Unicode symbol for unchecked box
            font_name = styles['Normal'].fontName
            font_size = styles['Normal'].fontSize
            checkbox_width = stringWidth(checkbox_symbol, font_name, font_size)
            checkbox_height = font_size

            for i in range(len(data)):
                col = i % 4
                row = i // 4
                x = col * 100 + 10
                y = (7 - row) * 20 + 10  # Invert the row since (0,0) is at the bottom-left in ReportLab
                checkbox_x = x - 2 * checkbox_width  # Adjust position for checkbox
                checkbox_y = y + 5  # Adjust position for checkbox
                checkbox_text = String(checkbox_x, checkbox_y, checkbox_symbol)  # Create a new checkbox for each item
                table_data[row][col] = [checkbox_text, Paragraph(data[i], styles['Normal'])]

            # Render PDF
            table = Table(table_data)
            table.setStyle(table_style)
            table.wrapOn(doc, 0, 0)
            table.drawOn(doc, 0, 0)
            doc.save()

        # Example data and title
        data = ["Item 1", "Item 2", "Item 3", "Item 4",
                "Item 5", "Item 6", "Item 7", "Item 8",
                "Item 9", "Item 10", "Item 11", "Item 12",
                "Item 13", "Item 14", "Item 15", "Item 16",
                "Item 17", "Item 18", "Item 19", "Item 20",
                "Item 21", "Item 22", "Item 23", "Item 24",
                "Item 25", "Item 26", "Item 27", "Item 28",
                "Item 29", "Item 30", "Item 31", "Item 32",
                "Item 33", "Item 34", "Item 35", "Item 36",
                "Item 37", "Item 38", "Item 39", "Item 40",
                "Item 41", "Item 42", "Item 43", "Item 44",
                "Item 45", "Item 46", "Item 47", "Item 48"]

        title = "Sample PDF"

        # Generate the PDF
        generate_pdf(data, title)


    def test_3():
        def generate_pdf(data, title):
            # Create a PDF canvas
            canvas = Canvas("output.pdf", pagesize=letter)

            # Define the size of the checkbox
            checkbox_size = 10

            # Define the position of the title
            title_x = 50
            title_y = 750

            # Define the starting position of the table
            table_x = 50
            table_y = 700

            # Define the row and column sizes
            row_height = 20
            col_width = 100

            # Draw the title
            styles = getSampleStyleSheet()
            title_text = Paragraph(title, styles["Title"])
            title_text.wrapOn(canvas, 400, 20)
            title_text.drawOn(canvas, title_x, title_y)

            # Draw the checkboxes and text
            for i, item in enumerate(data):
                col = i % 4
                row = i // 4
                x = table_x + col * col_width
                y = table_y - row * row_height
                canvas.drawString(x + checkbox_size + 5, y, item)
                canvas.rect(x, y - checkbox_size / 2, checkbox_size, checkbox_size, stroke=1, fill=0)

            # Save the PDF
            canvas.save()

        # Example data and title
        data = ["Item 1", "Item 2", "Item 3", "Item 4",
                "Item 5", "Item 6", "Item 7", "Item 8",
                "Item 9", "Item 10", "Item 11", "Item 12",
                "Item 13", "Item 14", "Item 15", "Item 16",
                "Item 17", "Item 18", "Item 19", "Item 20",
                "Item 21", "Item 22", "Item 23", "Item 24",
                "Item 25", "Item 26", "Item 27", "Item 28",
                "Item 29", "Item 30", "Item 31", "Item 32",
                "Item 33", "Item 34", "Item 35", "Item 36",
                "Item 37", "Item 38", "Item 39", "Item 40",
                "Item 41", "Item 42", "Item 43", "Item 44",
                "Item 45", "Item 46", "Item 47", "Item 48"]

        title = "Sample PDF"

        # Generate the PDF
        generate_pdf(data, title)


    def my_version_1():
        def generate_pdf(data, title):

            canvas_width, canvas_height = 600,  800
            now = datetime.datetime.now()
            # Create a PDF canvas
            canvas = Canvas(f"output_{now:%Y-%m-%d_%H%M%S}.pdf", pagesize=letter)
            canvas.setFont("Helvetica", 9)

            # Define the size of the checkbox
            checkbox_size = 10

            # Define the position of the title
            title_x = 50
            title_y = 750

            # Define the starting position of the table
            table_x = 50
            table_y = 700

            # Define the row and column sizes
            row_height = 20
            col_width = 135

            # Draw the title
            styles = getSampleStyleSheet()
            title_text = Paragraph(title, styles["Title"])
            title_text.wrapOn(canvas, canvas_width, 2)
            title_text.drawOn(canvas, title_x, title_y)

            box_row_max = {"p": 6, "t": 8}
            box_row_count = {"p": 0, "t": 0}

            # rows 0, 1, 2, 4, 5, 6 are 'player' rows and only have 6 rows max
            # rows 3 and 7 are player and 'team' rows, and need 8 rows in just the team cells

            # Draw the checkboxes and text
            for i, item in enumerate(data):
                row_key = "t" if i in (3, 7) else "p"
                col = i % 4
                row = i // 4
                x = table_x + col * col_width
                y = table_y - row * row_height
                print(f"{row_key=}, {item=}")
                canvas.drawString(x + checkbox_size + 5, y - 3, item)
                canvas.rect(x, y - checkbox_size / 2, checkbox_size, checkbox_size, stroke=1, fill=0)
                box_row_count[row_key] += 1
                box_row_count[row_key] %= box_row_max[row_key]
                # print(f"{row_key=}, {box_row_count=}")

            # Save the PDF
            canvas.save()

        # Example data and title
        data = ["Item 1", "Item 2", "Item 3", "Item 4",
                "Item 5", "Item 6", "Item 7", "Item 8",
                "Item 9", "Item 10", "Item 11", "Item 12",
                "Item 13", "Item 14", "Item 15", "Item 16",
                "Item 17", "Item 18", "Item 19", "Item 20",
                "Item 21", "Item 22", "Item 23", "Item 24",
                "Item 25", "Item 26", "Item 27", "Item 28",
                "Item 29", "Item 30", "Item 31", "Item 32",
                "Item 33", "Item 34", "Item 35", "Item 36",
                "Item 37", "Item 38", "Item 39", "Item 40",
                "Item 41", "Item 42", "Item 43", "Item 44",
                "Item 45", "Item 46", "Item 47", "Item 48"]

        title = "BWS 2024 NHL Playoff Pool"

        # Generate the PDF
        # generate_pdf(data, title)

        n_forward_boxes = 7
        n_defence_boxes = 3
        n_forwards_per_boxes = 6
        n_defence_per_boxes = 6
        n_teams_per_box = 8

        pool_boxes = nhl_api_utility.playoff_pool_sheet_view_only(
            n_forward_boxes=n_forward_boxes,
            n_defence_boxes=n_defence_boxes,
            n_forwards_per_boxes=n_forwards_per_boxes,
            n_defence_per_boxes=n_defence_per_boxes,
            kwargs_nhl_api_utility={
                "view_only": False,
                "max_query_hold_time": 60*60*24*2
            },
            do_save_api_handler=True,
            pool_texts=True
        )
        print(f"{pool_boxes=}")

        # prepped_pool_boxes = [[None]*4]*((8*6) + (1*5))
        # prepped_pool_boxes = [[None]*4]*(8*6)
        prepped_pool_boxes = [[None for j in range(4)] for i in range(8*6)]
        print(f"\n\n\tSTART\n{len(prepped_pool_boxes)=}, {prepped_pool_boxes=}")

        ordered_players = []
        cids = [0, 0, 0, 0]
        for conf, conf_data in pool_boxes.items():
            for position, position_data in conf_data.items():
                for i, box in enumerate(position_data):
                    # print(f"== {i=}, box={str(box)[:25]}")
                    col_idx = i % 4
                    for j, text in enumerate(box):
                        brn = j % 4
                        # x = j+((cids[2]//4)*8)+(((cids[2]*cids[3])//96)*24)
                        x = j+((cids[2]//4)*8)
                        y = col_idx + ((1+i) if (((cids[1] + 1) % 3) == 0) else 0)
                        # print(f"\t{cids=}, {x=}, {y=}, {i=}, {j=}, {col_idx=}, {brn=}, {(j*4)+i+(brn*8)=}, {(i*6)+j=}, {text=}")
                        print(f"\t{cids=}, {x=}, {y=}, {i=}, {j=}, {col_idx=}, {brn=}, {text=}")
                        # prepped_pool_boxes.insert((j*4)+i, pool_boxes[conf][position][i][j])
                        # # prepped_pool_boxes.insert(, pool_boxes[conf][position][i][j])
                        ordered_players.append(text)
                        # print(f'AAA = {prepped_pool_boxes[x]=}, {prepped_pool_boxes[x][y]=}')
                        prepped_pool_boxes[x][y] = text
                        cids[3] += 1
                    # if len(box) == 6:
                    #     prepped_pool_boxes[x+1][y] = None
                    #     prepped_pool_boxes[x+2][y] = None
                    # if len(box) == 6:
                    #     ordered_players.append(None)
                    #     ordered_players.append(None)
                    cids[2] += 1
                cids[1] += 1
            cids[0] += 1
        # # print(f"{len(ordered_players)=}, {ordered_players=}")
        #
        # # grouped = [ordered_players[i:i + 8] for i in range(0, len(ordered_players), 8)]
        #
        # for box in ordered_players[::8]:
        #     print(f"\t{box=}")

        # print(f"{ordered_players=}")
        # players_by_row = []
        # for i in range(6):
        #     # prepped_pool_boxes += ordered_players[::6+i] + [""] * 4
        #     x = len(ordered_players[i])
        #     players_by_row += [ordered_players[i::x]]
        #     print(f"{i=}, {x=}, {ordered_players[i::x]=}")
        #
        # print(f"{len(players_by_row)=}, {players_by_row=}")
        # zip_lsts = [[None]*8]*len(players_by_row)
        # zip_lsts += players_by_row
        #
        # for a, b, c, d, e, f, *g in zip(*zip_lsts):
        # # for a, b, c, d, *e in zip(*players_by_row):
        #     print(f"{a=}, {b=}, {c=}, {d=}, {e=}, {f=}, {g=}")
        #     # print(f"{a=}, {b=}, {c=}, {d=}, {e=}")
        #
        # prepped_pool_boxes = prepped_pool_boxes[:-4]
        #
        # p_conf_boxes = []
        # row_boxes = []
        #
        # # # # Top row West
        # # # prepped_pool_boxes += [f"East - Forward {i} (pick 1)" for i in range(1, 5)]
        # # # for j in range(4):
        # # #     for i in range(6):
        # # #         print(f"ROW1 ({i}, {j}) {((j + 1)*4)+i}, {(i*6)+j} = {pool_boxes['W']['F'][i][j]=}")
        # # #         # prepped_pool_boxes.append(pool_boxes['W']['F'][i][j])
        # # #         prepped_pool_boxes.insert((i*6)+j, pool_boxes['W']['F'][i][j])
        # #
        # # # space row
        # # prepped_pool_boxes += [" "] * 4
        # #
        # # # # 2nd row West
        # # # prepped_pool_boxes += [f"East - Forward {i} (pick 1)" for i in range(5, 9)]
        # # # for j in range(4, 8):
        # # #     for i in range(6):
        # # #         print(f"ROW2 ({i}, {j}) = {pool_boxes['W']['F'][i][j]=}")
        # # #         prepped_pool_boxes.append(pool_boxes['W']['F'][i][j])
        #
        print(f"\n\n\tEND\n{prepped_pool_boxes=}")
        for v in prepped_pool_boxes:
            print(f"lv={len(v)}, {v=}")
        #
        # # Generate the PDF
        # generate_pdf(prepped_pool_boxes, title)

    # test_3()
    my_version_1()