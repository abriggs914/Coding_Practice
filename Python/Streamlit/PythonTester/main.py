import streamlit as st
from itertools import permutations


st.set_page_config(
    page_title="Python Tester",
    layout="wide"
)


params = [
    a := -1,
    b := -1.26,
    c := 0,
    d := None,
    e := list(),
    f := tuple(),
    g := set(),
    h := dict(),
    i := True,
    j := False,
    k := "",
    l := "A",
    m := "6.32",
    n := [-8, -6, -4, -2, 0, 2, 4, 6, 8],
    o := (-8, -6, -4, -2, 0, 2, 4, 6, 8),
    p := [{"user": "a", "id": 0}, {"user": "b", "id": 1}, {"user": "c", "id": 2}, {"user": "d", "id": 3}, {"user": "e", "id": 4}],
    q := dict(x=5, y=5, w=20, h=50),
    r := "Long text in a sentence"
]

selectbox_options = sorted(list(map(str, params)))
selectbox_parameters = st.multiselect(
    "Select Parameters:",
    selectbox_options,
    default=selectbox_options
)


def process_0(items=[]):
    items.append(1)
    return items


def process_1(items=None):
    if items is None:
        items = []
    items.append(1)
    return items


def unique(items):
    return list(set(items))


funcs = {
    "unique": {
        "f": unique,
        "np": 1
    },
    "process": [
        {"f": process_0, "n": "process_0", "np": 1},
        {"f": process_1, "n": "process_1", "np": 1}
    ]
}


for func_name, func_datas in funcs.items():
    do_compare = isinstance(func_datas, (list, tuple))
    if not do_compare:
        func_datas = [func_datas]
    with st.container(horizontal=True):
        if do_compare:
            st.header(func_datas[0].get("n", func_name))
            st.header(func_datas[1].get("n", func_name))
        else:
            st.header(func_name)
    cols_results = st.columns(2 * len(func_datas))
    for i, func_data in enumerate(func_datas):
        func = func_data["f"]
        func_name = func_data.get("n", func_name)
        num_p = func_data["np"]
        params_to_use = [p for p in params.copy() if str(p) in selectbox_parameters]
        param_perms = permutations(params, num_p)
        passes, failures = [], []
        for ps in param_perms:
            try:
                v = func(*ps)
                # st.write(f"{func_name}(*{list(ps)}) => {v}")
                passes.append((ps, v))
            except Exception as e:
                # st.write(f"Could not apply {func_name} to {list(ps)} => {e}")
                failures.append((ps, e))
        
        with cols_results[2 * i]:
            st.subheader("Passes")
            for ps, v in passes:
                with st.container(horizontal=True):
                    st.write(f"{ps}")
                    st.success(v)
        with cols_results[(2 * i) + 1]:
            st.subheader("Failures")
            for ps, e in failures:
                with st.container(horizontal=True):
                    st.write(f"{ps}")
                    st.error(e)
    st.divider()


from tabulate import tabulate

data = [["Name", "Country", "Program"],
        ["Chi", "Vietnam", "Graduate"],
        ["John", "USA", "Graduate"],
        ["Lily", "Belgium", "Graduate"]]

# Display the table in the console using a grid format
print(tabulate(data, headers="firstrow", tablefmt="grid"))
