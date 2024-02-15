# Will not use JSON module, but will use the json module to test the output of the ccjson module
import sys

def trim_json(json_str):
    # Possible locations for trimming:
    # 1. Remove leading and trailing whitespaces
    # 2. Any space not within a string can be removed
    # 3. Remove any \n, \t, \r

    # Remove leading and trailing whitespaces
    json_str = json_str.strip()

    # Remove any space not within a string
    # Remove any \n, \t, \r
    in_string = False
    new_json_str = ""
    for char in json_str:
        if char == "\"":
            in_string = not in_string
        if char in [" ", "\n", "\t", "\r"]:
            if in_string:
                new_json_str += char
        else:
            new_json_str += char

    return new_json_str

def parse_json(json_str):

    if json_str == "":
        raise ValueError("Empty string")
    
    json_str = trim_json(json_str)
    
    # if len(json_str) == 2:
        # if json_str[0] == "{":
            # return {}
        # elif json_str[0] == "[":
            # return []
    if json_str == "[]":
        return []
    
    if json_str == "{}":
        return {}
        
    # If the string does not contain any curly braces or square brackets, it is a simple string or boolean
    if "{" not in json_str and "[" not in json_str:
        
        if json_str == "true":
            return True
        
        if json_str == "false":
            return False
        
        if json_str == "null":
            return None
        else:
            if json_str[0] == "\"" and json_str[-1] == "\"":
                return json_str.strip()[1:-1]
            else:
                try:
                    return int(json_str)
                except:
                    try:
                        return float(json_str)
                    except:
                        print(json_str, file=sys.stderr)
                        raise ValueError("Invalid JSON string")
        
    # Every element in the json will again be a valid json string
    # Split the string into elements
    elements = json_str[1:-1].split(",")

    # If the string starts with a curly brace, it is a dictionary
    if json_str[0] == "{":
        json_dict = {}
        for element in elements:
            key, value = element.split(":")
            json_dict[key.strip()[1:-1]] = parse_json(value)
        
        # print(json_dict)
        return json_dict
    
    # If the string starts with a square bracket, it is a list
    if json_str[0] == "[":
        json_list = []
        for element in elements:
            json_list.append(parse_json(element))
        
        # print(json_list)
        return json_list
    
    raise ValueError("Invalid JSON string")
    
def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()
    
if __name__ == "__main__":

    import sys
    try:
        if len(sys.argv) > 1:
            parse_json(read_file(sys.argv[1]))
            print("Valid JSON", flush=True)
            exit(0)
        else:
            parse_json(sys.stdin.read())
            print("Valid JSON", flush=True)
            exit(0)
    except ValueError as e:
        exit(1)
    except Exception as e:
        print("unknown error", file=sys.stderr)
        exit(1)