# Wasp Census

Analyze and visualize wasp social interaction data using pandas and plotly.

## Background

From June 3, 2019 to July 25, 2019 the movement of wasps between different nests was recorded. There were 84 wasps and 40 nests.

Each wasp was marked with a unique pattern of colors painted on its back. For example, the wasp recorded as "RGYW" had a pattern of red, green, yellow, and white.

## Usage

``` shell
git clone https://github.com/zatchl/wasp-census
cd wasp-census
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/python3 wasp_census.py
```

## wasp_census_2019.csv

|             | June 3           | June 4           | ... | July 25    |
| :---------: | ---------------- | ---------------- | --- | ---------- |
| **Nest 1**  | WWRR             | WWRR, GBYR       |     | WWRR, GBYR |
| **Nest 2**  | BYRW, WBRY, BBBB | BYRW, WBRY, RBRB |     | BYRW, WBRY |
|     ...     |                  |                  |     |            |
| **Nest 40** | YGRB             |                  |     | YGRB, BGRY |

## wasp_census.py

Currently *wasp_census.py* reads in *wasp_census_2019.csv* and creates an interaction table, a heatmap of the interaction table, and a summary table.

### Interaction table

The interaction table shows how many times each wasp was on the same nest as another wasp.

|          | WWRR | BYRW | WBRY | BBBB | GBYR | RBRB | ... |
| -------- | ---- | ---- | ---- | ---- | ---- | ---- | --- |
| **WWRR** | 0    | 0    | 0    | 0    | 2    | 0    |     |
| **BYRW** | 0    | 0    | 3    | 1    | 0    | 1    |     |
| **WBRY** | 0    | 3    | 0    | 1    | 0    | 1    |     |
| **BBBB** | 0    | 1    | 1    | 0    | 0    | 0    |     |
| **GBYR** | 2    | 0    | 0    | 0    | 0    | 0    |     |
| **RBRB** | 0    | 1    | 1    | 0    | 0    | 0    |     |
| ...      |      |      |      |      |      |      |     |

### Summary table

The summary table shows the number of days each wasp was seen, the number of nests each wasp visited, and the number of nest partners each wasp had.

|          | Days Seen | Nests Visited | Partners |
| -------- | --------- | ------------- | -------- |
| **WWRR** | 3         | 1             | 1        |
| **BYRW** | 3         | 1             | 3        |
| **WBRY** | 3         | 1             | 0        |
| **BBBB** | 0         | 1             | 1        |
| **GBYR** | 2         | 1             | 0        |
| **RBRB** | 0         | 1             | 1        |
| ...      |           |               |          |
