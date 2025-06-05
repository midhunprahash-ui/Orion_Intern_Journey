def convert_json_text_to_postgres_sql(json_path, sql_path, table_name):
    with open(json_path, 'r') as file:
        content = file.read()

    
    content = content.strip()
    content = content[1:-1]  
    records = content.split('},')

    data = []
    columns = []

    for i, record in enumerate(records):
        record = record.strip()
        if not record.endswith('}'):
            record += '}'

        
        record = record[1:-1]
        items = record.split(',')

        row = []
        keys = []

        for item in items:
            key, val = item.split(':', 1)
            key = key.strip().strip('"')
            val = val.strip().strip('"')

            val = val.replace("'", "''") 

            if val.replace('.', '', 1).isdigit() and '-' not in val:
                row.append(val)
            else:
                row.append(f"'{val}'")
            
            keys.append(key)

        if not columns:
            columns = keys

        data.append(f"({', '.join(row)})")

    insert_head = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n"
    final_sql = insert_head + ',\n'.join(data) + ";\n"

    with open(sql_path, 'w') as file:
        file.write(final_sql)


convert_json_text_to_postgres_sql('csv_to_json.json', 'json_to_sql.sql', 'employee')