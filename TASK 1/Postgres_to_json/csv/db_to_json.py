import psycopg2


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


def escape_string(s):
    return s.replace('"', '\\"')

json_output = '['
for i, row in enumerate(rows):
    json_output += '{'
    for j, value in enumerate(row):
        key = column_names[j]
        if isinstance(value, str):
            val_str = f'"{escape_string(value)}"'
        else:
            val_str = str(value)
        json_output += f'"{key}": "{val_str}"' if key == "hire_date" else f'"{key}": {val_str}'
        if j < len(row) - 1:
            json_output += ', '
    json_output += '}'
    if i < len(rows) - 1:
        json_output += ', '
json_output += ']'

print("Output saved into file",json_output)
f = open('db_to_json_output','w')
f.write(json_output)
f.close()

cursor.close()
conn.close()