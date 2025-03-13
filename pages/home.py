import streamlit as st

# Custom CSS for Sidebar
st.markdown(
    """
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #825d6b;
            padding-top: 10px;
        }

        /* Sidebar title */
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            text-align: left;
            color: #ffffff;
            padding-left: 15px;
            margin-bottom: 15px;
        }

        /* Sidebar menu item */
        .sidebar-item {
            font-size: 18px;
            padding: 12px;
            margin: 8px 12px;
            border-radius: 8px;
            color: #ffffff;
            text-decoration: none;
            display: flex;
            align-items: center;
            transition: background 0.3s ease, color 0.3s ease;
        }

        .sidebar-item:hover {
            background-color: c4c4c4;
        }

        /* Active item */
        .sidebar-item-active {
            background-color: c4c4c4;
            font-weight: bold;
            border-left: 4px solid #ffffff;
            padding-left: 10px;
        }

        /* Icon spacing */
        .sidebar-item span {
            margin-right: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar title
st.sidebar.markdown('<div class="sidebar-title">Menu</div>', unsafe_allow_html=True)

# Sidebar menu buttons
pages = {
    "Home": "Home",
    "Model 1": "Loan",
    "Model 2": "Loan",
    "Model 3": "Loan",
    "Model 4": "Loan",
    "Model 5": "Loan"
}

# Create buttons for navigation
selected_page = None
for label, value in pages.items():
    if st.sidebar.button(label):
        selected_page = value

# Default to Home if nothing is selected
page = selected_page if selected_page else "Home"