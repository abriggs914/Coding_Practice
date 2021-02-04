from display_func import *


# TODO should support variable multiplication recognition.
#   i.e.  "y = 3x" should be converted to "y = 3 * x"
#   "y = 3(x)" should be converted to "y = 3 * x"
#   "y = 3(x + 1)" should be converted to "y = 3 * (x + 1)"
#   "y = 3(1)" should be converted to "y = 3 * 1"

f1  = "y = mx+b", "y = m * x + b"
f2  = "y = m x + b", "y = m * x + b"
f3  = "y=mx+b", "y = m * x + b"
f4  = "y = m*x+b", "y = m * x + b"
f5  = "y = m*x +b", "y = m * x + b"
f6  = "y = m*x + b", "y = m * x + b"
f7  = "y = m *x+b", "y = m * x + b"
f8  = "y = m * x+b", "y = m * x + b"
f9  = "y = m * x +b", "y = m * x + b"
f10 = "y = m * x + b", "y = m * x + b"
f11 = "y = m*x+ b", "y = m * x + b"
f12 = "(y = ((m*(x)))+ b)", "y = m * x + b"
f13 = "((y) = (((m*(x)))+ (b)))", "y = m * x + b"
f14 = "y = 1 / x + 1", "     (  1  )     \ny =  ( ___ )  + 1\n     (  x  )     "
f15 = "y = 1 / ((x + 1) / 4 - 2)", "       (   )       \n      (  1  )      \ny =  (  ___  )  + 1\n      (  x  )      \n       (   )       "
f16 = "y = 1 / ((x + 1) / 4 - 2) + ((16 * x) / 9)", "         (             )           (        )  \n        (       1       )         (  16 * x  ) \ny =    (  _____________  )    +  (   ______   )\n      (     (       )     )       (     9    ) \n     (     (  x + 1  )     )       (        )  \n      (   (   _____   )   )                    \n       (   (  4 - 2  )   )                     \n        (   (       )   )                      \n         (             )                       "
f17 = "y = x ^ 2", "      (          ) \n     (         2  )\ny =  (  x  ^^     )\n      (          ) "
f18 = "y = x ^ (12 / x)", "        (                 )   \n       (           (    )  )  \n      (           (  12  )  ) \n     (           (   __   )  )\n     (            (   x  )   )\n      (            (    )   ) \ny =    (   x  ^^           )  \n        (                 )   "

# TODO for each of DIVISION, POWER, and LOG I need examples of every permutation and nested samples
#  Since each of the above functions require two operands, I also need samples of when the secondary operand is swapped
#  i.e. DIVISION: denominator swap with numerator
#  i.e. POWER: base swap with exponent
#  i.e. LOG: base swap with A-value

#		---		DIVISION EXAPMPLES	  --

# "y = 1 / x + 1"

# "       (   )       "
# "      (  1  )      "
# "y =  (  ___  )  + 1"
# "      (  x  )      "
# "       (   )       "

# "y = 1 / ((x + 1) / 4 - 2)"

# "     (               )     "
# "     (       1       )     "
# "y =  (  ___________  )  + 1"
# "     (  (         )  )     "
# "     (  (  x + 1  )  )     "
# "     (  (  _____  )  )     "
# "     (  (  4 - 2  )  )     "
# "     (  (         )  )     "
# "     (               )     "

# "         (             )         "
# "        (       1       )        "
# "y =    (  _____________  )    + 1"
# "      (     (       )     )      "
# "     (     (  x + 1  )     )     "
# "      (   (   _____   )   )      "
# "       (   (  4 - 2  )   )       "
# "        (   (       )   )        "
# "         (             )         "

# "y = 1 / ((x + 1) / 4 - 2) + ((16 * x) / 9)"

# "         (             )           (        )  "
# "        (       1       )         (  16 * x  ) "
# "y =    (  _____________  )    +  (   ______   )"
# "      (     (       )     )       (     9    ) "
# "     (     (  x + 1  )     )       (        )  "
# "      (   (   _____   )   )                    "
# "       (   (  4 - 2  )   )                     "
# "        (   (       )   )                      "
# "         (             )                       "

#		--	 POWER EXAMPLES	   --

# y = x ^ 2

# "      (          ) "
# "     (         2  )"
# "y =  (  x  ^^     )"
# "      (          ) "

# y = x ^ (12 / x)

# "        (                 )   "
# "       (           (    )  )  "
# "      (           (  12  )  ) "
# "     (           (   __   )  )"
# "     (            (   x  )   )"
# "      (            (    )   ) "
# "y =    (   x  ^^           )  "
# "        (                 )   "


#		--	 LOG EXAMPLES	   --

# y = log(10, x)

#       (        )
# y =  (  log  x  )
#      (     10   )
#       (        )

# y = log(10, ((3 * x) / 2))

#       (        )
# y =  (  log  x  )
#      (     10   )
#       (        )

#		--	OTHER EXAMPLES	  --

# y = m * x + b

# "y = m * x + b"


to_test = {}
names = ["f1", "f2", "f3", "f4", "f4", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13"]
tests = [f1, f2, f3, f4, f4, f6, f7, f8, f9, f10, f11, f12, f13]
# to_test = dict(zip(names, tests))
to_test["f1"] = f1
to_test["f2"] = f2
to_test["f3"] = f3
to_test["f4"] = f4
to_test["f5"] = f5
to_test["f6"] = f6
to_test["f7"] = f7
to_test["f8"] = f8
to_test["f9"] = f9
to_test["f10"] = f10
to_test["f11"] = f11
to_test["f12"] = f12
to_test["f13"] = f13
to_test["f14"] = f14
to_test["f15"] = f15
to_test["f16"] = f16
to_test["f17"] = f17
to_test["f18"] = f18
border = "".join(["#" for i in range(45)])
for n, t in to_test.items():
    # print("tst: " + str(t) + " tst[0]: " + str(t[0]) + " tst[1]: " + str(t[1]))
    func, results = t
    res = display_func(func)
    print(
        "{b}\n\t--  {n}  --\nFUNC ARGS: <<{a}>>\nRES: <<\n{r}\n>>\nDESIRED: <<\n{d}\n>>\nCORRECT: <<{c}>>\n{b}".format(
            n=n, b=border, a=func, r=res, d=results, c=res == results))

# for c in Chars:
# print("\n" + c.j_s+"\n")