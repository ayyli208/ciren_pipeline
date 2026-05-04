import re
from pathlib import Path

import pandas as pd


INPUT_XLSX = Path(r"d:\UMich\Senior Year\umtri\ciren_database\ciren_crash_summaries.xlsx")
OUTPUT_XLSX = Path(r"d:\UMich\Senior Year\umtri\ciren_database\ciren_crash_summaries_categorized.xlsx")

SCENARIOS = [
    "car_following",
    "cut_in",
    "lane_departure_opposite",
    "lane_departure_same",
    "left_turn_straight",
    "left_turn_turn",
    "right_turn_straight",
    "right_turn_turn",
    "roundabout_av_inside",
    "roundabout_av_outside",
    "traffic_signal",
    "vehicle_encroachment",
    "vru_at_crosswalk",
    "vru_without_crosswalk",
]


def _contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text) for p in patterns)


def classify_scenario(summary: str) -> str | None:
    if not isinstance(summary, str) or not summary.strip():
        return None

    s = summary.lower()

    has_left_turn = _contains_any(s, [r"\bleft turn", r"\bturning left", r"\bturned left"])
    has_right_turn = _contains_any(s, [r"\bright turn", r"\bturning right", r"\bturned right"])
    has_straight = _contains_any(s, [r"\bgoing straight", r"\bproceeding straight", r"\btraveling straight", r"\bcontinued straight"])
    has_signal = _contains_any(s, [r"\btraffic signal", r"\bsignal(?:ized)? intersection", r"\bred light", r"\bgreen light", r"\bstoplight"])

    has_roundabout = _contains_any(s, [r"\broundabout", r"\btraffic circle"])
    has_inside = _contains_any(s, [r"\binside lane", r"\binboard lane", r"\binner lane"])
    has_outside = _contains_any(s, [r"\boutside lane", r"\boutboard lane", r"\bouter lane"])

    has_vru = _contains_any(s, [r"\bpedestrian", r"\bbicycl", r"\bcyclist", r"\bskateboard", r"\bscooter"])
    has_crosswalk = _contains_any(s, [r"\bcrosswalk", r"\bmarked crossing", r"\bpedestrian crossing"])

    has_rear_end = _contains_any(s, [r"\brear[- ]end", r"\bstruck .*rear", r"\bfront .*struck .*rear", r"\bfollowing too closely"])
    has_cut_in = _contains_any(s, [r"\bcut[ -]?in", r"\bmerged? into .*lane", r"\bchanged lanes? into", r"\bentered .*lane in front of"])

    has_cross_center = _contains_any(
        s,
        [r"\bcrossed .*center", r"\binto oncoming", r"\boncoming lane", r"\bleft of center", r"\bopposing lane", r"\bwrong way"],
    )
    has_off_road = _contains_any(
        s,
        [r"\bleft the .*roadway", r"\bran off (the )?road", r"\bdeparted (the )?lane", r"\boff the (right|left) side", r"\broad departure"],
    )

    has_encroach = _contains_any(
        s,
        [r"\bencroach", r"\bdrifted into .*lane", r"\bentered .*lane", r"\bintruded into .*lane"],
    )

    # VRU first because these scenarios are specific and mutually important.
    if has_vru:
        if has_crosswalk:
            return "vru_at_crosswalk"
        return "vru_without_crosswalk"

    if has_roundabout:
        if has_inside:
            return "roundabout_av_inside"
        if has_outside:
            return "roundabout_av_outside"
        return None

    if has_left_turn and has_straight:
        return "left_turn_straight"
    if has_left_turn:
        return "left_turn_turn"
    if has_right_turn and has_straight:
        return "right_turn_straight"
    if has_right_turn:
        return "right_turn_turn"

    if has_rear_end:
        return "car_following"
    if has_cut_in:
        return "cut_in"

    if has_cross_center:
        return "lane_departure_opposite"
    if has_off_road:
        return "lane_departure_same"

    if has_encroach:
        return "vehicle_encroachment"
    if has_signal:
        return "traffic_signal"

    return None


def main() -> None:
    if not INPUT_XLSX.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_XLSX}")

    df = pd.read_excel(INPUT_XLSX)
    if "cirenid" not in df.columns or "crash_summary" not in df.columns:
        raise ValueError("Expected columns: cirenid, crash_summary")

    out = df.copy()
    out["scenario"] = out["crash_summary"].apply(classify_scenario)
    out = out[out["scenario"].notna()].copy()
    out = out.rename(columns={"cirenid": "ciren_id"})
    out = out[["ciren_id", "crash_summary", "scenario"]]

    out.to_excel(OUTPUT_XLSX, index=False)

    print(f"Input rows: {len(df)}")
    print(f"Matched rows: {len(out)}")
    print(f"Unmatched rows: {len(df) - len(out)}")
    print(f"Wrote: {OUTPUT_XLSX}")

    counts = out["scenario"].value_counts().sort_index()
    print("\nScenario counts:")
    for scenario in SCENARIOS:
        print(f"  {scenario}: {int(counts.get(scenario, 0))}")


if __name__ == "__main__":
    main()
