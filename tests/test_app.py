import csv
import json
from typing import Dict, Generator

import pytest
from chalice.test import Client

from app import app


def test_index():
    with Client(app) as client:
        response = client.http.get("/")
        assert response.json_body == {"hello": "world"}


def load_params_from_json(json_path):
    with open(json_path) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def client() -> Generator:
    with Client(app) as c:
        yield c


@pytest.fixture(scope="function")
def example_features():
    with open("tests/fixtures/examples.json") as f:
        return json.load(f)


@pytest.fixture(scope="function")
def netherland_city_mini():
    f_path = "tests/fixtures/municipalities_v7_mini.csv"
    jsonArray = []
    with open(f_path, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            jsonArray.append(row)

    return jsonArray


def test_create_features(
    client,
    example_features,
    # mocker
):
    ## We do not install pytest-mock so let not mock but call actual api
    #     mocker.patch('client.http.post', return_value={})
    res = client.http.post(
        "/features",
        headers={"Content-Type": "application/json"},
        body=json.dumps(example_features),
    )
    assert res.status_code == 200
