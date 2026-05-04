import streamlit as st

st.set_page_config(page_title="LMT Flight", layout="wide")

st.title("LMT Flight")
st.write("Web üzerinden düzenlendi!")

if st.button("Test"):
    st.success("Calisiyor!")
