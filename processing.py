from datetime import datetime
from pathlib import Path
import pandas as pd


CSV_FILE = "IEC_wirelibrary_tic elkas_V22.csv"


def _now_topconvert_line() -> str:
    now = datetime.now()
    return now.strftime("; ***** TopConvert: %A, %B %d, %Y   %H:%M:%S *****")


def _normalize_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_cross_section(value) -> str:
    text = _normalize_text(value).replace(",", ".")
    if not text:
        return ""
    try:
        number = float(text)
        if number.is_integer():
            return str(int(number))
        return str(number)
    except ValueError:
        return text


def _cross_section_to_terminal_code(cross_section: str) -> str:
    normalized = _normalize_cross_section(cross_section)

    mapping = {
        "0.75": "FER8_075",
        "1": "FER8_100",
        "1.5": "FER8_150",
        "2.5": "FER8_250",
        "4": "FER10_400",
    }

    if normalized not in mapping:
        raise ValueError(f"Nepalaikoma kvadratūra terminalui: {cross_section}")

    return mapping[normalized]


def _load_wire_database(csv_file: str = CSV_FILE) -> pd.DataFrame:
    csv_path = Path(csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"Nerastas CSV failas: {csv_file}")

    df = pd.read_csv(csv_path, sep=";")
    df["Color_norm"] = df["Color"].astype(str).str.strip()
    df["CrossSectionMM2_norm"] = (
        df["CrossSectionMM2"]
        .astype(str)
        .str.strip()
        .str.replace(",", ".", regex=False)
    )
    return df


def _find_wire_row(df: pd.DataFrame, color: str, cross_section: str) -> pd.Series:
    color_norm = _normalize_text(color)
    cross_norm = _normalize_cross_section(cross_section)

    matches = df[
        (df["Color_norm"] == color_norm) &
        (df["CrossSectionMM2_norm"] == cross_norm)
    ]

    if matches.empty:
        raise ValueError(
            f"CSV nerastas įrašas spalvai '{color_norm}' ir kvadratūrai '{cross_norm}'."
        )

    if len(matches) > 1:
        raise ValueError(
            f"CSV rasti keli įrašai spalvai '{color_norm}' ir kvadratūrai '{cross_norm}'."
        )

    return matches.iloc[0]


def _filter_wires(wires: list[dict]) -> list[dict]:
    filtered = []
    for wire in wires:
        if any(_normalize_text(v) for v in wire.values()):
            filtered.append(wire)
    return filtered


def build_job_content(project: str) -> str:
    project = _normalize_text(project)

    lines = [
        _now_topconvert_line(),
        "",
        "[NewJob]",
        f"\tJob = {project}, 1",
        f"\tArticleKey = {project}_001",
        "\tTotalPieces = 1",
        "\tBatchSize = 1",
    ]
    return "\n".join(lines)


def build_article_content(wires: list[dict], csv_file: str = CSV_FILE) -> str:
    wires = _filter_wires(wires)
    if not wires:
        raise ValueError("Nėra nei vieno užpildyto laido.")

    project = _normalize_text(wires[0].get("project", ""))
    if not project:
        raise ValueError("Projektas neužpildytas.")

    df = _load_wire_database(csv_file)

    lines = [
        _now_topconvert_line(),
        "",
        "[DeleteArticle]",
        f"\tArticleKey = {project}_001",
        "",
        "[NewArticle]",
        f"\tArticleKey = {project}_001",
        f'\tName = "{project}"',
        "\tBundlingSide = 4",
        f"\tNumberOfLeadSets = {len(wires)}",
        "",
    ]

    for index, wire in enumerate(wires, start=1):
        component_1 = _normalize_text(wire.get("component_1", ""))
        point_1 = _normalize_text(wire.get("point_1", ""))
        component_2 = _normalize_text(wire.get("component_2", ""))
        point_2 = _normalize_text(wire.get("point_2", ""))
        wire_name = _normalize_text(wire.get("wire_name", ""))
        length = _normalize_text(wire.get("length_mm", ""))
        color = _normalize_text(wire.get("color", ""))
        cross_section = _normalize_cross_section(wire.get("cross_section", ""))

        row = _find_wire_row(df, color=color, cross_section=cross_section)

        wire_key = _normalize_text(row["WireKey"])
        font_key = _normalize_text(row["FontKey"])
        terminal_key = _cross_section_to_terminal_code(cross_section)

        bundling_post_process = 2 if index == len(wires) else 0

        lines.extend([
            f"[NewLeadSet{index}]",
            "\tBundlingSide = 1",
            f"\tBundlingPostProcess = {bundling_post_process}",
            "\tBundlingCenterPostProcess = 0",
            f"\tWireKey = {wire_key}",
            f"\tWireLength = {length}",
            f"\tFontKey = {font_key}",
            f"\tTerminalKeyBegin = {terminal_key}",
            f"\tTerminalKeyEnd = {terminal_key}",
            "",
            f"[NewMarkingTextWire{index}-2]",
            f'\tMarkingTextBegin = 25, "{wire_name}", 0',
            f'\tMarkingTextBegin = 105, "-{component_1}:{point_1} {wire_name}", 0',
            f'\tMarkingTextEndless = 40, "-{component_1}:{point_1} {wire_name} -{component_2}:{point_2}", 0',
            f'\tMarkingTextEnd = 25, "{wire_name}", 1',
            f'\tMarkingTextEnd = 105, "{wire_name} -{component_2}:{point_2}", 1',
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


def generate_job_dds(
    project: str,
    output_file: str = "Job.dds",
) -> tuple[Path, str]:
    content = build_job_content(project)
    output_path = Path(output_file)
    output_path.write_text(content, encoding="utf-8")
    return output_path, content


def generate_article_dds(
    wires: list[dict],
    csv_file: str = CSV_FILE,
    output_file: str = "Article.dds",
) -> tuple[Path, str]:
    content = build_article_content(wires=wires, csv_file=csv_file)
    output_path = Path(output_file)
    output_path.write_text(content, encoding="utf-8")
    return output_path, content


def generate_all_dds(
    wires: list[dict],
    csv_file: str = CSV_FILE,
    job_output_file: str = "Job.dds",
    article_output_file: str = "Article.dds",
) -> dict:
    wires = _filter_wires(wires)
    if not wires:
        raise ValueError("Nėra nei vieno užpildyto laido.")

    project = _normalize_text(wires[0].get("project", ""))
    if not project:
        raise ValueError("Projektas neužpildytas.")

    job_path, job_content = generate_job_dds(
        project=project,
        output_file=job_output_file,
    )

    article_path, article_content = generate_article_dds(
        wires=wires,
        csv_file=csv_file,
        output_file=article_output_file,
    )

    return {
        "job_path": job_path,
        "job_content": job_content,
        "article_path": article_path,
        "article_content": article_content,
    }
