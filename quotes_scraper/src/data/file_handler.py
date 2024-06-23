import json

def to_json(data, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def from_json(file_name):  
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

