import streamlit as st
# from st_paywall import add_auth # now I see.. they were imported from the "installed" version of st_paywall

from src.st_paywall import add_auth

st.set_page_config(layout="centered")

# initialize session state
if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is not None:
    st.write("token is not none")
    st.write(st.session_state.token)
    st.write("email is " + str(st.session_state.token["email"]))
else:
    st.write("token is none")

add_auth(
    required=True,
    login_button_text="Login with Google",
    login_button_color="#FD504D",
    login_sidebar=False,
)

# st.write("Congrats, you are subscribed!")
# st.write("the email of the user is " + str(st.session_state.email))
