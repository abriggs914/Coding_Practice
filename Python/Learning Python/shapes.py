BOX_SHAPE = """
xxx
x x
xxx
"""

TRIANGLE_SHAPE = """
  x 
 x x
xxxxx
"""

QUESTION_SHAPE = """
  x
 x x
x   x
   x
  x
  x

  x
"""

def draw_shape(name, char):
  if name == 'box':
    return BOX_SHAPE.replace('x', char)
  elif name == 'triangle':
    return TRIANGLE_SHAPE.replace('x', char)
  else:
    return QUESTION_SHAPE.replace('x', char)
