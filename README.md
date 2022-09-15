

## I. Geo Poc
Poc for geojson  Rest api
Alive example is deployed at :
    [https://7tbwx0uuee.execute-api.ap-southeast-1.amazonaws.com/api/features?page=1](https://7tbwx0uuee.execute-api.ap-southeast-1.amazonaws.com/api/features?page=1).
## II. Delevelopment
1. Installation
- create a virtualenv with version `3.9.12` . Note: This is dev/test on python `3.9.12`, maybe lower version work (?) . Version `3.10+` does not work yet
- activate the new created virtualenv
- Install libraries:
    `pip install -r requirements.txt`
    `pip install -r requirements-dev.txt`
2. init db
`python init_resources.py`
3. Run dev
`chalice local`

4. Routes list :
    a. Open new tab
    b. activate the new created virtualenv
    c. Now we can try below commands

    - Create user
    `http POST http://127.0.0.1:8000/auth/register username=baotran13 password=123`
    `http POST https://7tbwx0uuee.execute-api.ap-southeast-1.amazonaws.com/api/auth/register username=someone password=123`
    - login (save response somwhere)
    `http POST http://127.0.0.1:8000/auth/login username=baotran13 password=123`
    `http POST https://7tbwx0uuee.execute-api.ap-southeast-1.amazonaws.com/api/auth/login username=someone password=123`

    - get list
    `http GET http://127.0.0.1:8000/features?page=1`
    `http GET https://7tbwx0uuee.execute-api.ap-southeast-1.amazonaws.com/api/features?page=1`

    - get list with token (replace token return from `/login` ) - same result get list
    `http GET http://127.0.0.1:8000/features_with_token 'Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJhb3RyYW4xMyIsImp0aSI6Ijg1M2FhNzEwLTJjNmUtNDQwYi04ZTJmLThjY2RhY2FhM2IwZCJ9._eodpfPE_JiPhR0XF9Xh-VfTH18cA68QmYyxLSp_Wqo' `
    `http GET https://7tbwx0uuee.execute-api.ap-southeast-1.amazonaws.com/api/features_with_token 'Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJhb3RyYW4xMyIsImp0aSI6Ijg1M2FhNzEwLTJjNmUtNDQwYi04ZTJmLThjY2RhY2FhM2IwZCJ9._eodpfPE_JiPhR0XF9Xh-VfTH18cA68QmYyxLSp_Wqo' `
    - get one (the id is geohas from get list)
    `http GET http://127.0.0.1:8000/features/u1k9ztpu51k5`
    `http GET http://127.0.0.1:8000/features/u1k9ztpu51k5`
    - delete one (the id is geohash from get list)
    `http GET http://127.0.0.1:8000/features/u1k9ztpu51k5 'Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJhb3RyYW4xMyIsImp0aSI6Ijg1M2FhNzEwLTJjNmUtNDQwYi04ZTJmLThjY2RhY2FhM2IwZCJ9._eodpfPE_JiPhR0XF9Xh-VfTH18cA68QmYyxLSp_Wqo' `

    `http GET http://127.0.0.1:8000/features/u1k9ztpu51k5 'Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJhb3RyYW4xMyIsImp0aSI6Ijg1M2FhNzEwLTJjNmUtNDQwYi04ZTJmLThjY2RhY2FhM2IwZCJ9._eodpfPE_JiPhR0XF9Xh-VfTH18cA68QmYyxLSp_Wqo' `

## III.Deployment
1. Allow iam policy dynamydb
- open file `.chalice/policy-prod.json`
- replace my account with valid account (12 digit)
2. Run deploy:
- `chalice deploy --stage prod`
3. Url is printed out if deployment is successfully

## IV. Post the csv file
### Local
1. (Local only) Run the local dev in step II.3
2. Open new tab
3. Go to the project dir
4. Activate the virtualenv created in step II.1
3. Run : `python parse_csv_upload.py`
### Prod api
2. Open new tab
3. Go to the project dir
4. Activate the virtualenv created in step II.1
5. Open file `parse_csv_upload.py` :
    - comment out line 11th
    - line 10th , replace the value with the value in III.3

### Note/Limitation:
- Geohash id : there is no small enough libary for geohash , so i can only hash `Point` -> only accept `Point`  . Any recommend how to hash `polygon` ?
- Dynamodb scan issue : if we scan the the huge table without query ,it may lead to capacity issue in dynamodb.
    - We only post the mini version of the csv 100 records .
    - Once all api work well then we can try to post all 7000.
    - Dynamodb only support next_page_token type, not number_page_token -> we scan all -> too many records may leads to capacity-problem

- route `/features_with_token` is just an example of token auth. For convinence , other routes are public (can be added authorized later)
- Dynamodb only support next_page_token type, not number_page_token -> we scan all -> too many records may leads to capacity-problem
