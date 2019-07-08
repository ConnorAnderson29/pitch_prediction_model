import pandas as pd
from sklearn.pipeline import Pipeline
import pickle
import pitch_functions
from flask import Flask, request, render_template, jsonify
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_url_path="")

with open('final_test.pkl', 'rb') as f:
     model = pickle.load(f)

@app.route("/")
def index():
    """Return the main page."""
    return render_template("new_index.html")


@app.route("/output", methods=["GET", "POST"])
def output():
    """Retun text from user input"""
    #Python object to store user data
    data = request.get_json(force=True)
    # every time the user_input identifier
    out = {"pitcher": data["pitcher"].value,
                            'hitter': data["hitter"].value,
                            'top/bottom': data["top/bottom"].value,
                            'inning': data["inning"].value,
                            'hitter_side': data["hitter_side"].value,
                            'pitcher_side': data["pitcher_side"].value,
                            'runners_on': data["runners_on"].value,
                            'nasty': data["nasty"].value,
                            'zone': data["zone"].value,
                            'pitch_num': data["pitch_num"].value,
                            'pitch_type': data["pitch_type"].value,
                            'prior_pitch_type': data["prior_pitch_type"].value,
                            'count': data["count"].value}
    
    
    
    # output dictionary to web
    print(data)
    return jsonify(data["user_input"])

