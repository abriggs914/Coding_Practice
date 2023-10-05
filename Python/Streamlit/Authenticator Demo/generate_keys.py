import pickle
from pathlib import Path

import streamlit_authenticator as stauth

# How to Add a User Authentication Service (Login Form) in Streamlit
# https://www.youtube.com/watch?v=JoFGrSRj4X4

# How to Add a User Authentication Service (Login Form) in Streamlit + Database
# https://www.youtube.com/watch?v=eCbH2nPL9sU

users = {
    "Avery Briggs": ("abriggs", "password"),
    "Donald Duck": ("dduck", "quack"),
    "James Bond": ("007", "gun")
}

