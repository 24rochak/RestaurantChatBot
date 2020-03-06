import random
import urllib3

global URL
import json

URL = "https://search-search-restaurant-glzu626h7v2stq24rvzlvbncpu.us-east-1.es.amazonaws.com/restaurants/"

size = 30


def getCount(cuisine):
    countURL = URL + '_count?q=' + cuisine
    try:
        http = urllib3.PoolManager()
        result = http.request('GET', countURL).data
        data = json.loads(result.decode('utf-8'))
        return data['count']
    except:
        return None


def getData(cuisine, start, size):
    searchURL = URL + '_search?q=' + cuisine + '&from=' + str(start) + '&size=' + str(size)
    try:
        http = urllib3.PoolManager()
        result = http.request('GET', searchURL).data
        data = json.loads(result.decode('utf-8'))
        return data
    except:
        return None


def getRestaurantIDs(hits):
    return [item['_source']['RestaurantID'] for item in hits]


# matchingCount = getCount(cuisine='chinese')
# if matchingCount:
#     print("Count: ", matchingCount)
# start = random.randrange(matchingCount - size - 1)
#
# data = getData(cuisine='chinese', start=start, size=size)
# hits = data['hits']['hits']
# IDs = getRestaurantIDs(hits=hits)
# print(IDs)

IDs = ['FJFliqqHXFZutkp_dmWdfw', 'SMImQM_JfZkIZwflTgOAoQ', 'Qwd4Tv-CqgO2Yl9zZgkKOQ', 'e-6UcplEErq2Hj14-eiM6Q',
       'nzgtntDHIH8Gygim1cQBxA', '1QXTYR312XXgUExNmTEWuA', 'sinDhwX8Egru_3FCI7bhkw', 'K0qsGnFv-edPDqVBdLCocQ',
       'JAC3_9kPdF0TFVBt3gYQVA', 'MYPes7EWP5aLiVG1Z_9eFQ', 'GJZnf3B-ADjlCV1NXsHvGQ', '4pnfZWTgH2924iEKRa0hkw',
       'mUl0wtO7tPkBocuJqZ-7Dw', 'zYoL-o9YJpGTwJ-Gmj8AFA', 'AQqUiXi0hn1xu5qVfM54IQ', '3K7Kc82bhU6-qjAjsBs3Fw',
       'si4n0EtvAl3QisVHoKPOuw', 'fgGRIM0b9JGIoNOAnHzROQ', 'FDhOPRZ01PDEEH-QCnVIyQ', 'b7uTP_afs5Gkf66K7yDl-w',
       'nrsWSUJdNtOhV2UzPi-oOQ', 'cCHkQ5oISNafWnLoBpsagg', 'lt3Leywt1pzy23OzDqYRVA', 'ikx8R8u2lmxhpLGByCjgPw',
       'qVVBIO2w2HfEGS3SA27RUg', 'ItZ8CzZAGXGjB8_9HxDIXg', 'Gd3_3mxOvj2xYiqysV8rbQ', 'zdX9mwhoknXXYL1GCstnow',
       '54om5q7V4anmIXw2PdNJbA', 'AbfZkSRMtiHE3naWrN-0Eg']

import boto3

client = boto3.client('dynamodb')

restaurants = []

for id in IDs:
    data = client.get_item(TableName='yelp-restaurants',
                           Key={
                               'RestaurantID': {'S': id}
                           })

    data = data['Item']
    name = data['name']['S']
    address = data['address']['S']
    rating = data['rating']['S']
    phoneNumber = data['phone']['S']
    restaurants.append([name,address,rating,phoneNumber])

restaurants.sort(key=lambda x:x[2],reverse=True)
print(restaurants)
