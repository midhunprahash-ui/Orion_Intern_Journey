def convert_csv_to_postgres_bulk_insert(csv_path, sql_path, table_name):
    with open(csv_path, 'r') as csv_file:
        lines = csv_file.readlines()

    headers = lines[0].strip().split(',')

    sql_lines = [f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES\n"]

    value_lines = []
    for line in lines[1:]:
        values = line.strip().split(',')

        formatted_values = []
        for val in values:
            val = val.strip().replace("'", "''")  
            if val.replace('.', '', 1).isdigit():  
                formatted_values.append(val)
            else:
                formatted_values.append(f"'{val}'")
        
        value_lines.append(f"({', '.join(formatted_values)})")

    final_sql = ',\n'.join(value_lines) + ";\n"

    with open(sql_path, 'w') as sql_file:
        sql_file.write(sql_lines[0])
        sql_file.write(final_sql)


if __name__ == "__main__":
    convert_csv_to_postgres_bulk_insert('db_to_csv_output.csv', 'csv_to_sql.sql', 'employee')