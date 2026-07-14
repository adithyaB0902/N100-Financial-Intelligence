import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Financial Intelligence")

st.sidebar.success("Select a page from the sidebar.")

st.markdown("""
Welcome to the **N100 Financial Intelligence Dashboard**.

### Available Modules
- 🏠 Home
- 🏢 Company Profile
- 🔍 Financial Screener
- 👥 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports

Use the navigation menu on the left to open each screen.
""")