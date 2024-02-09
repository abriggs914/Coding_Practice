from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import String
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet



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


    test_3()