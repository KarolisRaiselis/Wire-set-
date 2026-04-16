import streamlit as st

st.set_page_config(page_title="Wire-set", layout="wide")

st.title("Wire-set")
st.subheader("Laido duomenų suvedimas")

with st.form("wire_form"):
    col1, col2 = st.columns(2)

    with col1:
        component_1 = st.text_input("Komponentas 1")
        point_1 = st.text_input("Komponento taškas 1")
        wire_name = st.text_input("Laido pavadinimas")
        color = st.text_input("Spalva")

    with col2:
        component_2 = st.text_input("Komponentas 2")
        point_2 = st.text_input("Komponento taškas 2")
        cross_section = st.text_input("Kvadratūra")
        project = st.text_input("Projektas")

    submitted = st.form_submit_button("Išsaugoti")

if submitted:
    wire_data = {
        "component_1": component_1,
        "point_1": point_1,
        "component_2": component_2,
        "point_2": point_2,
        "wire_name": wire_name,
        "color": color,
        "cross_section": cross_section,
        "project": project,
    }

    st.success("Duomenys išsaugoti")
    st.write(wire_data)
