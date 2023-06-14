import easyocr
import streamlit as st
reader = easyocr.Reader(['en','ko']) # this needs to run only once to load the model into memory
result = reader.readtext('nobrand.jpg', detail = 0, paragraph=True)

st.text(result)
