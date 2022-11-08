
if __name__ == '__main__':

    from pyodbc_connection import *
    from tkinter_utility import *

    WIN = tkinter.Tk()
    WIN.geometry(f"800x600")
    WIN.title("Pyodbc + Treeview")
    df_IT_requests = connect("SELECT * FROM [IT Requests]")

    tv_label_IT_requests, label_IT_requests, treeview_IT_requests, scroll_x_IT_requests, scroll_y_IT_requests = treeview_factory(WIN, df_IT_requests)
    label_IT_requests.grid()
    scroll_x_IT_requests.grid()
    treeview_IT_requests.grid()
    scroll_y_IT_requests.grid(column=1)
    WIN.mainloop()
