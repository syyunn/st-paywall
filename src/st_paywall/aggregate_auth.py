import streamlit as st
from .google_auth import get_logged_in_user_email, show_login_button
from .stripe_auth import is_active_subscriber, redirect_button
from .buymeacoffee_auth import get_bmac_payers

payment_provider = st.secrets.get("payment_provider", "stripe")

def add_auth(
    required: bool = True,
    login_button_text: str = "Login with Google",
    login_button_color: str = "#FD504D",
    login_sidebar: bool = True,

):
    st.write("add auth")
    st.write("required: " + str(required))
    
    if required:
        st.write("required auth")
        require_auth(
            login_button_text=login_button_text,
            login_sidebar=login_sidebar,
            login_button_color=login_button_color,
        )
    else:
        st.write("optional auth")
        optional_auth(
            login_button_text=login_button_text,
            login_sidebar=login_sidebar,
            login_button_color=login_button_color,
        )


def require_auth(
    login_button_text: str = "Login with Google",
    login_button_color: str = "#FD504D",
    login_sidebar: bool = True,
):
    st.write("require auth")
    user_email = get_logged_in_user_email()
    st.write("user_email: " + str(user_email))

    if not user_email:
        show_login_button(
            text=login_button_text, color=login_button_color, sidebar=login_sidebar
        )
        st.stop()

    if payment_provider == "stripe":
        is_subscriber = user_email and is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email and user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    # if not is_subscriber:
    #     redirect_button(
    #         text="Subscribe now!",
    #         customer_email=user_email,
    #         payment_provider=payment_provider,
    #     )
    #     st.session_state.user_subscribed = False
    #     st.stop()
    # elif is_subscriber:
    #     st.session_state.user_subscribed = True

    if st.sidebar.button("Logout", type="primary"):
        del st.session_state.token
        del st.session_state.email
        del st.session_state.user_subscribed
        st.rerun()


def optional_auth(
    login_button_text: str = "Login with Google",
    login_button_color: str = "#FD504D",
    login_sidebar: bool = True,
):
    st.write("optional auth")
    user_email = get_logged_in_user_email()
    if payment_provider == "stripe":
        is_subscriber = user_email and is_active_subscriber(user_email)
    elif payment_provider == "bmac":
        is_subscriber = user_email and user_email in get_bmac_payers()
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    if not user_email:
        show_login_button(
            text=login_button_text, color=login_button_color, sidebar=login_sidebar
        )
        st.session_state.email = ""
        st.sidebar.markdown("")

    # if not is_subscriber:
    #     redirect_button(
    #         text="Subscribe now!", customer_email="", payment_provider=payment_provider
    #     )
    #     st.sidebar.markdown("")
    #     st.session_state.user_subscribed = False

    # elif is_subscriber:
    #     st.session_state.user_subscribed = True

    if st.session_state.email != "":
        if st.sidebar.button("Logout", type="primary"):
            del st.session_state.email
            del st.session_state.user_subscribed
            st.rerun()
