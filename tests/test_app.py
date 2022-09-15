from chalice.test import Client
from app import app
import pytest
import json
from typing import Dict, Generator
import csv
def test_index():
    with Client(app) as client:
        response = client.http.get('/')
        assert response.json_body == {'hello': 'world'}

# the fixtures/examples.json is from https://en.wikipedia.org/wiki/GeoJSON


def load_params_from_json(json_path):
    with open(json_path) as f:
        return json.load(f)

@pytest.fixture(scope="module")
def client() -> Generator:
    with Client(app) as c:
        yield c

@pytest.fixture(scope="function")
def example_features():
    with open('tests/fixtures/examples.json') as f:
        return json.load(f)

@pytest.fixture(scope="function")
def netherland_city_mini():
    f_path = 'tests/fixtures/municipalities_v7_mini.csv'
    jsonArray = []

    #read csv file
    with open(f_path, encoding='utf-8') as csvf:
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        #convert each csv row into python dict
        for row in csvReader:
            #add this python dict to json array
            jsonArray.append(row)

    return jsonArray
def test_create_features(client, example_features):
    res = client.http.post(
        '/features',
        headers={'Content-Type':'application/json'},
        body=json.dumps(example_features)

    )
    assert res.status_code == 200


def test_post_csv(client, netherland_city_mini):
    pass