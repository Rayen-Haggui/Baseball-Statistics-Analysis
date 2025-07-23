"""
Baseball Statistics Analysis Module

Provides functions to read and process CSV files of batting data,
compute standard baseball metrics, filter by season, and identify
top performers by year or career.
"""

import csv

# Typical cutoff used for official statistics
MINIMUM_AB = 500


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields

    Returns:
      List of dicts mapping field names to values for each row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(
            csvfile, delimiter=separator, quotechar=quote
        )
        for row in reader:
            table.append(row)
    return table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields

    Returns:
      Dict of dicts keyed by keyfield value mapping to row dicts.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(
            csvfile, delimiter=separator, quotechar=quote
        )
        for row in reader:
            table[row[keyfield]] = row
    return table


def batting_average(info, batting_stats):
    """
    Compute batting average (H/AB) if AB >= MINIMUM_AB, else 0.
    """
    hits = float(batting_stats[info['hits']])
    at_bats = float(batting_stats[info['atbats']])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    return 0


def onbase_percentage(info, batting_stats):
    """
    Compute on-base percentage (H+BB)/(AB+BB) if AB >= MINIMUM_AB, else 0.
    """
    hits = float(batting_stats[info['hits']])
    at_bats = float(batting_stats[info['atbats']])
    walks = float(batting_stats[info['walks']])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    return 0


def slugging_percentage(info, batting_stats):
    """
    Compute slugging percentage ((1B+2*2B+3*3B+4*HR)/AB) if AB >= MINIMUM_AB, else 0.
    """
    hits = float(batting_stats[info['hits']])
    doubles = float(batting_stats[info['doubles']])
    triples = float(batting_stats[info['triples']])
    home_runs = float(batting_stats[info['homeruns']])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info['atbats']])
    if at_bats >= MINIMUM_AB:
        total_bases = (
            singles + 2 * doubles + 3 * triples + 4 * home_runs
        )
        return total_bases / at_bats
    return 0


def filter_by_year(statistics, year, yearid):
    """
    Filter list of stat dicts to only those matching given year.
    """
    res = []
    for stat in statistics:
        if int(stat[yearid]) == year:
            res.append(stat)
    return res


def top_player_ids(info, statistics, formula, numplayers):
    """
    Compute top numplayers (playerID, stat) sorted descending by stat.
    """
    pid_field = info['playerid']
    scored = []
    for stat in statistics:
        score = formula(info, stat)
        scored.append((stat[pid_field], score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:numplayers]


def lookup_player_names(info, top_ids_and_stats):
    """
    Convert (playerID, stat) to formatted 'x.xxx --- First Last' strings.
    """
    master = read_csv_as_nested_dict(
        info['masterfile'], info['playerid'], info['separator'], info['quote']
    )
    result = []
    for pid, stat in top_ids_and_stats:
        name_first = master[pid][info['firstname']]
        name_last = master[pid][info['lastname']]
        text = f"{stat:.3f} --- {name_first} {name_last}"
        result.append(text)
    return result


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Returns formatted top stats for a given year.
    """
    stats = read_csv_as_list_dict(
        info['battingfile'], info['separator'], info['quote']
    )
    yearly = filter_by_year(stats, year, info['yearid'])
    top_ids = top_player_ids(info, yearly, formula, numplayers)
    return lookup_player_names(info, top_ids)


def aggregate_by_player_id(statistics, playerid, fields):
    """
    Aggregate specified numeric fields by player, include playerid key.
    """
    res = {}
    for stat in statistics:
        pid = stat[playerid]
        if pid not in res:
            res[pid] = {playerid: pid}
            for field in fields:
                res[pid][field] = 0
        for field in fields:
            res[pid][field] += int(stat[field])
    return res


def compute_top_stats_career(info, formula, numplayers):
    """
    Returns formatted top career stats aggregated across all years.
    """
    stats = read_csv_as_list_dict(
        info['battingfile'], info['separator'], info['quote']
    )
    pid = info['playerid']
    fields = info['battingfields']
    agg = aggregate_by_player_id(stats, pid, fields)
    agg_list = list(agg.values())
    top_ids = top_player_ids(info, agg_list, formula, numplayers)
    return lookup_player_names(info, top_ids)
