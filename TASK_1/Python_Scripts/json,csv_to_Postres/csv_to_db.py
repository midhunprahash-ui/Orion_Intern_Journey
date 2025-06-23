import psycopg2

def convert_csv_to_postgres_bulk_upsert_and_execute(csv_path, table_name, conflict_column='emp_id'):
    import collections

    with open(csv_path, 'r') as csv_file:
        lines = csv_file.readlines()

    headers = lines[0].strip().split(',')

    if conflict_column not in headers:
        raise ValueError(f"Conflict column '{conflict_column}' not found in CSV headers")

    
    emp_dict = collections.OrderedDict()

    for line in lines[1:]:
        values = line.strip().split(',')
        row_dict = dict(zip(headers, values))
        emp_id = row_dict[conflict_column]
        emp_dict[emp_id] = row_dict  

    value_lines = []
    for emp_id, row_dict in emp_dict.items():
        formatted_values = []
        for col in headers:
            val = row_dict[col].strip().replace("'", "''")
            if val.replace('.', '', 1).isdigit():
                formatted_values.append(val)
            else:
                formatted_values.append(f"'{val}'")
        value_lines.append(f"({', '.join(formatted_values)})")

    update_columns = [col for col in headers if col != conflict_column]
    set_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_columns])

    sql = (
        f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES\n"
        f"{',\n'.join(value_lines)}\n"
        f"ON CONFLICT ({conflict_column}) DO UPDATE SET {set_clause};"
    )

    
    try:
        connection = psycopg2.connect(
            database="db1",
            user="postgres",
            password="your_password",
            host="localhost",  
            port="5432"        
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit() 
        print("Upsert operation completed successfully.")
    except Exception as e:
        print(f"Error executing SQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    convert_csv_to_postgres_bulk_upsert_and_execute(
        csv_path='/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_1/Input_Files/employees.csv',
        table_name='employee',
        conflict_column='emp_id'
    )
