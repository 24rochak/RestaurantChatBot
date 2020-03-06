import boto3
import json
import os


def buildItem(data, cuisine):
    item = {}
    if 'id' in data:
        item['RestaurantID'] = {'S': data['id']}
    if 'name' in data:
        item['name'] = {'S': data['name']}
    if 'rating' in data:
        item['rating'] = {'S': str(data['rating'])}
    if 'coordinates' in data:
        item['location'] = {'SS': [str(data['coordinates']['latitude']), str(data['coordinates']['longitude'])]}
    if 'price' in data:
        item['price'] = {'S': data['price']}
    if 'location' in data and 'display_address' in data['location']:
        item['address'] = {'S': ", ".join(row for row in data['location']['display_address'])}
    if 'phone' in data:
        item['phone'] = {'S': data['phone']}
    item['cuisine'] = {'S': cuisine}
    return item


dynamodb = boto3.client('dynamodb')

fnames = os.listdir("Restaurant Data")

failCount, passCount = 0, 0
for name in fnames:
    fname = os.path.join("Restaurant Data", name)
    cuisine = fname.split('\\')[1].split('_')[0]
    print(fname, cuisine)
    with open(fname, 'r') as f:
        data = json.load(f)['businesses']

    for i, business in enumerate(data):
        if not business['is_closed']:
            item = buildItem(business, cuisine)
            try:
                dynamodb.put_item(TableName='yelp-restaurants', Item=item)
                passCount += 1
            except:
                print("Failed")
                failCount += 1
        print("Processed: {} of {}".format(i, cuisine))

print("Pass Count: ", passCount)
print("Fail Count: ", failCount)
