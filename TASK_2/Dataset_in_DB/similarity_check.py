import pandas as pd
from thefuzz import fuzz
import jellyfish
import joblib
import psycopg2

# Loading the trained model

model = joblib.load('name_matching_model(DB).pkl')


def compute_features(username, employee_name):
    return [
        fuzz.ratio(username, employee_name),
        fuzz.partial_ratio(username, employee_name),
        fuzz.token_set_ratio(username, employee_name),
        int(jellyfish.soundex(username) == jellyfish.soundex(employee_name)),
        int(jellyfish.metaphone(username) == jellyfish.metaphone(employee_name))
    ]

def fetch_employees():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="emp_test",
            user="postgres",
            password="12345"
        )
       
        df = pd.read_sql("SELECT EMP_ID,First_name,Last_name FROM employee_1;", conn)
        conn.close()
        if df.empty:
            print("No employees found in the database.")
            return pd.DataFrame(columns=['emp_id', 'employee_name'])
        df['employee_name'] = df['first_name'].str.strip() + ' ' + df['last_name'].str.strip()
        return df[['emp_id', 'employee_name']]
    except Exception as e:
        print("Error fetching employees:", e)
        return pd.DataFrame(columns=['emp_id', 'employee_name'])

def match_username(input_username, threshold=0.7):
    employees = fetch_employees()
    if employees.empty:
        print("No employee data available for matching.")
        return

    features = employees['employee_name'].apply(lambda en: compute_features(input_username, en))
    features_df = pd.DataFrame(list(features), columns=[
        'levenshtein', 'partial_ratio', 'token_set_ratio', 'soundex_match', 'metaphone_match'
    ])
    probs = model.predict_proba(features_df)[:, 1]
    employees['probability'] = probs

    matches = employees[employees['probability'] >= threshold]
    if matches.empty:
        print("No likely matches found.")

        top_matches = employees.sort_values('probability', ascending=False).head(5)
        print("\nTop 5 closest matches (for reference):")
        for _, row in top_matches.iterrows():
            print(f"emp_id: {row['emp_id']}, emp_name: {row['employee_name']}, probability: {row['probability']:.2f}")
    else:
        print("\nPossible matches:")
        for _, row in matches.sort_values('probability', ascending=False).iterrows():
            print(f"This username matches with emp_id: {row['emp_id']}, emp_name: {row['employee_name']} (probability: {row['probability']:.2f})")

if __name__ == "__main__":
    input_username = input("Enter the username to match: ").strip()
    match_username(input_username, threshold=0.8)  