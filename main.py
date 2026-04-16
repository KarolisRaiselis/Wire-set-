import streamlit as st

st.set_page_config(page_title="Wire-set", layout="wide")

st.title("Wire-set")
st.subheader("Laidų suvedimas")

# 🔢 kiek eilučių turim
if "rows" not in st.session_state:
    st.session_state.rows = 1

# ➕ mygtukas pridėti eilutę
if st.button("➕ Pridėti laidą"):
    st.session_state.rows += 1

# 🧾 forma
with st.form("wire_form"):
    wires = []

    for i in range(st.session_state.rows):
        st.markdown(f"### Laidas {i+1}")

        cols = st.columns(8)

        component_1 = cols[0].text_input("Komponentas 1", key=f"c1_{i}")
        point_1 = cols[1].text_input("Taškas 1", key=f"p1_{i}")
        component_2 = cols[2].text_input("Komponentas 2", key=f"c2_{i}")
        point_2 = cols[3].text_input("Taškas 2", key=f"p2_{i}")
        wire_name = cols[4].text_input("Laido pav.", key=f"name_{i}")
        color = cols[5].text_input("Spalva", key=f"color_{i}")
        cross_section = cols[6].text_input("Kvadratūra", key=f"cross_{i}")
        project = cols[7].text_input("Projektas", key=f"proj_{i}")

        wires.append({
            "component_1": component_1,
            "point_1": point_1,
            "component_2": component_2,
            "point_2": point_2,
            "wire_name": wire_name,
            "color": color,
            "cross_section": cross_section,
            "project": project,
        })

    submitted = st.form_submit_button("Išsaugoti visus")

if submitted:
    st.success("Duomenys išsaugoti")
    st.write(wires)
