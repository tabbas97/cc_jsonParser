import json

def logdec(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__} with args: {args} and kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logdec
def valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except:
        return False
    
if __name__ == "__main__":
    print(valid_json("{}"))
    print(valid_json("valid:False"))
    print(valid_json(""))