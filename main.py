with st.form("wire_form"):

    # 🔹 1 eilė (dideli headeriai)
    top = st.columns([2, 2, 1, 1, 1, 1, 1])
    top[0].markdown("**Komponentas 1**")
    top[1].markdown("**Komponentas 2**")
    top[2].markdown("")
    top[3].markdown("**Laido pav.**")
    top[4].markdown("**Ilgis (mm)**")
    top[5].markdown("**Spalva**")
    top[6].markdown("**Kvadratūra**")
    top[7].markdown("**Projektas**")

    # 🔹 2 eilė (sub-headeriai)
    sub = st.columns(8)
    sub[0].markdown("Pav.")
    sub[1].markdown("Taškas")
    sub[2].markdown("Pav.")
    sub[3].markdown("Taškas")
    sub[4].markdown("")
    sub[5].markdown("")
    sub[6].markdown("")
    sub[7].markdown("")

    wires = []

    # 🔹 Input eilutės
    for i in range(st.session_state.rows):
        cols = st.columns(8)

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
