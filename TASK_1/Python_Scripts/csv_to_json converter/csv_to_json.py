def format_value(value):

    if value.replace('.', '').isdigit():
        return value  
    return f'"{value}"' 

def csv_to_json(csv_file, json_file):

    json_data = '['
    
    with open(csv_file, 'r') as file:
    
        headers = file.readline().strip().split(',')
        
        
        first_record = True
        for line in file:
            values = line.strip().split(',')
            
            
            if not first_record:
                json_data += ','
            first_record = False
            
            
            json_data += '\n  {'
            for i, value in enumerate(values):
                if i > 0:  
                    json_data += ','
                json_data += f'\n    "{headers[i]}": {format_value(value)}'
            json_data += '\n  }'
    

    json_data += '\n]'
    
    
    with open(json_file, 'w') as file:
        file.write(json_data)


csv_to_json('diabetes.csv', 'csv_to_json.json')
