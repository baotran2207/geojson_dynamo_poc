from chalicelib.config import settings
import boto3

DEFAULT_USERNAME = settings.default_username
DEFAULT_PASSWORD = settings.default_password

User_table = settings.DYNAMO_USER_TABLE_NAME
features_table = settings.DYNAMO_FEATURES_TABLE_NAME

TABLES = {
    'features': {
        'name': features_table,
        'hash_key': 'geohash',
        # 'range_key': 'username',
        'capacity': 5
    },
    'users': {
        'name': User_table,
        'hash_key': 'username',
        'capacity': 1
        # 'range_key': "created_at"
    }
}


def create_table(table_name, hash_key, range_key=None, capacity=1):
    client = boto3.client('dynamodb')
    key_schema = [
        {
            'AttributeName': hash_key,
            'KeyType': 'HASH',
        }
    ]
    attribute_definitions = [
        {
            'AttributeName': hash_key,
            'AttributeType': 'S',
        }
    ]
    if range_key is not None:
        key_schema.append({'AttributeName': range_key, 'KeyType': 'RANGE'})
        attribute_definitions.append(
            {'AttributeName': range_key, 'AttributeType': 'S'})
    try:
        client.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': int(capacity),
                'WriteCapacityUnits': int(capacity),
            }
        )
        waiter = client.get_waiter('table_exists')
        waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})
        print(f"Table {table_name} is created ! ")
    except client.exceptions.ResourceInUseException:
        print(f"Table {table_name} exits ! ")
    return table_name

def init_db():
    for table_config in TABLES.values():
        create_table(
            table_config.get('name'),
            table_config.get('hash_key'),
            table_config.get('range_key'),
            table_config.get('capacity'),
        )

