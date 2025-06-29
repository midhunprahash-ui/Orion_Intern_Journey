import psycopg2
from config import DB_CONFIG2

def format_value(value):

    if value is None:
        return ''
    value = str(value)
    if ',' in value or '"' in value:
        return f'"{value.replace("`", "``")}"'
    return value

def db_to_csv(output_file):

    conn = psycopg2.connect(DB_CONFIG2)
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM name_matching_samples")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    with open(output_file, 'w') as f:
        f.write(','.join(column_names) + '\n')
        

        
        for row in rows:
            csv_row = ','.join(format_value(value) for value in row)
            f.write(csv_row + '\n')
            

    
    cursor.close()
    conn.close()
    f.close()


if __name__ == "__main__":
    db_to_csv("modeltraining_output.csv")


