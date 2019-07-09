import pandas as pd
from sklearn.pipeline import Pipeline
import pickle


from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_url_path="")

with open('final_test.pkl', 'rb') as f:
     model = pickle.load(f)

@app.route("/")
def index():
    """Return the main page."""
    return render_template("new_index.html")

def merge_player_stats(dataframe):
    '''Sources data from CSVs located in the main directory. 
    Then it merges the data on the name of the player and returns their stats merged with pitches.'''
    hitter_df = pd.read_csv('../../public_data/hitter_data.csv')
    pitcher_df = pd.read_csv('../../public_data/pitcher_data.csv')
    
    hitter_df = hitter_df[['PLAYER', 'SLG', 'OPS', 'WAR']]
    hitter_df = hitter_df.rename(columns={'PLAYER': 'hitter'})
    
    pitcher_df = pitcher_df[['PLAYER', 'WAR', 'WHIP', 'ERA', 'SO']]
    pitcher_df = pitcher_df.rename(columns={'PLAYER': 'pitcher'})
    
    dataframe = dataframe.rename(columns={'matchup.batter.fullName': 'hitter',
                                      'matchup.pitcher.fullName': 'pitcher'})
    
    merged = pd.merge(hitter_df, dataframe, on='hitter')
    full_merge = pd.merge(pitcher_df, merged, on='pitcher')
    
    return full_merge

def format_user_input(user_dict):
    live_df = pd.DataFrame.from_dict(user_dict)
    created_test = merge_player_stats(live_df)
    created_test['pitchData.nastyFactor'] = 35.326
    created_test['pitchData.zone'] = 9.8751
    return created_test


@app.route("/output", methods=["GET", "POST"])
def output():
    """Retun text from user input"""
    #Python object to store user data
    data = list(request.get_json(force=True))
    dictionary_of_data = format_user_input(data)
    preds = model.predict_probab(dictionary_of_data)
    off_speed_pred = preds[0][0]
    fastball_pred = preds[0][1]
    # every time the user_input identifier
#     out = {"pitcher": data["pitcher"].value,
#                             'hitter': data['hitter'].value,
#                             'top/bottom': data["top/bottom"].value,
#                             'inning': data["inning"].value,
#                             'hitter_side': data["hitter_side"].value,
#                             'pitcher_side': data["pitcher_side"].value,
#                             'runners_on': data["runners_on"].value,
#                             'nasty': data["nasty"].value,
#                             'zone': data["zone"].value,
#                             'pitch_num': data["pitch_num"].value,
#                             'pitch_type': data["pitch_type"].value,
#                             'prior_pitch_type': data["prior_pitch_type"].value,
#                             'count': data["count"].value}
    final_dict = {'Probability of Off Speed' : off_speed_pred, 
                 'Probability of Fastball': fastball_pred}
    
    
    # output dictionary to web
    print(data)
    return jsonify(final_dict)

