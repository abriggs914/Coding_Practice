import utility


def avg(*lst):
    # print(f"average of {lst=}, {type(lst)=}")
    return utility.avg(*lst)


def remove_lst_marks(str_in):
    if not isinstance(str_in, str):
        str_in = str(str_in)
    return str_in.replace("[", "").replace("]", "").replace("'", "")



if __name__ == '__main__':

    from pyodbc_connection import *
    from tkinter_utility import *

    WIN = tkinter.Tk()
    WIN.geometry(f"800x600")
    WIN.title("Pyodbc + Treeview")
    df_IT_requests = connect("SELECT * FROM [IT Requests]")

    treeview_controller = treeview_factory(
        WIN, df_IT_requests
        , viewable_column_names=[
            "RequestDate",
            "Status",
            "Request",
            "RequestedBy",
            "LabourEstimate",
            "LabourActual",
            "Comments"
        ]
        , aggregate_data={
            "LabourEstimate": (avg, "%.2f"),
            "LabourActual": avg,
            "RequestedBy": (utility.mode, remove_lst_marks)
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
    label_treeview_controller.grid(row=0)
    scrollbar_x_treeview_controller.grid(row=3, sticky="ew")
    treeview_treeview_controller.grid(row=1, column=0)
    scrollbar_y_treeview_controller.grid(row=1, column=1, sticky="ns")
    for i, data in enumerate(aggregate_objects_treeview_controller):
        if i > 0:
            tv, entry, x1x2 = data
            # print(f"{i=}, {tv.get()=}")
            entry.grid(row=0, column=i)
        else:
            data.grid(row=2)

    tv_label_treeview_controller.set("Almost forgot my title!")
    WIN.mainloop()
