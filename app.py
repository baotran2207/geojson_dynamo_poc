
from chalice import Chalice, AuthResponse, Response
from chalicelib.blueprints import init_blueprint
from chalicelib.auth import decode_jwt_token
from chalicelib.utils import get_page_info, get_base_url, parse_csv_to_json
from geojson import FeatureCollection
from chalicelib.models import create_features, delete_feature, get_features, get_feature, put_feature
import boto3

dy = boto3.resource('dynamodb')
app = Chalice(app_name='geo_poc')

app.register_blueprint

@app.route('/')
def index():
    return {'hello': 'world'}

init_blueprint(app)
# init_db()

@app.authorizer()
def jwt_auth(auth_request):
    token = auth_request.token
    decoded = decode_jwt_token(token)
    return AuthResponse(routes=['*'], principal_id=decoded['username'])

@app.route('/features', methods=['POST'])
def api_create_features():
    body = app.current_request.json_body
    features_raw = body.get('features')

    fea_col = FeatureCollection(features_raw)['features']
    res = create_features(fea_col)
    return {'results': res}

@app.route('/features', methods=['GET'])
def api_get_features():
    query_ = app.current_request.query_params
    page_number = query_ and int(query_.get("page", 1)) or 1
    results_per_page = query_ and int(query_.get("results_per_page", 10)) or 10
    res = get_features()

    start_page, end_page, info = get_page_info(
        len(res),
        page_num=page_number,
        results_per_page=results_per_page,
    )
    total_pages = info.get('total_pages')

    base_url  =  get_base_url(app.current_request)

    response = {
        'meta': info,
        'next_page': page_number < total_pages and f'{base_url}/features?page={page_number + 1}' or '',
        'pre_page': page_number > 1 and f'{base_url}/features?page={page_number - 1}' or '',
        'results': res[start_page:end_page]
    }
    return response
@app.route('/features_with_token', methods=['GET'], authorizer=jwt_auth)
def api_get_features_with_token():
    return api_get_features()

@app.route('/features/{geohash}', methods=['GET'])
def api_get_feature(geohash):
    response = get_feature(geohash)
    return response

@app.route('/features/{geohash}', methods=['DELETE'], authorizer=jwt_auth)
def get_user(geohash):
    response = delete_feature(geohash)
    return f'Deleted {geohash}'

@app.route('/features/{geohash}', methods=['PUT'], authorizer=jwt_auth)
def get_user(geohash):
    response = put_feature(geohash, app.current_request.json_body)
    return response

