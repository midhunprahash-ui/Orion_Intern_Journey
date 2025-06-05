import psycopg2
import pandas as pd
from thefuzz import process, fuzz


db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'emp_details',
    'user': 'postgres',
    'password': '12345'
}

conn = psycopg2.connect(**db_config)

query = "SELECT * FROM employees;"
employee_df = pd.read_sql(query, conn)
conn.close()


employee_df['full_name'] = employee_df['first_name'].str.strip() + " " + employee_df['last_name'].str.strip()

def clean_name(name):
    
    return ''.join(e for e in name.lower() if e.isalnum() or e.isspace())

employee_df['clean_full_name'] = employee_df['full_name'].apply(clean_name)


input_name = input("Enter the user name to search for: ")
cleaned_input = clean_name(input_name)


def find_best_matches(query, df, limit=5, threshold=80):
    matches = process.extract(query, df['clean_full_name'], scorer=fuzz.token_set_ratio, limit=limit)
    
    filtered = []
    for match in matches:
        name, score, idx = match
        if score >= threshold:
            row = df.iloc[idx]
            filtered.append((row['emp_id'], row['full_name'], score))
    return filtered

matches = find_best_matches(cleaned_input, employee_df)


if matches:
    print("\nTop matching employees:")
    for emp_id, full_name, score in matches:
        print(f"ID: {emp_id} | Name: {full_name} | Match Score: {score}")
else:
    print("No close matches found.")

