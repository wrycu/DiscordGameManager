from jsonschema import validate, ValidationError
from json import load
from config_schema import configSchema

def loadConfig(filename = "config.example.json"):
    with open(filename) as data_file:
        data = load(data_file)
    data_file.close()
    validate(data, configSchema)
    print(validate(data, configSchema))
    return data