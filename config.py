from configparser import ConfigParser
import os
from jsonschema import validate, ValidationError
import json

configSchema = {
    "type": "object",
    "required": ["discord"],
    "properties": {
        "discord": {
            "type": "object",
            "required": ["username", "oauth_token"],
            "properties": {
                "username": {"type": "string"},
                "oauth_token": {"type": "string"},
                "channels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                },
                "global_admins": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                },
                "required_roles": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                },
            }
        },
        "games": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "type", "app_id", "install_dir", "commands"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "app_id": {"type": "string"},
                    "install_dir": {"type": "string"},
                    "commands": {
                        "type": "object",
                        "required": ["start", "stop", "connect", "delay"],
                        "properties": {
                            "start": {"type": "string"},
                            "stop": {"type": "string"},
                            "update": {"type": "string"},
                            "connect": {"type": "string"},
                            "players": {"type": "string"},
                            "version": {"type": "string"},
                            "delay": {"type": "string"},
                        }
                    },
                    "admins": {
                        "type": "array",
                        "items": {"type": "string"},
                        "uniqueItems": True
                    },
                }
            },
            "uniqueItems": True
        },
    },
}

def loadConfig(filename = "config.json"):
    with open(filename) as data_file:
        data = json.load(data_file)
    data_file.close()
    validate(data, configSchema)
    return data

def testConfig():
    with open("config_test/config_test1.json") as data_file1:
        data1 = json.load(data_file1)
    with open("config_test/config_test2.json") as data_file2:
        data2 = json.load(data_file2)
    with open("config_test/config_test3.json") as data_file3:
        data3 = json.load(data_file3)
    with open("config_test/config_test4.json") as data_file4:
        data4 = json.load(data_file4)
    with open("config_test/config_test5.json") as data_file5:
        data5 = json.load(data_file5)

    num_passed = 0
    try:
        validate(data1, configSchema)
    except ValidationError:
        num_passed+=1

    try:
        validate(data2, configSchema)
    except ValidationError:
        num_passed+=1
    try:
        validate(data3, configSchema)
        num_passed+=1
    except ValidationError:
        print("Failed")

    try:
        validate(data4, configSchema)
    except ValidationError:
        num_passed+=1

    try:
        validate(data5, configSchema)
    except ValidationError:
        num_passed+=1

    return num_passed

config = loadConfig()
num_passed = testConfig()
print("Passed {0}/5 Config Tests.".format(num_passed))