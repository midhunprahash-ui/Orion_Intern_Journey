import pandas as pd
from thefuzz import fuzz
import jellyfish
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib


df = pd.read_csv('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_2/Training_data/synthetic_name_match_data.csv')

df[['first_name', 'last_name']] = df['employee_name'].str.split(' ',n=1, expand=True)


def compute_features(row):
    fname = row['first_name']
    lname = row['last_name']
    uname = row['username']
    ename = row['employee_name']
    
    return pd.Series({

        'levenshtein_fullname': fuzz.ratio(uname, ename),
        'partial_ratio_fullname': fuzz.partial_ratio(uname, ename),
        'token_set_ratio_fullname': fuzz.token_set_ratio(uname, ename),

        'levenshtein_fname': fuzz.ratio(uname, fname),
        'partial_ratio_fname': fuzz.partial_ratio(uname, fname),
        'token_set_ratio_fname': fuzz.token_set_ratio(uname, fname),

        'levenshtein_lname': fuzz.ratio(uname, lname),
        'partial_ratio_lname': fuzz.partial_ratio(uname, lname),
        'token_set_ratio_lname': fuzz.token_set_ratio(uname, lname),

        'soundex_match_fullname': int(jellyfish.soundex(uname) == jellyfish.soundex(ename)),
        'metaphone_match_fullname': int(jellyfish.metaphone(uname) == jellyfish.metaphone(ename)),

        'soundex_match_fname': int(jellyfish.soundex(uname) == jellyfish.soundex(fname)),
        'metaphone_match_fname': int(jellyfish.metaphone(uname) == jellyfish.metaphone(fname)),

        'soundex_match_lname': int(jellyfish.soundex(uname) == jellyfish.soundex(lname)),
        'metaphone_match_lname': int(jellyfish.metaphone(uname) == jellyfish.metaphone(lname))
    })

features = df.apply(compute_features, axis=1)
df = pd.concat([df, features], axis=1)

feature_cols = [
    'levenshtein_fullname', 'partial_ratio_fullname', 'token_set_ratio_fullname',
    'levenshtein_fname', 'partial_ratio_fname', 'token_set_ratio_fname',
    'levenshtein_lname', 'partial_ratio_lname', 'token_set_ratio_lname',
    'soundex_match_fullname', 'metaphone_match_fullname',
    'soundex_match_fname', 'metaphone_match_fname',
    'soundex_match_lname', 'metaphone_match_lname'
]

X = df[feature_cols]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=32)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(rf, 'new_model.pkl')
