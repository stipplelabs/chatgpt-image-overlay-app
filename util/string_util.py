import random
import math
import re, regex, json

# String utility functions 

def removePhishing(value):
    if not value:
        return value

    # value = value.replace("\\s", "")
    value = re.sub(r"\s+", "", value)  # \s matches all white spaces
    value = value.replace("=", "")
    value = value.replace("'or'", "")
    return value


def rand(length):

    # storing strings in a list
    digits = [i for i in range(0, 10)]

    # initializing a string
    random_str = ""

    # we can generate any lenght of string we want
    for i in range(length):
        # generating a random index
        # if we multiply with 10 it will generate a number between 0 and 10 not including 10
        # multiply the random.random() with length of your base list or str
        index = math.floor(random.random() * 10)

        random_str += str(digits[index])

    return random_str


def extract_json_from_string(text):
    json_pattern = regex.compile(r'(?P<json_obj>\{(?:[^{}]|(?R))*\})|(?P<json_array>\[(?:[^\[\]]|(?R))*\])')
    json_matches = json_pattern.finditer(text)

    extracted_json = []
    for match in json_matches:
        if match.group('json_obj'):
            json_data = json.loads(match.group('json_obj'))
        elif match.group('json_array'):
            json_data = json.loads(match.group('json_array'))
        extracted_json.append(json_data)

    return extracted_json[0] if extracted_json else None
