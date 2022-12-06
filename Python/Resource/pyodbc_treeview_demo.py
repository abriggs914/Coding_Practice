import utility


def avg(*lst):
    print(f"average of {lst=}, {type(lst)=}")
    return utility.avg(*lst)


if __name__ == '__main__':

    from pyodbc_connection import *
    from tkinter_utility import *

    WIN = tkinter.Tk()
    WIN.geometry(f"800x600")
    WIN.title("Pyodbc + Treeview")
    df_IT_requests = connect("SELECT * FROM [IT Requests]")

    print(f"{df_IT_requests.columns=}")

    # tv_label_IT_requests, label_IT_requests, treeview_IT_requests, scroll_x_IT_requests, scroll_y_IT_requests = treeview_factory(WIN, df_IT_requests)
    treeview_controller = treeview_factory(
        WIN, df_IT_requests
        , aggregate_data={
            "LabourEstimate": avg,
            "LabourActual": avg,
            "RequestedBy": utility.mode
        }
    )
    frame_treeview_controller, \
    tv_label_treeview_controller, \
    label_treeview_controller, \
    treeview_treeview_controller, \
    scrollbar_x_treeview_controller, \
    scrollbar_y_treeview_controller, \
    (tv_button_new_item_treeview_controller, button_new_item_treeview_controller), \
    (tv_button_delete_item_treeview_controller, button_delete_item_treeview_controller), \
    aggregate_objects_treeview_controller\
        = treeview_controller.get_objects()

    frame_treeview_controller.grid()
    label_treeview_controller.grid()
    scrollbar_x_treeview_controller.grid()
    treeview_treeview_controller.grid()
    scrollbar_y_treeview_controller.grid(column=1)
    for i, data in enumerate(aggregate_objects_treeview_controller):
        if i > 0:
            tv, entry, x1x2 = data
            print(f"{i=}, {tv.get()=}")
            entry.grid(row=0, column=i)
        else:
            data.grid()
    WIN.mainloop()
