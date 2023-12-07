def set_lst():
    global lst
    lst = list(range(1, 6))  # Added a closing parenthesis here


if __name__ == '__main__':
    lst = None
    set_lst()
    print(f"{lst}")
