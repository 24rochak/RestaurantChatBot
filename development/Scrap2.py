import requests
import json

business_id = 'YdKrw2kuULpYX9FdP2RrAA'

API_KEY = 'YaLAtuExWjgw9PmNxD2dPzxaLWqXgU5dE0A4SX29VwqCH9OGzUigzK3jN021IDjvZcIWLA8Chz9jfWfLuZYUeP9a4517rXs16Y8d8d-AADj_U0yHYhlQGAnhaYegXXYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

data = {}
ids = []
for i in range(0, 1000, 50):
    PARAMETERS = {'term': 'european restaurant',
                  'limit': 50,
                  'location': 'New York',
                  'offset': i}
    response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    temp_data = response.json()
    print("Retrieved data from offset {}".format(i))
    for item in temp_data['businesses']:
        ids.append(item)

data['businesses'] = ids

data = data['businesses'][0]

f = open("european_data.json", mode='w')
json.dump(data, f)
f.close()