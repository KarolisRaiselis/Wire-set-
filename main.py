import streamlit as st
import pandas as pd
from processing import generate_all_dds

st.set_page_config(page_title="Wire-set", layout="wide")

st.markdown("""
<style>
div[data-testid="stMarkdownContainer"] p {
    margin-bottom: 2px;
}

div[data-testid="stTextInput"],
div[data-testid="stNumberInput"] {
    margin-bottom: -30px;
}
</style>
""", unsafe_allow_html=True)

st.title("Wire-set")
st.subheader("Laidų suvedimas")

import pandas as pd

df = pd.read_csv("IEC_wirelibrary_tic elkas_V22.csv", sep=";")

color_options = (
    df["Color"]
    .dropna()
    .astype(str)
    .str.strip()
    .loc[lambda x: x != ""]
    .unique()
    .tolist()
)

cross_section_options = (
    df["CrossSectionMM2"]
    .dropna()
    .astype(str)
    .str.strip()
    .loc[lambda x: x != ""]
    .tolist()
)

# spalvos
color_options = sorted(set(color_options))

# kvadratūra -> skaičius, tik iki 4 mm²
cross_section_options = sorted(
    {
        float(str(x).replace(",", "."))
        for x in cross_section_options
        if 0.75 <= float(str(x).replace(",", ".")) <= 4
    }
)

# jei nori rodyti kaip tekstą selectbox'e
cross_section_options = [str(x).replace(".0", "") for x in cross_section_options]

if "rows" not in st.session_state:
    st.session_state.rows = 2

with st.form("wire_form"):
    wires = []

    # Viršutinė antraščių eilė
    top = st.columns([2, 2, 1, 1, 1, 1, 1])

    with top[0]:
        st.markdown(
            "<div style='text-align:center'><b>Komponentas 1</b></div>",
            unsafe_allow_html=True
        )

    with top[1]:
        st.markdown(
            "<div style='text-align:center'><b>Komponentas 2</b></div>",
            unsafe_allow_html=True
        )

    top[2].markdown("**Laido pav.**")
    top[3].markdown("**Ilgis (mm)**")
    top[4].markdown("**Spalva**")
    top[5].markdown("**Kvadratūra**")
    top[6].markdown("**Projektas**")

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
        length = cols[5].text_input("", key=f"len_{i}")
        color = cols[6].selectbox(
            "",
            options=color_options,
            key=f"color_{i}"
        )

        cross = cols[7].selectbox(
            "",
            options=cross_section_options,
            key=f"cross_{i}"
        )
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

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

    left, mid, right = st.columns([6, 1, 1])

    with mid:
        add_row = st.form_submit_button("➕")

    with right:
        save = st.form_submit_button("💾 Išsaugoti")

if add_row:
    st.session_state.rows += 1
    st.rerun()

if save:
    try:
        result = generate_all_dds(wires)

        st.success("Sugeneruoti abu DDS failai")

        st.download_button(
            label="Atsisiųsti Job.dds",
            data=result["job_content"],
            file_name="Job.dds",
            mime="text/plain",
        )

        st.download_button(
            label="Atsisiųsti Article.dds",
            data=result["article_content"],
            file_name="Article.dds",
            mime="text/plain",
        )

    except Exception as e:
        st.error(f"Klaida: {e}")
