import pytest
import json
import glob

@pytest.fixture
def ccjson():
    import ccjson
    yield ccjson

def test_trim_json(ccjson):
    assert ccjson.trim_json("  {  key  :  value  }  ") == "{key:value}"
    assert json.loads(ccjson.trim_json(open("tests/tests/step3/valid.json").read())) == json.loads(open("tests/tests/step3/valid.json").read())
    assert json.loads(ccjson.trim_json(open("tests/tests/step4/valid.json").read())) == json.loads(open("tests/tests/step4/valid.json").read())

def test_step1_valid(ccjson):
    assert ccjson.parse_json("{}") == {}
    assert ccjson.parse_json("[]") == []
    assert ccjson.parse_json(open("tests/tests/step1/valid.json").read()) == json.loads(open("tests/tests/step1/valid.json").read())

def test_step1_invalid(ccjson):
    with pytest.raises(ValueError):
        ccjson.parse_json("")
        ccjson.parse_json("valid:False")
        ccjson.parse_json(open("tests/tests/step1/invalid.json").read())

def test_json_list(ccjson):
    assert ccjson.parse_json("[1,2,3]") == [1,2,3]

def test_step2_valid1(ccjson):
    ccjo = ccjson.parse_json('{"key":"value"}')
    print(ccjo)
    assert ccjson.parse_json('{"key":"value"}') == {"key":"value"}
def test_step2_valid2(ccjson):
    assert ccjson.parse_json('{"key1":"value1","key2":"value2"}') == {"key1":"value1","key2":"value2"}
def test_step2_valid3(ccjson):
    assert ccjson.parse_json(open("tests/tests/step2/valid.json").read()) == json.loads(open("tests/tests/step2/valid.json").read())

def test_step2_invalid1(ccjson):
    with pytest.raises(ValueError):
        ccjson.parse_json(open("tests/tests/step2/invalid.json").read())
        
def test_step2_invalid(ccjson):
    with pytest.raises(ValueError):
        ccjson.parse_json('{"key":"value"')
        ccjson.parse_json('{"key":"value"')
        ccjson.parse_json('{"key":"value"')

def test_step3_valid(ccjson):
    assert ccjson.parse_json(open("tests/tests/step3/valid.json").read()) == json.loads(open("tests/tests/step3/valid.json").read())

def test_step3_invalid(ccjson):
    with pytest.raises(ValueError):
        ccjson.parse_json(open("tests/tests/step3/invalid.json").read())

def test_step4_valid(ccjson):
    assert ccjson.parse_json(open("tests/tests/step4/valid.json").read()) == json.loads(open("tests/tests/step4/valid.json").read())

def test_step4_invalid(ccjson):
    with pytest.raises(ValueError):
        ccjson.parse_json(open("tests/tests/step4/invalid.json").read())

@pytest.mark.parametrize(
        "json_str, expected", 
        ids = glob.glob("test/test/pass*.json"), 
        argvalues = [(
                open(file).read(), 
                json.loads(open(file).read())
            ) for file in glob.glob("test/test/pass*.json")]
        )
def test_step5_valid(ccjson, json_str, expected):
    import glob
    assert ccjson.parse_json(json_str) == expected

@pytest.mark.parametrize(
        "json_str", 
        ids = glob.glob("test/test/fail*.json"), 
        argvalues = [ open(file).read() for file in glob.glob("test/test/fail*.json") ]
        )
def test_step5_invalid(ccjson, json_str):
    with pytest.raises(ValueError):
        ccjson.parse_json(json_str)