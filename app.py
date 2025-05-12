import streamlit as st

# --- Set session state defaults ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "login_prompted" not in st.session_state:
    st.session_state.login_prompted = False



# --- Conditional Pages ---
if st.session_state["logged_in"]:
    pages = {
        "Your account": [
            st.Page("pages/logout.py", title="Log out", icon=":material/logout:"),
            st.Page("pages/simu_history.py", title="Simulation History", icon=":material/history:"),
            st.Page("pages/settings.py", title="Settings", icon=":material/settings:"),
        ],
        "Simulations": [
            st.Page("pages/01_simu_basic.py", title="Simulation Basique", icon=":material/monitoring:"),
            st.Page("pages/02_simu_advanced.py", title="Simulation Avancée", icon=":material/monitoring:"),
            st.Page("pages/03_simu_advanced_v2.py", title="Simulation Avancée V2", icon=":material/monitoring:"),
            st.Page("pages/04_simu_pret_zero.py", title="Simulation Pret Zero", icon=":material/monitoring:"),
            st.Page("pages/06_simu_pret_in_fine.py", title="Simulation Pret In Fine", icon=":material/monitoring:"),
            st.Page("pages/09_simu_comparateur_pret.py", title="Simulation Comparateur", icon=":material/monitoring:"),
            st.Page("pages/11_simu_loyer_locatif.py", title="Simulation Loyer Locatif", icon=":material/monitoring:"),
        ],
        "Others": [
            st.Page("pages/about.py", title="About", icon=":material/info:"),
            st.Page("pages/faq.py", title="FAQ", icon=":material/help:"),
            st.Page("pages/contact.py", title="Contact", icon=":material/contacts_product:"),
        ],
    }
else:
    pages = {
        "Authentication": [
            st.Page("pages/login.py", title="Login", icon=":material/login:")
        ],
        "Simulations": [
            st.Page("pages/01_simu_basic.py", title="Simulation Basique", icon=":material/monitoring:"),
            st.Page("pages/02_simu_advanced.py", title="Simulation Avancée", icon=":material/monitoring:")
        ],
        "Others": [
            st.Page("pages/about.py", title="About", icon=":material/info:"),
            st.Page("pages/faq.py", title="FAQ", icon=":material/help:"),
            st.Page("pages/contact.py", title="Contact", icon=":material/contacts_product:"),
        ],
    }


# --- Render Navigation ---
pg = st.navigation(pages)

# --- Show Logo ---
st.logo("static/img/bank_logo.png", icon_image="static/img/bank_logo.png")

# --- Prompt for login on first visit ---
if not st.session_state["logged_in"] and not st.session_state["login_prompted"]:
    st.session_state["login_prompted"] = True
    st.switch_page("pages/login.py")  # <- you must have a `login.py` page in /pages
    
pg.run()
