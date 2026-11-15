# Pitfalls in Synthetic Data Generation

Team Solon Superintelligence · High School Hack O/IO 2026 · Sleep on It

We compared the challenge’s synthetic sleep dataset with a CDC survey to see what a realistic average might hide. Average sleep was 7.1 hours in the synthetic file and 6.7 in the survey. The charts show where the similarities end, including a much stronger link between pulse and sleep in the synthetic file.

## Open the presentation

[Download the project ZIP](https://github.com/Zxchz/Solon-Superintelligence-OH-IO-Submission/archive/refs/heads/main.zip), unzip it, and double-click `index.html`. It runs offline in a browser. Use the arrow keys to advance and the Fullscreen button to present. Slides 11 and 12 explain the data, methods, and limitations.

## Data and analysis

- [Challenge data](data/sleep.csv) is the 374-record [Sleep Health and Lifestyle Dataset](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) by Laksika Tharmalingam (CC0).
- The comparison uses 4,423 participants from [CDC NHANES 2009–2010](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2009) and [2011–2012](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2011). The figures describe the unweighted survey sample.

To reproduce the charts, run this from the project folder with Python and pandas installed. [The analysis script](analyze.py) downloads the public NHANES files if they are missing.

```bash
python3 analyze.py nhanes-cache
```

[Three-minute demo narration](demo-script.md)
