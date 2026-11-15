"""Rebuild the app's aggregate data from the challenge CSV and the CDC's XPT files.

Requires pandas. Run: python3 analyze.py /path/to/nhanes-cache
Missing public XPT files are downloaded to the supplied cache.
"""
import argparse
import json
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

APP_DIR = Path(__file__).resolve().parent
BMI_CATEGORIES = ["Underweight", "Healthy weight", "Overweight", "Obesity"]
RELATIONSHIPS = [("Age", "Sleep"), ("Pulse", "Sleep"), ("Age", "Systolic BP")]
COMPONENTS = {
    "DEMO": ["RIDAGEYR"],
    "OCQ": ["OCD150"],
    "SLQ": ["SLD010H"],
    "BMX": ["BMXBMI"],
    "BPX": ["BPXPLS", "BPXSY1"],
    "PAQ": ["PAQ650", "PAQ655", "PAD660", "PAQ665", "PAQ670", "PAD675"],
}


def read_cycle(year, suffix, cache):
    tables = []
    for component, columns in COMPONENTS.items():
        name = f"{component}_{suffix}.XPT"
        path = cache / name
        if not path.is_file():
            url = f"https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/{name}"
            download = path.with_suffix(".part")
            urlretrieve(url, download)
            download.replace(path)
        tables.append(pd.read_sas(path).set_index("SEQN")[columns])
    return pd.concat(tables, axis=1)


def weekly_minutes(frame, flag, days, minutes):
    valid_days = frame[days].where(frame[days].between(1, 7))
    valid_minutes = frame[minutes].where(frame[minutes].between(10, 1439))
    return (valid_days * valid_minutes).mask(frame[flag].eq(2), 0).where(frame[flag].isin([1, 2]))


def survey_sample(cache):
    frame = pd.concat([read_cycle(2009, "F", cache), read_cycle(2011, "G", cache)])
    cohort = frame.loc[
        frame.RIDAGEYR.between(27, 59)
        & frame.OCD150.isin([1, 2])
        & frame.SLD010H.between(2, 12)
    ]
    return pd.DataFrame({
        "Age": cohort.RIDAGEYR,
        "Sleep": cohort.SLD010H,
        "Pulse": cohort.BPXPLS.where(cohort.BPXPLS.gt(0)),
        "Systolic BP": cohort.BPXSY1.where(cohort.BPXSY1.gt(0)),
        "BMI": pd.cut(cohort.BMXBMI, [-float("inf"), 18.5, 25, 30, float("inf")],
                      labels=BMI_CATEGORIES, right=False),
        "Activity": weekly_minutes(cohort, "PAQ650", "PAQ655", "PAD660")
                    + weekly_minutes(cohort, "PAQ665", "PAQ670", "PAD675"),
    })


def synthetic_sample(frame):
    return pd.DataFrame({
        "Age": frame.Age,
        "Sleep": frame["Sleep Duration"],
        "Pulse": frame["Heart Rate"],
        "Systolic BP": frame["Blood Pressure"].str.split("/").str[0].astype(int),
        "BMI": frame["BMI Category"].replace({
            "Normal": "Healthy weight", "Normal Weight": "Healthy weight", "Obese": "Obesity"
        }),
        "Activity": frame["Physical Activity Level"],
    })


def short_sleep(frame):
    return int(frame.Sleep.lt(7).sum())


def counts(frame):
    return {"n": len(frame), "short": short_sleep(frame)}


def summarize(frame, activity_cutoff):
    bins = pd.cut(frame.Sleep, [-float("inf"), 5, 6, 7, 8, 9, 10, float("inf")], right=False)
    valid_activity = frame.dropna(subset=["Activity"])
    correlations = []
    for left, right in RELATIONSHIPS:
        pair = frame[[left, right]].dropna()
        correlations.append({"r": round(pair[left].corr(pair[right]), 6), "n": len(pair)})
    return {
        **counts(frame),
        "averageSleep": round(frame.Sleep.mean(), 6),
        "averagePulse": round(frame.Pulse.mean(), 6),
        "pulseN": int(frame.Pulse.count()),
        "sleepBins": bins.value_counts(sort=False).tolist(),
        "bmi": [counts(frame.loc[frame.BMI.eq(label)]) for label in BMI_CATEGORIES],
        "correlations": correlations,
        "activity": [
            counts(valid_activity.loc[valid_activity.Activity.lt(activity_cutoff)]),
            counts(valid_activity.loc[valid_activity.Activity.ge(activity_cutoff)]),
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path, help="Directory for public NHANES XPT files")
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(APP_DIR / "data" / "sleep.csv")
    synthetic = synthetic_sample(raw)
    unique_rows = synthetic.loc[~raw.drop(columns="Person ID").duplicated()]
    result = {
        "synthetic": summarize(synthetic, 60),
        "survey": summarize(survey_sample(args.cache), 150),
        "duplicateCheck": {
            "n": len(unique_rows),
            "pulseSleepR": round(unique_rows.Pulse.corr(unique_rows.Sleep), 6),
        },
    }
    start_tag = '<script type="application/json" id="analysis">'
    index = APP_DIR / "index.html"
    before, data = index.read_text(encoding="utf-8").split(start_tag, maxsplit=1)
    _, after = data.split("</script>", maxsplit=1)
    index.write_text(before + start_tag + "\n" + json.dumps(result, separators=(",", ":"))
                     + "\n</script>" + after, encoding="utf-8")
