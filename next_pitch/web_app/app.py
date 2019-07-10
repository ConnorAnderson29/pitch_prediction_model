import pandas as pd
from sklearn.pipeline import Pipeline
import pickle


from flask import Flask, request, render_template, jsonify
pd.set_option('display.max_columns', None)

app = Flask(__name__, static_url_path="")

with open('final.pkl', 'rb') as f:
     model = pickle.load(f)

@app.route("/")
def index():
    """Return the main page."""
    return render_template("index.html", hitters=hitters, pitchers=pitchers, half_inning=half_inning, innings=innings, 
    hitter_side=hitter_side, pitcher_side=pitcher_side, prev_pitch= prev_pitch, count=count, baserunners=baserunners)

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

test_list = ['pitcher',
            'WAR_x',
            'WHIP',
            'ERA',
            'SO',
            'hitter',
            'SLG',
            'OPS',
            'WAR_y',
            'about.halfInning',
            'about.inning',
            'matchup.batSide.code',
            'matchup.pitchHand.code',
            'matchup.splits.menOnBase',
            'pitchData.nastyFactor',
            'pitchData.zone',
            'pitchNumber',
            'pitch_type',
            'prior_pitch_type',
            'count']

hitters = pd.read_csv('../../public_data/hitter_data.csv')['PLAYER'].tolist()
pitchers = pd.read_csv('../../public_data/pitcher_data.csv')['PLAYER'].tolist()
half_inning = ["top", "bottom"]
innings = [1,2,3,4,5,6,7,8,9]
hitter_side = ['L', 'R']
pitcher_side = ['L', 'R']
prev_pitch = [1.0,0.0]
count = ["0.0-0.0", "0.0-0.1", "0.0-0.2", "1.0-0.0", 
         "1.0-1.0", "1.0-2.0", "2.0-0.0", "2.0-1.0", 
         "2.0-2.0","3.0-0.0", "3.0-1.0", "3.0-2.0"]
baserunners = [('Men_On'), ('Empty'), ('Loaded')]




def format_user_input(user_dict):
    live_df = pd.DataFrame([user_dict])
    created_test = merge_player_stats(live_df)
    created_test = created_test[test_list]
    return created_test


@app.route("/output", methods=["GET", "POST"])
def output():
    """Retun text from user input"""
    #Python object to store user data
    data = request.get_json(force=True)
    float_keys = set(['inning', 'pitchNumber', 'prior_pitch_type'])
    int_keys = set(['about.inning'])

    for key, val in data.items():
        if key in float_keys:
            data[key] = float(val)
    for key,val in data.items():
        if key in int_keys:
            data[key] = int(val)
    # Make Keys 
    data['pitch_type'] = 1.0
    data['pitchData.nastyFactor'] = 35.326
    data['pitchData.zone'] = 9.8751
    print(data)

    formatted_df = format_user_input(data)
    print(formatted_df)
    preds = model.predict_proba(formatted_df)
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
    print(final_dict)
    return jsonify(final_dict)

