import streamlit as st
import os
import json
import hashlib
import secrets
import hmac
from datetime import datetime, timezone

USER_DB_FILE = "users.json"


# ==========================
# JSON USER DB HELPERS
# ==========================

def load_user_db() -> dict:
    """Load or initialize the user DB."""
    if not os.path.exists(USER_DB_FILE):
        return {"users": {}}
    with open(USER_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_user_db(db: dict) -> None:
    """Persist the user DB to disk."""
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


# ==========================
# PASSWORD HASHING
# ==========================

def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """
    Returns (salt, password_hash).

    Uses PBKDF2-HMAC-SHA256 with 100k iterations.
    """
    if salt is None:
        salt = secrets.token_hex(16)  # 32-char hex string

    pw_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    pw_hash = hashlib.pbkdf2_hmac("sha256", pw_bytes, salt_bytes, 100_000)
    return salt, pw_hash.hex()


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    _, pw_hash = hash_password(password, salt)
    # Use compare_digest to avoid timing attacks (overkill here, but good habit)
    return hmac.compare_digest(pw_hash, stored_hash)


# ==========================
# USER OPERATIONS
# ==========================

def register_user(username: str, password: str) -> tuple[bool, str]:
    """
    Attempt to register; returns (success, message).
    """
    username = username.strip()
    if not username:
        return False, "Username cannot be empty."

    db = load_user_db()
    users = db["users"]

    if username in users:
        return False, "Username already exists."

    salt, pw_hash = hash_password(password)
    now = datetime.now(timezone.utc).isoformat()

    users[username] = {
        "password_hash": pw_hash,
        "salt": salt,
        "first_access": now,
        "last_access": now,
        "times_accessed": 1,
    }

    save_user_db(db)
    return True, f"User '{username}' registered."


def login_user(username: str, password: str) -> tuple[bool, str]:
    """
    Attempt to log in; returns (success, message).
    If success, updates last_access and times_accessed.
    """
    username = username.strip()
    db = load_user_db()
    users = db["users"]

    if username not in users:
        return False, "Invalid username or password."

    user = users[username]

    if not verify_password(password, user["password_hash"], user["salt"]):
        return False, "Invalid username or password."

    # Update access stats
    now = datetime.now(timezone.utc).isoformat()
    user["last_access"] = now
    user["times_accessed"] = int(user.get("times_accessed", 0)) + 1

    save_user_db(db)
    return True, f"Welcome back, {username}!"


def change_user_password(username: str, old_password: str, new_password: str) -> tuple[bool, str]:
    """
    Change password for logged-in user.
    """
    db = load_user_db()
    users = db["users"]

    if username not in users:
        return False, "User not found."

    user = users[username]

    # Verify old password
    if not verify_password(old_password, user["password_hash"], user["salt"]):
        return False, "Old password is incorrect."

    # Set new password
    salt, pw_hash = hash_password(new_password)
    user["salt"] = salt
    user["password_hash"] = pw_hash

    save_user_db(db)
    return True, "Password updated successfully."


def get_user_stats(username: str) -> dict | None:
    db = load_user_db()
    return db["users"].get(username)


def show_login_register():
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username").lower()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            ok, msg = login_user(username, password)
            if ok:
                st.session_state.user = username
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    with tab_register:
        st.subheader("Create an account")
        with st.form("register_form"):
            username = st.text_input("New username").lower()
            password = st.text_input("New password", type="password")
            password2 = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Register")

        if submitted:
            if password != password2:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password should be at least 6 characters.")
            else:
                ok, msg = register_user(username, password)
                if ok:
                    st.success(msg)
                    st.info("You can now log in.")
                else:
                    st.error(msg)


def show_change_password() -> bool:

    if st.session_state.get("user") is None:
        st.error("You are not logged in.")
        st.stop()

    st.subheader("Change password")
    with st.form("change_password_form"):
        old_pw = st.text_input("Old password", type="password")
        new_pw = st.text_input("New password", type="password")
        new_pw2 = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Change password")

    if submitted:
        if new_pw != new_pw2:
            st.error("New passwords do not match.")
        elif len(new_pw) < 6:
            st.error("New password should be at least 6 characters.")
        else:
            ok, msg = change_user_password(st.session_state.user, old_pw, new_pw)
            if ok:
                st.success(msg)
                st.toast(body=msg, duration=8)
                return True
            else:
                st.error(msg)
    return False


def show_main_app():
    st.title("Protected App Area 🔐")
    username = st.session_state.user

    # Show basic stats
    stats = get_user_stats(username)
    if stats:
        st.write(f"**User:** `{username}`")
        st.write(f"First access: `{stats['first_access']}`")
        st.write(f"Last access: `{stats['last_access']}`")
        st.write(f"Times accessed: `{stats['times_accessed']}`")

    st.write("---")
    st.write("Your actual app content goes here…")

    st.write("---")
    show_change_password()

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()


def st_auth() -> bool:


    # ==========================
    # MAIN ROUTER
    # ==========================

    if st.session_state.get("user") is None:

        # ==========================
        # STREAMLIT UI
        # ==========================

        st.set_page_config(page_title="JSON Auth Demo", page_icon="🔐")

        if "user" not in st.session_state:
            st.session_state.user = None

        st.title("JSON-based Auth Example")
        show_login_register()
        return False
    else:
        # show_main_app()
        return True
