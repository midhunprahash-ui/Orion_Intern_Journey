import pandas as pd
import re
import psycopg2 
from psycopg2 import OperationalError 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def connect_to_postgresql(dbname, user, password, host='localhost', port='5432'):
 
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Successfully connected to database!")
        return conn
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_employee_data_from_db(conn):
  
    if conn is None:
        return pd.DataFrame() 

    query = "SELECT emp_id, first_name, last_name FROM employees;"
    try:
        df = pd.read_sql(query, conn)
        df.columns = ['Emp_ID', 'First_name', 'Last_name']
        print("Employee data fetched from database:")
        print(df.head()) 
        return df
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return pd.DataFrame()

def prepare_all_searchable_names(employee_df):
    
    searchable_names = []
    name_to_employee_map = []

    for index, row in employee_df.iterrows():
        emp_id = row['Emp_ID']
        first_name = str(row['First_name']).lower()
        last_name = str(row['Last_name']).lower()

        variations = [
            f"{first_name} {last_name}", 
            first_name,                 
            last_name,                
            f"{first_name[0]}{last_name}" if first_name else "", 
            f"{last_name}{first_name[0]}" if first_name else "", 
            f"{last_name} {first_name}", 
        ]
        variations = [v for v in variations if v]

        for var in variations:
            searchable_names.append(var)
            name_to_employee_map.append({'Emp_ID': emp_id, 'Name_Variation': var})

    return searchable_names, pd.DataFrame(name_to_employee_map)

def check_username_match(username, employee_df, vectorizer, employee_name_vectors, employee_name_map_df, name_similarity_threshold=0.3):
   
    username_lower = username.lower()
    best_match_info = None
    max_similarity = -1.0 

    if any(char.isdigit() for char in username):
        for index, row in employee_df.iterrows():
            if username_lower == str(row['Emp_ID']).lower():
                return {
                    "Emp_ID": row['Emp_ID'],
                    "First_name": row['First_name'],
                    "Last_name": row['Last_name'],
                    "Match_Type": "Exact Emp_ID Match",
                    
                }

    username_variations_for_names = [username_lower]
    cleaned_username_alpha = ''.join(char for char in username_lower if char.isalpha())
    if cleaned_username_alpha:
        username_variations_for_names.append(cleaned_username_alpha)
    username_tokens = username_lower.replace('_', ' ').replace('.', ' ').strip().split()
    username_variations_for_names.extend(username_tokens)
    if len(username_tokens) >= 2:
        username_variations_for_names.append(f"{username_tokens[0]}{username_tokens[1]}")
        username_variations_for_names.append(f"{username_tokens[1]}{username_tokens[0]}")

    if not username_variations_for_names:
        return None

    username_vecs = vectorizer.transform(username_variations_for_names)
    if username_vecs.shape[0] == 0:
        return None

    similarities = cosine_similarity(username_vecs, employee_name_vectors)

    for i, user_sims in enumerate(similarities):
        for j, sim_score in enumerate(user_sims):
            if sim_score > max_similarity:
                max_similarity = sim_score
                matched_name_info = employee_name_map_df.iloc[j]
                best_match_info = {
                    "Emp_ID": matched_name_info['Emp_ID'],
                    "Matched_Name_Variation": matched_name_info['Name_Variation'],
                    
                }

    if best_match_info and best_match_info['Similarity_Score'] / 100.0 >= name_similarity_threshold:
        matched_emp_row = employee_df[employee_df['Emp_ID'] == best_match_info['Emp_ID']].iloc[0]

        if username_lower == str(matched_emp_row['First_name']).lower():
             return {
                "Emp_ID": matched_emp_row['Emp_ID'],
                "First_name": matched_emp_row['First_name'],
                "Last_name": matched_emp_row['Last_name'],
                "Match_Type": "Exact First Name Match",
                
            }
        elif username_lower == str(matched_emp_row['Last_name']).lower():
            return {
                "Emp_ID": matched_emp_row['Emp_ID'],
                "First_name": matched_emp_row['First_name'],
                "Last_name": matched_emp_row['Last_name'],
                "Match_Type": "Exact Last Name Match",
                
            }
        else:
            return {
                "Emp_ID": matched_emp_row['Emp_ID'],
                "First_name": matched_emp_row['First_name'],
                "Last_name": matched_emp_row['Last_name'],
                "Match_Type": "Cosine Similarity Name Match",
                "Matched_Name_Variation": best_match_info['Matched_Name_Variation'],
                
            }
    else:
        return None

if __name__ == "__main__":
    DB_CONFIG = {
        'dbname': 'emp_details',  
        'user': 'postgres',         
        'password': '12345',     
        'host': 'localhost',             
        'port': '5432'                   
    }

    conn = connect_to_postgresql(**DB_CONFIG)

    if conn:
        employee_db = fetch_employee_data_from_db(conn)
        conn.close() 

        if not employee_db.empty:
            print("\n" + "="*50 + "\n")

            all_searchable_names, employee_name_map_df = prepare_all_searchable_names(employee_db)

            vectorizer = TfidfVectorizer(lowercase=True, stop_words=None, analyzer='word', token_pattern=r'\b\w+\b')
            vectorizer.fit(all_searchable_names)

            employee_name_vectors = vectorizer.transform(all_searchable_names)

            usernames_to_check = [
                "john", "doe", "john_doe123", "jsmith_hr", "robertj",
                "sarahm", "E001", "e005", "E123", "emp_id_e002",
                "chrisb", "unknownuser", "jessica", "jones", "garcia",
                "rodriguez", "ananya", "sharma", "m_khan", "jdoe",
                "smithjane", "john123", "doejane", "E007", "Michael", "Williams"
            ]

            print("\n--- Checking Usernames based on Specific Rules ---")
            for username in usernames_to_check:
                print(f"\nProcessing username: '{username}'")
                found_employee = check_username_match(
                    username, employee_db, vectorizer, employee_name_vectors, employee_name_map_df,
                    name_similarity_threshold=0.35 
                )

                if found_employee:
                    print(f"  --> Match Found!")
                    print(f"      Emp_ID: {found_employee['Emp_ID']}")
                    print(f"      Name: {found_employee['First_name']} {found_employee['Last_name']}")
                    print(f"      Match Type: {found_employee['Match_Type']}")
                    if 'Matched_Name_Variation' in found_employee:
                        print(f"      Matched Name Variation: '{found_employee['Matched_Name_Variation']}'")
                    print(f"      Score: {found_employee['Score']}{'%' if found_employee['Match_Type'] == 'Cosine Similarity Name Match' else ''}")
                else:
                    print(f"  --> No match found for '{username}' based on the defined rules.")
                print("-" * 60)
        else:
            print("No employee data loaded. Cannot proceed with matching.")
    else:
        print("Failed to connect to the database. Please check your configuration.")