

class e(Exception):
    def __init__(self, msg=""):
        super().__init__(msg)

m = "raised exception"
for i in range(6):
    print(i)
    if i == 4:
        raise e(m)