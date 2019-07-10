# Next Pitch Prediction Model
## Goal 
#### A web application that utilizes machine learning to make 'pitch-type' predictions based on current MLB game situations

## Business Understanding
As a former collegiate baseball players, I understand that mastering your mental approach is the hardest part about being an elite hitter. Major League Baseball organizations pay pitchers millions of dollars to confuse opposing hitters and as a player, I always struggled with understanding how pitchers would attack my weaknesses at the plate. NextPitch will help hitters train for in-game scenarios with a data driven advantage, giving them more confidence in their approach at the plate.


## Data Understanding
The data is collected from play-by-play data from all games played in the 2018 season. The python wrapper StatsApi was used to collect both gameids, and play-by-play data. The data comes directly from Major League Baseball and includes information like 'pitch_types', 'pitch_number', 'pitcher_id', 'men_on_base' and other relevant game data. During the collection of data, a dictionary was created with hand-selected columns that were viewed as potentially useful. Player data from espn.com was collected along with the play-by-play data to create a merged data frame with both hitter/pitcher and game data.

## Data Preparation
MLB Game data is plentiful and fairly easy to access using StatsApi. The data comes in as .json and needs to be reorganized into a dataframe. After the data frame is constructed, there are several features that need to be dropped or engineered.
- Add Previous Pitch Column
- Add Hitter/Pitcher Stats
- Engineer count column
- Drop Various Redundant Columns(Pitcher/Hitter id Code, Play Results)
- Select Data User's Can Input(Prior Pitch Type, Count, Pitcher Name, Hitter Name)
Final Features before Modeling(Pitchers, Hitters, Half_Inning, Inning, Batter Side, Pitcher Side, BaseRunners, Pitch Count, Previous Pitch)


## Modeling
Model: Gradient Boosted Trees Classifier
- Parameters: N_estimators = 200
- Max_depth = 10
Performance: 
- Accuracy Score: ~70% 
- F1- Score: ~69% 
- AUC Score: ~68%

## Evaluation:
MLB pitchers rely on both scouting reports and "gut" feelings to make decisions on what pitch to throw. This makes their actions less predictable. The overall naive accuracy of predicting fastball or off_speed is 55%. Differences between elite and average hitters is minimal. For example, let's look at J.D. Martinez and Amed Rosario. J.D. was one of the most recognized hitters in the game, he finished 2nd in average and was an important piece to the Boston Red Sox 2018 World Series Championship. Amed Rosario on the other hand is a quality player, but 79th best hitter in baseball and nobody cares. The difference between these two hitters was 41 hits. The MLB season is 26.5 weeks long. The difference between being considered one of the best hitters in baseball and being average is 1.5 hits per week. 1.5 hits per week can be the difference between signing a massive free agent contract, or having to retire. Having a ~70% of anticipating the next pitch could be a career changer for some hitters. This model just needs to provide 1 hit a week to become useful.

## Deployment
The Web Application can be accessed here. The user will be able to input game data and receive a prediction.

## Future Improvements
- Look into a BiDirectional NN to help predict pitch sequencing.
- Restructure and add more features including weather, previous pitch sequences, previous successes and failures..etc
- Create Pseudo Live Feed to test real-live-world application and accuracy. 
 



