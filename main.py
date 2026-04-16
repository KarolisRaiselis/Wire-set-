import streamlit as st

st.set_page_config(page_title="Wire-set", layout="wide")

st.title("Wire-set")
st.subheader("Laidų suvedimas")

if "rows" not in st.session_state:
    st.session_state.rows = 1

with st.form("wire_form"):

    # 🔹 Header (tik vieną kartą)
    header = st.columns(8)
    header[0].markdown("**Komponentas 1**")
    header[1].markdown("**Taškas 1**")
    header[2].markdown("**Komponentas 2**")
    header[3].markdown("**Taškas 2**")
    header[4].markdown("**Laido pav.**")
    header[5].markdown("**Spalva**")
    header[6].markdown("**Kvadratūra**")
    header[7].markdown("**Projektas**")

    wires = []

    # 🔹 Dinaminės eilutės
    for i in range(st.session_state.rows):
        cols = st.columns(8)

        component_1 = cols[0].text_input("", key=f"c1_{i}")
        point_1 = cols[1].text_input("", key=f"p1_{i}")
        component_2 = cols[2].text_input("", key=f"c2_{i}")
        point_2 = cols[3].text_input("", key=f"p2_{i}")
        wire_name = cols[4].text_input("", key=f"name_{i}")
        color = cols[5].text_input("", key=f"color_{i}")
        cross_section = cols[6].text_input("", key=f"cross_{i}")
        project = cols[7].text_input("", key=f"proj_{i}")

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

    # 🔹 Mygtukai apačioje dešinėje
    col_left, col_right = st.columns([6, 2])

    with col_right:
        add_row = st.form_submit_button("➕")
        save = st.form_submit_button("💾 Išsaugoti")

# 🔹 Veiksmai po submit
if add_row:
    st.session_state.rows += 1
    st.rerun()

if save:
    st.success("Duomenys išsaugoti")
    st.write(wires)
