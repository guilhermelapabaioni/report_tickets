import streamlit as st
import hashlib


def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_password():
    def password_entered():
        input_hash = hash_password(st.session_state["password"])
        if input_hash == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Senha de Acesso",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.info("Suporte: guilherme.baioni@t-systems.com")
        return False

    elif not st.session_state["password_correct"]:
        st.error("Senha incorreta. Tente novamente.")
        st.text_input(
            "Senha de Acesso",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False

    return True
