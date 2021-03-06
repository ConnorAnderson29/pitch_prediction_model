# Libraries
import pandas as pd  # Dataframes
from pandas.io.json import json_normalize  # JSON wrangler
import statsapi  # Python wrapper MLB data API
import numpy as np

pd.set_option("display.max_columns", None)


# Data Collection Function


def collect_game_data(start_date, end_date):
    """Calls StatsApi to collect game IDs for games played during defined period"""
    schedule = statsapi.schedule(start_date=start_date, end_date=end_date)
    full = json_normalize(schedule)
    gamepks = full["game_id"]

    """Iterates through play-by-play data, normalizes nested .json, 
        and adds data back to columns defined below."""
    list_for_final_df = []
    for game in gamepks:
        curr_game = statsapi.get("game_playByPlay", {"gamePk": game})
        curr_plays = curr_game.get("allPlays")
        curr_plays_df = pd.DataFrame(curr_plays)
        curr_plays_norm = json_normalize(curr_plays)

        all_plays_cols = [
            "about.atBatIndex",
            "about.halfInning",
            "about.inning",
            "count.balls",
            "count.strikes",
            "matchup.batSide.code",
            "matchup.batter.fullName",
            "matchup.batter.id",
            "matchup.pitchHand.code",
            "matchup.splits.menOnBase",
            "matchup.pitcher.fullName",
            "matchup.pitcher.id",
            "result.eventType",
        ]

        play_events_cols = [
            "count.balls",
            "count.strikes",
            "details.ballColor",
            "details.call.code",
            "details.call.description",
            "details.type.description",
            "details.call.code",
            "details.description",
            "details.code",
            "details.type.code",
            "index",
            "pitchData.nastyFactor",
            "pitchData.zone",
            "pitchNumber",
            "type",
        ]
        i = 1
        for index, row in curr_plays_norm.iterrows():
            play_events = json_normalize(row["playEvents"])
            """Determines whether columns are in list defined above and adds data accordingly.
                    Returns a data frame containing play-by-play game data"""

            for play_events_idx, play_events_row in play_events.iterrows():

                game_dict = {}
                game_dict["gamepk"] = game
                game_dict["pitch_id"] = (
                    str(game) + "_" + str(row["about.atBatIndex"]) + "_" + str(i)
                )
                game_dict["prior_pitch"] = (
                    str(game) + "_" + (str(row["about.atBatIndex"]) + "_" + str(i - 1))
                )

                for col_all_plays in all_plays_cols:
                    if col_all_plays in curr_plays_norm.columns:
                        game_dict[col_all_plays] = row[col_all_plays]
                    else:
                        game_dict[col_all_plays] = np.nan
                for col_play_events in play_events_cols:
                    if col_play_events in play_events.columns:
                        game_dict[col_play_events] = play_events_row[col_play_events]
                    else:
                        game_dict[col_play_events] = np.nan

                list_for_final_df.append(game_dict)
                i += 1
    return pd.DataFrame(list_for_final_df)


# DATA CLEANING


def define_prior_pitch(dataframe):
    """Creates a data frame that has a previous pitch column."""
    each_pitch = dataframe
    pitch_id_df = each_pitch[["pitch_id", "details.type.code"]].copy()
    merged_df = pd.merge(
        each_pitch, pitch_id_df, how="left", left_on="prior_pitch", right_on="pitch_id"
    )
    each_pitch_merged = merged_df
    each_pitch_merged = each_pitch_merged.rename(
        {
            "pitch_id_y": "previous_pitch_in_ab",
            "details.type.code_y": "previous_pitch_code",
        },
        axis=1,
    )

    each_pitch_clean = each_pitch_merged.drop(
        [
            "result.eventType",
            "type",
            "pitch_id_x",
            "previous_pitch_in_ab",
            "prior_pitch",
            "details.ballColor",
        ],
        axis=1,
    )
    return each_pitch_clean


def map_pitches(dataframe):
    """Files down pitches from 10 options to 3 options. 
        Fundamental part of the data cleaning"""
    each_pitch_clean = dataframe
    pitch_dict = {"FF": "Fastball"}
    pitch_dict["FT"] = "Fastball"
    pitch_dict["FC"] = "Fastball"
    pitch_dict["FS"] = "Fastball"
    pitch_dict["CH"] = "Changeup"
    pitch_dict["SI"] = "Fastball"
    pitch_dict["FT"] = "Fastball"
    pitch_dict["CU"] = "Breaking_Ball"
    pitch_dict["SL"] = "Breaking_Ball"
    pitch_dict["KC"] = "Breaking_Ball"
    pitch_dict["nan"] = "NA"

    each_pitch_clean["pitch_type"] = each_pitch_clean["details.type.code_x"].map(
        pitch_dict
    )
    each_pitch_clean["prior_pitch_type"] = each_pitch_clean["previous_pitch_code"].map(
        pitch_dict
    )

    each_pitch_clean = each_pitch_clean.drop(
        [
            "details.type.code_x",
            "details.type.description",
            "details.code",
            "gamepk",
            "index",
            "matchup.batter.id",
        ],
        axis=1,
    )
    return each_pitch_clean


def merge_player_stats(dataframe):
    """Takes player stats from Public Data and merges them by player
        name and creates a new merged data frame with player stats attached."""

    hitter_df = pd.read_csv("public_data/hitter_data.csv")
    pitcher_df = pd.read_csv("public_data/pitcher_data.csv")

    hitter_df = hitter_df[["PLAYER", "SLG", "OPS", "WAR"]]
    hitter_df = hitter_df.rename(columns={"PLAYER": "hitter"})

    pitcher_df = pitcher_df[["PLAYER", "WAR", "WHIP", "ERA", "SO"]]
    pitcher_df = pitcher_df.rename(columns={"PLAYER": "pitcher"})

    dataframe = dataframe.rename(
        columns={
            "matchup.batter.fullName": "hitter",
            "matchup.pitcher.fullName": "pitcher",
        }
    )

    merged = pd.merge(hitter_df, dataframe, on="hitter")
    full_merge = pd.merge(pitcher_df, merged, on="pitcher")

    return full_merge


def add_atbat_counts(dataframe):
    """Changes count columns into strings and then merges a 
        final COUNT column as a string. 
        The string will be usedfor OneHotEncoding."""
    add_feats = dataframe
    add_feats["count.balls"] = add_feats["count.balls"].astype(str)
    add_feats["count.strikes"] = add_feats["count.strikes"].astype(str)
    add_feats["count"] = add_feats["count.balls"] + "-" + add_feats["count.strikes"]
    add_feats = add_feats.drop(
        ["previous_pitch_code", "details.call.code", "count.balls", "count.strikes"],
        axis=1,
    )
    final_pitches = add_feats

    return final_pitches


def binarize_target(dataframe):
    '''Takes in a data frame, and maps pitch_dict over the data frame columns "previous_pitch_type
    and pitch_type. Makes it easier for model to predict correctly."'''
    pitch_clean = dataframe
    pitch_dicts = {"Fastball": 1, "0": 1, "Breaking_Ball": 0, "Changeup": 0}
    pitch_clean["pitch_type"] = pitch_clean["pitch_type"].map(pitch_dicts)
    pitch_clean["prior_pitch_type"] = pitch_clean["prior_pitch_type"].map(pitch_dicts)
    pitch_cleaned = pitch_clean.dropna()
    return pitch_cleaned


def get_clean_data(start_date, end_date):
    """Collects and cleans data using start and end dates
        then acts as a wrapper function for the other 
        data cleaning functions. Outputs a cleaned data frame"""
    raw_data = collect_game_data(start_date, end_date)

    prior_pitch_add = define_prior_pitch(raw_data)

    mapped_pitches = map_pitches(prior_pitch_add)

    merged_pitches = merge_player_stats(mapped_pitches)

    added_counts = add_atbat_counts(merged_pitches)

    final = added_counts

    return final.copy()


def format_user_input(user_dict):
    '''Uses user input dictionary recieved from Flask App
        and creates a data frame row that can be used
        inside of "model.predict"'''
    live_df = lib.pd.DataFrame([user_dict])
    created_test = data_collection.merge_player_stats(live_df)
    created_test = created_test[test_list]
    return created_test
