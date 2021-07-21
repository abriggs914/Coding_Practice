from utility import *

# from reportlab.graphics.shapes import Drawing, String
# from reportlab.lib.colors import *
# from reportlab.graphics import shapes,renderPDF
# from reportlab.graphics.charts.piecharts import Pie
# d = Drawing(400,200)
# d.add(String(100,175,"Without labels", textAnchor="middle"))
# d.add(String(300,175,"With labels", textAnchor="middle"))
# pc = Pie()
# pc.x = 25
# pc.y = 50
# pc.data = [10,20,30,40,50,60]
# pc.slices[0].popout = 5
# d.add(pc, 'pie1')
# pc2 = Pie()
# pc2.x = 150
# pc2.y = 50
# pc2.data = [10,20,30,40,50,60]
# pc2.labels = ['a','b','c','d','e','f']
# d.add(pc2, 'pie2')

########################################################################################################################

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import magenta, pink, blue, green


def create_simple_form():
    c = canvas.Canvas('simple_form.pdf')

    c.setFont("Courier", 20)
    c.drawCentredString(300, 700, 'Employment Form')
    c.setFont("Courier", 14)
    form = c.acroForm

    c.drawString(10, 650, 'First Name:')
    form.textfield(name='fname', tooltip='First Name',
                   x=110, y=635, borderStyle='inset',
                   borderColor=magenta, fillColor=pink,
                   width=300,
                   textColor=blue, forceBorder=True)

    c.drawString(10, 600, 'Last Name:')
    form.textfield(name='lname', tooltip='Last Name',
                   x=110, y=585, borderStyle='inset',
                   borderColor=green, fillColor=magenta,
                   width=300,
                   textColor=blue, forceBorder=True)

    c.drawString(10, 550, 'Address:')
    form.textfield(name='address', tooltip='Address',
                   x=110, y=535, borderStyle='inset',
                   width=400, forceBorder=True)

    c.drawString(10, 500, 'City:')
    form.textfield(name='city', tooltip='City',
                   x=110, y=485, borderStyle='inset',
                   forceBorder=True)

    c.drawString(250, 500, 'State:')
    form.textfield(name='state', tooltip='State',
                   x=350, y=485, borderStyle='inset',
                   forceBorder=True)

    c.drawString(10, 450, 'Zip Code:')
    form.textfield(name='zip_code', tooltip='Zip Code',
                   x=110, y=435, borderStyle='inset',
                   forceBorder=True)

    # form.
    print(dict_print({
        "dir()": dir(form),
        "referenceMap": form.referenceMap,
        "Value 1": form.getRef("zip_code"),
        "Value 2": form.getRefStr("zip_code"),
        "Fields 1": form.fields[0].format,
        "Fields 2": form.fields[0].name
    }))

    c.save()


if __name__ == '__main__':
    create_simple_form()


########################################################################################################################


#
# # simple_checkboxes.py
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfform
# from reportlab.lib.colors import magenta, pink, blue, green
#
#
# def create_simple_checkboxes():
#     c = canvas.Canvas('simple_checkboxes.pdf')
#
#     c.setFont("Courier", 20)
#     c.drawCentredString(300, 700, 'Pets')
#     c.setFont("Courier", 14)
#     form = c.acroForm
#
#     c.drawString(10, 650, 'Dog:')
#     form.checkbox(name='cb1', tooltip='Field cb1',
#                   x=110, y=645, buttonStyle='check',
#                   borderColor=magenta, fillColor=pink,
#                   textColor=blue, forceBorder=True)
#
#     c.drawString(10, 600, 'Cat:')
#     form.checkbox(name='cb2', tooltip='Field cb2',
#                   x=110, y=595, buttonStyle='cross',
#                   borderWidth=2, forceBorder=True)
#
#     c.drawString(10, 550, 'Pony:')
#     form.checkbox(name='cb3', tooltip='Field cb3',
#                   x=110, y=545, buttonStyle='star',
#                   borderWidth=1, forceBorder=True)
#
#     c.drawString(10, 500, 'Python:')
#     form.checkbox(name='cb4', tooltip='Field cb4',
#                   x=110, y=495, buttonStyle='circle',
#                   borderWidth=3, forceBorder=True)
#
#     c.drawString(10, 450, 'Hamster:')
#     form.checkbox(name='cb5', tooltip='Field cb5',
#                   x=110, y=445, buttonStyle='diamond',
#                   borderWidth=None,
#                   checked=True,
#                   forceBorder=True)
#
#     c.save()
#
#
# if __name__ == '__main__':
#     create_simple_checkboxes()