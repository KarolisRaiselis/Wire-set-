import streamlit as st

st.markdown("""
    <style>
    div[data-testid="stTextInput"] {
        margin-bottom: -30px;
    }
    div[data-testid="stNumberInput"] {
        margin-bottom: -30px;
    }
    </style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Wire-set", layout="wide")

st.title("Wire-set")
st.subheader("Laidų suvedimas")

if "rows" not in st.session_state:
    st.session_state.rows = 2

with st.form("wire_form"):
    wires = []

    # Viršutinė antraščių eilė
    top = st.columns(9)
    top[0].markdown("**Komponentas 1**")
    top[1].markdown("")
    top[2].markdown("**Komponentas 2**")
    top[3].markdown("")
    top[4].markdown("**Laido pav.**")
    top[5].markdown("**Ilgis (mm)**")
    top[6].markdown("**Spalva**")
    top[7].markdown("**Kvadratūra**")
    top[8].markdown("**Projektas**")

    # Apatinė antraščių eilė
    sub = st.columns(9)
    sub[0].markdown("Pav.")
    sub[1].markdown("Taškas")
    sub[2].markdown("Pav.")
    sub[3].markdown("Taškas")
    sub[4].markdown("")
    sub[5].markdown("")
    sub[6].markdown("")
    sub[7].markdown("")
    sub[8].markdown("")

    # Įvedimo eilutės
    for i in range(st.session_state.rows):
        cols = st.columns(9)

        c1 = cols[0].text_input("", key=f"c1_{i}")
        p1 = cols[1].text_input("", key=f"p1_{i}")
        c2 = cols[2].text_input("", key=f"c2_{i}")
        p2 = cols[3].text_input("", key=f"p2_{i}")
        name = cols[4].text_input("", key=f"name_{i}")
        length = cols[5].number_input("", min_value=0, step=1, key=f"len_{i}")
        color = cols[6].text_input("", key=f"color_{i}")
        cross = cols[7].text_input("", key=f"cross_{i}")
        project = cols[8].text_input("", key=f"proj_{i}")

        wires.append({
            "component_1": c1,
            "point_1": p1,
            "component_2": c2,
            "point_2": p2,
            "wire_name": name,
            "length_mm": length,
            "color": color,
            "cross_section": cross,
            "project": project,
        })
    st.markdown("""
    <div style="height:30px;"></div>
    """, unsafe_allow_html=True)
    left, mid, right = st.columns([6, 1, 1])

    with mid:
        add_row = st.form_submit_button("➕")

    with right:
        save = st.form_submit_button("💾 Išsaugoti")

if add_row:
    st.session_state.rows += 1
    st.rerun()

if save:
    st.success("Duomenys išsaugoti")
    st.write(wires)
