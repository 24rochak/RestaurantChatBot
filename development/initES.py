import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

dynamodb = boto3.resource('dynamodb')

yelp_restaurants = dynamodb.Table('yelp-restaurants')
data = yelp_restaurants.scan()['Items']

print(len(data))

session = boto3.session.Session()
credentials = session.get_credentials()
service = 'es'
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, session.region_name, service)
endpoint = "https://search-search-restaurant-glzu626h7v2stq24rvzlvbncpu.us-east-1.es.amazonaws.com/"

es = Elasticsearch(
    endpoint,
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())
count = 0
for restaurant in data:
    restaurantID = restaurant['RestaurantID']
    cuisine = restaurant['cuisine']

    document = {
        'RestaurantID': restaurantID,
        'cusisine': cuisine
    }

    es.index(index='restaurants', doc_type='restaurant', id=restaurantID, body=document)

    check = es.get(index='restaurants', doc_type='restaurant', id=restaurantID)
    if check:
        print("Index %s found" % restaurantID)
        count += 1
        print(count)
