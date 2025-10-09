import os.path

from streamlit_utility import *
from pathlib import Path
import sys



# Point to the directory that *contains* the module you want
tv_series_file_path = r"C:\Users\abrig\Documents\Coding_Practice\Python\TV_series\main.py"
tv_shows_dir = Path(os.path.dirname(tv_series_file_path)).resolve()
if str(tv_shows_dir) not in sys.path:
    sys.path.insert(0, str(tv_shows_dir))

# Now you can import it like a normal module
import main as projectc_main  # watch out for name collisions
# projectc_main.some_function()

import main as tv_shows_module
# from tv_shows_module.main import series_list

st.write(tv_shows_module.series_list)


# with open(series_path, encoding="utf-8") as f:
#     code = f.read()
#     st.write(code[:50])
#     e_code = eval(code)
#     st.write(type(e_code))