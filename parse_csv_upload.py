import csv
import json
from pprint import pprint

import requests
from geojson import Feature, FeatureCollection, Point

f_path = "tests/fixtures/municipalities_v7_mini.csv"

base_url = "https://7tbwx0uuee.execute-api.ap-southeast-1.amazonaws.com/api"  ## replace with actual deployment
base_url = "http://localhost:8000"  ## local only, comment out
reader = csv.DictReader(open(f_path, encoding="utf-8"))


def gen_chunks(reader, chunksize=10):
    """
    Chunk generator. Take a CSV `reader` and yield
    `chunksize` sized slices.
    """
    chunk = []
    for index, line in enumerate(reader, 0):
        if index % chunksize == 0 and index > 0:
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk


def post_data(data) -> requests.Response:
    return requests.post(
        f"{base_url}/features",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )


def serilize_data(raw_data: list) -> Feature:
    lat = float(raw_data.get("latitude"))
    long = float(raw_data.get("longitude"))
    point = Point((lat, long))
    return Feature(
        geometry=point,
        properties={
            "municipality": raw_data.get("municipality"),
            "province": raw_data.get("province"),
        },
    )


def main():
    for chunk_data in gen_chunks(reader, chunksize=5):

        to_post_data = {
            "type": "FeatureCollection",
            "features": [serilize_data(data) for data in chunk_data],
        }

        response = post_data(to_post_data)
        print(response)


if __name__ == "__main__":
    main()
