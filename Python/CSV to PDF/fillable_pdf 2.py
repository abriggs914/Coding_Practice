
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas

c = canvas.Canvas('watermark.pdf')
# with open('testplot.png') as ti:
c.drawImage('testplot.png', 350, 550, width=150, height=150)
c.save()

with open("watermark.pdf", 'rb') as wm, open('QuoteEmail.pdf', 'rb') as tp:

    output_file = PdfFileWriter()
    watermark = PdfFileReader(wm)
    input_file = PdfFileReader(tp)

    page_count = input_file.getNumPages()
    for page_number in range(page_count):
        print("Plotting png to {} of {}".format(page_number, page_count))
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        output_file.addPage(input_page)

    with open('output.pdf', 'wb') as outputStream:
        output_file.write(outputStream)
