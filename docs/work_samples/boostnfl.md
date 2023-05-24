# A Simple Machine Learning algorithm to predict the outcome of NFL games - Implemented using Python

[Source](https://github.com/AviouslyK/BoostNFL)

## An Introduction: Responsible Sports Gambling

During the fall of 2022, I found myself more excited for the upcoming NFL season then usual. A sports betting app was running
a promotion: deposit $25, get $200 additionally to bet with. Being an avid NFL football fan, I thought a fun project might be 
to design a machine learning algorithm to predict the outcome of games each week. Then I can feel secure that my bets aren't based
on my own biases, but just the data. 

There was no expectation to beat Vegas of course, but getting $200 free from the onset means I should be able to at least break even ... right?

Let's find out.

# Building the model

## Obtaining and Cleaning the data
The first thing needed is a public dataset of all NFL games, with the teams, outcomes, and any other useful features. Thankfully, I found one online at http://www.habitatring.com/games.csv, which has data from 1999 to the present, and is updated regularly.

To begin, we can use **pandas** to read in all the data from the website and put it into a DataFrame. We make two copies of the data, one will end up as our training data, and the other will be our testing/validation data. 

```python
import pandas as pd

# Read in public NFL dataset

# For Training and Validation
X_full = pd.read_csv("http://www.habitatring.com/games.csv") 
# For Testing
X_test_full = pd.read_csv("http://www.habitatring.com/games.csv") 
```

Now we separate out our Training and Validation Data, from our testing data. To start with, let's train and validate on all NFL games played before the 2019 season, Then we can test our performance on games played during and after 2019. 

To keep thing simple, let's also only consider regular season games - any NFL fan knows that _anything_ can happen in the playoffs, and we don't want to confuse are model!


```python 
# Remove rows with missing target
X_full = X_full.dropna( how='any', subset=['away_score','home_score','total','result'])

# Separate out Training/Validation data
X_full = X_full[X_full['game_type'] == "REG"] 
X_full = X_full[X_full['season'] < 2019]

# Separate out Testing Data
X_test_full = X_test_full[(X_test_full['season'] >= 2019) & (X_test_full['game_type'] == "REG")]

```

Now we want to separate the target from our predictors. In this case, our _target_, i.e. what w'ere trying to predict, will be the `result` column of the data, where `result = home_score - away_score`. 

```python
# separate target from predictors
y_test = X_test_full.result 
y = X_full.result 
X_full.drop(['result'], axis=1, inplace=True) # this is target
X_full.drop(['away_score'], axis=1, inplace=True) # these are directly related to target
X_full.drop(['home_score'], axis=1, inplace=True)
X_full.drop(['total'], axis=1, inplace=True) 
```

The next step is to separate out our Validation set from our Training set. When training a machine learning model, you need to calculate some measure of it's accuracy, before you go an apply it to real data. And of course, you can't use the same data you trained it on to evaluate it. There is a lot that could be said about the ideal ratio of training vs validation data, but in this case I will simply take 70% of the data pulled from before 2019, and use it for training. The other 30% will be used for validation.

We can use the **sklearn** package to easily execute this.

```python 
from sklearn.model_selection import train_test_split

# Break off validation set from training data
X_train_full, X_valid_full, y_train, y_valid = train_test_split(X_full, y, train_size=0.7, test_size=0.3, random_state=0)
```

Finally, the last step of data cleaning we need to do, is to convert any categorical data into numerical. Here I chose to one-hot encode the data. As an example this would convert 

| Color | Val |
|-------|-----|
| red   | 14  |
| blue  | 22  |
| white | 18  | 

into

| red | blue | white | val |
|-----|------|-------|-----|
| 1   | 0    | 0     | 14  |
| 0   | 1    | 0     | 22  |
| 0   |   0  | 1     | 18  |

Now we apply this quite simply:

```python
# Select numerical columns
numerical_cols = [cname for cname in X_train_full.columns if 
                X_train_full[cname].dtype in ['int64', 'float64']]

# Select categorical columns
categorical_cols = [cname for cname in X_train_full.columns if
                    X_train_full[cname].nunique() < 1000 and 
                    X_train_full[cname].dtype == "object" or X_train_full[cname].dtype == "string"]

# Keep selected columns only
my_cols = categorical_cols + numerical_cols
X_train = X_train_full[my_cols].copy()
X_valid = X_valid_full[my_cols].copy()
X_test = X_test_full[my_cols].copy()

# Save copies of the data before one-hot encoding, for showing results later on
X_train_OG = X_train
X_valid_OG = X_valid
X_test_OG = X_test

# One-hot encode the data (to shorten the code, we use pandas)
X_train = pd.get_dummies(X_train)
X_valid = pd.get_dummies(X_valid)
X_test = pd.get_dummies(X_test)
X_train, X_valid = X_train.align(X_valid, join='left', axis=1)
X_train, X_test = X_train.align(X_test, join='left', axis=1)
```

Now we can print out the data, and see what we have so far

```python
X_train.name = 'Training Set'
X_test.name = 'Test Set'

print('Number of Training Examples = {}'.format(X_train.shape[0]))
print('Number of Validation Examples = {}'.format(X_valid.shape[0]))
print('Number of Test Examples = {}\n'.format(X_test.shape[0]))

print(my_cols)
print("\n")
```

```plaintext
$ python boost_nfl.py

Number of Training Examples = 3567
Number of Validation Examples = 1529
Number of Test Examples = 1327

['game_type', 'gameday', 'weekday', 'gametime', 'away_team', 'home_team', 'location', 'nfl_detail_id', 'roof', 'surface', 'away_qb_id', 'home_qb_id', 'away_qb_name', 'home_qb_name', 'away_coach', 'home_coach', 'referee', 'stadium_id', 'stadium', 'season', 'week', 'overtime', 'old_game_id', 'gsis', 'pff', 'espn', 'away_rest', 'home_rest', 'away_moneyline', 'home_moneyline', 'spread_line', 'away_spread_odds', 'home_spread_odds', 'total_line', 'under_odds', 'over_odds', 'div_game', 'temp']
```