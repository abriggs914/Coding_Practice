# Calculate and show the linear formula between 2 points.

p1 = (60,200)
p2 = (220,80)
p3 = (80,60)

m = lambda p1, p2 : (p2[1] - p1[1]) / (p2[0] - p1[0])
b = lambda m, x1, y1 : y1 - (m * x1)
formula = lambda p1, p2 : "y = " + str(m(p1, p2)) + "x + " + str(b(m(p1, p2), p1[0], p1[1]))

print("formula(p1, p2): " + str(formula(p1, p2)))
print("formula(p1, p3): " + str(formula(p1, p3)))
print("formula(p3, p2): " + str(formula(p3, p2)))