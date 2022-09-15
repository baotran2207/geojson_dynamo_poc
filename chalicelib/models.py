
from dataclasses import dataclass
from datetime import datetime
from chalicelib.config import settings
from chalicelib.auth import get_password_hash
from chalice import BadRequestError
import boto3
from pydantic import BaseModel
from geojson import Feature, Point
import pygeohash as pgh
import json

User_table = settings.DYNAMO_USER_TABLE_NAME
Feature_table = settings.DYNAMO_FEATURES_TABLE_NAME


class User(BaseModel):
    username: str
    password: str
    hashed_password: str = None
    created_at: datetime = datetime.utcnow()
## inDB
class UserDB(BaseModel):
    username: str
    created_at: str
    hashed_password: str = None
    def __post_init__(self):
        print(self.created_at)

@dataclass
class FeatureDB:
    """
        Dynamodb does not accept float -> we convert to str before import into dynamodb
    """
    geohash: str
    geojson: Feature

    def __post_init__(self):
        coordinates_str = [str(coor) for coor in self.geojson['geometry']['coordinates']]
        self.geojson['geometry']['coordinates'] = coordinates_str



# controllers

## users controller
def create_user(new_user: User):
    table = boto3.resource('dynamodb').Table(User_table)

    username = new_user.username.strip()

    user = get_user(username)
    if user:
        print(f'User exist {user}')
        raise BadRequestError("Username exists")

    hashed_password = get_password_hash(new_user.password)
    item = {
        'username': str(username),
        'hashed_password': str(hashed_password),
        'created_at' : new_user.created_at.isoformat(),
    }
    table.put_item(Item=item)

    return get_user(username)



def get_user(username) -> User:
    table = boto3.resource('dynamodb').Table(User_table)
    user_record = table.get_item(Key={'username': username}).get('Item')
    if user_record:
        return UserDB(**user_record)
    return None

def get_features(max_limit:int =50) ->list:
    table = boto3.resource('dynamodb').Table(Feature_table)
    response = table.scan(Limit=max_limit)
    return response.get('Items',[])


def create_features(features: list[Feature] ) -> list:
    get_coordinates = lambda feature : feature['geometry']['coordinates']
    features_to_put = [
        FeatureDB(
           geohash=pgh.encode(*get_coordinates(feature)),geojson=feature
        )
        for feature in features
    ]

    table = boto3.resource('dynamodb').Table(Feature_table)
    with table.batch_writer() as batch:
        for item in features_to_put:
            batch.put_item(Item=item.__dict__)

    return item.__dict__

def put_feature(geohash, new_item):
    table = boto3.resource('dynamodb').Table(Feature_table)
    table.put_item(Item=new_item)
    return

def get_feature(geohash):
    table = boto3.resource('dynamodb').Table(Feature_table)
    res = table.get_item(Key={
        'geohash': geohash
    },)
    item = res.get('Item', {})

    return item

def delete_feature(geohash):
    table = boto3.resource('dynamodb').Table(Feature_table)
    res = table.delete_item(Key={
        'geohash': geohash
    },)
    item = res.get('Item', {})

    return item