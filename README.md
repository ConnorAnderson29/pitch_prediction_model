# Next Pitch Prediction Model

## Business Understanding
Mastering the mental apprroach is one of the hardest parts about being an elite professional hitter. Major League Baseball organizations pay pitchers millions of dollars to confuse opposing hitters. As a college baseball player, I always struggled with understanding how pitchers would attack my weaknesses at the plate. This product will help hitters better understand the patterns pitchers follow and will give them more confidence in their approach at the plate. Hitters aren't the only atheletes that will benefit from this model. Pitchers are notorious for following patterns and becoming predictable. By using this model, they can identify their tendencies and learn how to avoid repeat mistakes. 

## Data Understanding
The data will come from all MLB games played in the 2018 season. This is a large and very diverse dataset(around 2 million pitches). The data will include all information about each individual pitch per game(including: pitch type, base runners, pitcher name, etc..)

## Data Preparation
Data is plentiful and fairly easy to retrieve so if more is needed to avoid overfitting then it will be possible to get. After my data is collected, using domain knowledge I will engineer several features that I believe are important(previous pitches, batter attributes, pitcher attributes...etc). Feature engineering will have a huge effect on the model. My goal is to create as close to a replica of the game situation as I can in the data. 

## Modeling
I’m going to train test split 80/20 and then keep a reserve validation set of 20%. This way I can really test the accuracy of the model. Modeling will either utilize a neural network or classification models.First, I will use the data with XGBoost/Gradient Boosted trees. If those models are not successful, then the next step may be to try and train on a neural network just to see if it can produce some deep features. This may take time so I may use a cloud computing service to do the job quickly. 

## Evaluation
I will report both the accuracy score and cross entropy loss, on training and test data. I want the model to err towards fastballs. 
## Deployment
#### User Story:
My typical user will be an athlete or an avid baseball fan who is curious about how pitching tendencies influence the game. They would use my app by going  to the site, entering game information and receiving a prediction for the pitch that would most likely be thrown in that situation. The game information would include count, base runners, outs, inning, pitcher era, and hitter slugging percentage. Entering the information at first would be a hassle, especially during a fast paced game, which is why the end goal is to add a live MLB game which will constantly predict the next pitch. This way a user could enter a game, the application will call the api and the user will be able to interact with the baseball game in a new and interesting way. 



