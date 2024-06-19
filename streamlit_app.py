import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    page_icon="👋",
)

st.write("# Welcome to User Study Dashboard! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This site is used to show demos for experiment ideas and docs for the Boolean query user studies.
    **👈 Select a demo from the sidebar** to see some examples.

    ### U1: AI query, Human query?
    - Collaborative docs [one drive](https://utoronto-my.sharepoint.com/:f:/g/personal/erica_lenton_utoronto_ca/Eg3L3NL8LNRJk2JNNXRXvg4BzyvXVlREIq9sf5usB2CGDA?e=5%3aDRoafw&at=9)
    - Personal docs [google doc](https://docs.google.com/document/d/1nTp0XsbzuAm5IYXl-QdAT7Ah89khAs_QU4oirNM-2Lc/edit?usp=sharing)
    ### U2: Good query, Bad query?
    - UQ MyResearch [send by email]()
"""
)