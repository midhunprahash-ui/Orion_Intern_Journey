import psycopg2

def format_value(value):

    if value is None:
        return ''
    value = str(value)
    if ',' in value or '"' in value:
        return f'"{value.replace("`", "``")}"'
    return value

def db_to_csv(output_file):

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="my_db",
        user="postgres",
        password="your_password_here"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    with open(output_file, 'w') as f:
        f.write(','.join(column_names) + '\n')
        
        for row in rows:
            csv_row = ','.join(format_value(value) for value in row)
            f.write(csv_row + '\n')

    
    cursor.close()
    conn.close()


if __name__ == "__main__":
    db_to_csv("db_to_csv_output.csv")


