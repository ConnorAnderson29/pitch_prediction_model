# Libraries
import pandas as pd # Dataframes
from pandas.io.json import json_normalize # JSON wrangler
import statsapi # Python wrapper MLB data API
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(0)
import os
import seaborn as sns


#DATA MANIPULATION AND MODELLING
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import f1_score, accuracy_score, roc_auc_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn_pandas import DataFrameMapper, FunctionTransformer, gen_features, pipeline
from sklearn_pandas.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelBinarizer
import xgboost as xgb

# Neural Networks
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.utils import to_categorical
from keras.layers import Bidirectional, Activation









def calc_roc_acc_score(y_test, y_pred, average='macro'):
    """Calculate binary/multiclass AUC
       Returns: AUC
    """
    lb = LabelBinarizer()
    lb.fit(y_test)
    y_test = lb.transform(y_test)
    y_pred = lb.transform(y_pred)
    return roc_auc_score(y_test, y_pred, average=average)
   

    
def calc_acc_and_f1_score(true, preds, model_name='Model Name'):
    """Calculate and print classification metrics
    """
    acc = accuracy_score(true, preds)
    f1 = f1_score(true, preds, average='weighted')
    multi_auc = calc_roc_acc_score(true, preds)
    #print('Model:{}'.format(model_name))
    print('Accuracy:{:.3f}'.format(acc))
    print('F1-Score: {:.3f}'.format(f1))
    print('AUC: {:.3f}'.format(multi_auc))


def run_classifier_models(classifiers, preprocessor, X_train, X_test, y_train, y_test):
    for classifier in classifiers:
        ''' Intialize Pipeline, Fit Pipeline to Train Set''' 
        """URL MUST BE STRING"""
        clf1 = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', classifier)])
        clf1.fit(X_train, y_train)

        ''' Calculate and display performance metrics''' 
        print(classifier)
        print('\n')
        print('Training Metrics')
        pitch_functions.calc_acc_and_f1_score(y_train, clf1.predict(X_train))
        print('\n')
        print('Testing Metrics')
        pitch_functions.calc_acc_and_f1_score(y_test, clf1.predict(X_test))
        print('\n')

def scrape_espn_player_data(url, final_df):

    '''This functions scrapes ESPN leaderboard data and returns a Pandas Data Frame'''

    for i in range(1,1000, 40):
        url =url.format(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
        for player in players:
            # Get Stat for each player
            stats = [stat.get_text() for stat in player.find_all('td')]
            # Create temp dataframe to add later
            temp_df = pd.DataFrame(stats).transpose()
            temp_df.columns = columns
            # Add Data to final_df
            final_df = pd.concat([final_df, temp_df], ignore_index=True)
    return final_df


def final_model(predictors, target, new_pitch):
    
    target = pitch_clean['pitch_type']
    predictors = pitch_clean.drop(['pitch_type', 'hitter', 'pitcher' ], axis=1)
    
    X_train, X_test, y_train, y_test = train_test_split(predictors, target, random_state=10)
    
    num_features = list(predictors.select_dtypes(exclude='object'))
    num_features = [i for i in num_features if i not in {'about.inning', 'pitchData.zone', 'matchup.pitcher.id'}]
    numeric_transformer = Pipeline(steps=[('keeper', None)])
    cat_transfomer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', categories='auto'))])
    
    preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, num_features),
                                              ('cat', cat_transfomer, cat_features)])
    pipe = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', classifiers_test)])
    pipe.fit(X_train, y_train)
    print(pitch_functions.calc_acc_and_f1_score(y_test, pipe.predict(X_test)))
    prediction = pipe.predict(new_pitch)
    
    
    if prediction == 1:
        print ('Fastball')
    else: 
        print ('Off_Speed')
    