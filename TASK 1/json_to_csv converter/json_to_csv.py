def parse_json_array(json_str):
    json_str = json_str.strip()
    if not (json_str.startswith('[') and json_str.endswith(']')):
        raise ValueError("Not a JSON array")
    json_str = json_str[1:-1].strip()

    objects = []
    buffer = ''
    depth = 0
    for c in json_str:
        if c == '{':
            depth += 1
        if c == '}':
            depth -= 1
        buffer += c
        if depth == 0 and buffer.strip():
            objects.append(buffer.strip())
            buffer = ''
    items = []
    for obj_str in objects:
        obj_str = obj_str.strip()
        if obj_str.startswith(','):
            obj_str = obj_str[1:]
        if obj_str.startswith('{') and obj_str.endswith('}'):
            obj_str = obj_str[1:-1]
        pairs = []
        curr = ''
        in_quotes = False
        for ch in obj_str:
            if ch == '"' and (not curr or curr[-1] != '\\'):
                in_quotes = not in_quotes
            if ch == ',' and not in_quotes:
                pairs.append(curr)
                curr = ''
            else:
                curr += ch
        if curr:
            pairs.append(curr)
        obj = {}
        for pair in pairs:
            if ':' not in pair:
                continue
            key, value = pair.split(':', 1)
            key = key.strip().strip('"')
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.replace('.', '', 1).isdigit():
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            obj[key] = value
        items.append(obj)
    return items

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        json_str = f.read()

    data = parse_json_array(json_str)

    headers = []
    for item in data:
        for key in item.keys():
            if key not in headers:
                headers.append(key)

    
    with open(csv_file, 'w') as f:
        f.write(','.join(headers) + '\n')
        for item in data:
            row = []
            for h in headers:
                value = item.get(h, "")
                if isinstance(value, str) and (',' in value or '"' in value):
                    value = '"' + value.replace('"', '""') + '"'
                row.append(str(value))
            f.write(','.join(row) + '\n')


json_to_csv('diabetes.json', 'diabetes.csv')
