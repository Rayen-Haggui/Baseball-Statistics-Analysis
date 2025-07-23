# Baseball Statistics Analysis

A standalone Python tool for processing and analyzing baseball batting data. This repository provides functions to read CSV files, compute player statistics (batting average, on-base percentage, slugging percentage), filter data by year, and identify top performers by season or career.

---

## Features

* Read CSV data into list-of-dicts or nested-dicts
* Compute standard baseball metrics:

  * **Batting Average** (H/AB)
  * **On-Base Percentage** ((H+BB)/(AB+BB))
  * **Slugging Percentage** ((1B + 2×2B + 3×3B + 4×HR)/AB)
* Filter records by season year
* Aggregate career stats across seasons
* Select top N players by any metric and format results

---

## Project Structure

```
baseball-stats-analysis/
├── LICENSE
├── .gitignore
├── README.md
├── requirements.txt
└── src/
    └── baseball_stats.py
```

* `src/baseball_stats.py`: Core module containing all data processing and statistical functions.

---
