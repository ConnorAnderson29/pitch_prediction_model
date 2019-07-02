from sklearn.metrics import f1_score, accuracy_score, roc_auc_score
from sklearn.preprocessing import LabelBinarizer
















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


def run_classifier_models(classifiers, X_train, X_test, y_train, y_test):
    for classifier in classifiers:
        ''' Intialize Pipeline, Fit Pipeline to Train Set''' 
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
        url ='http://www.espn.com/mlb/stats/batting/_/year/2018/count/{}/qualified/false'.format(i)
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