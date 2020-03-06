import boto3

# client = boto3.client('sns')
#
# response = client.publish(PhoneNumber='+16462703160', Message="This is test message from boto3")
# print(response)
data = [['Foo-Hing Chinese Kitchen', '2706 3rd Ave, Bronx, NY 10454', '4.5', '+17186657593'],
        ['Pho New York Restaurant', '73 Mulberry St, New York, NY 10013', '4.5', '+16467918039'],
        ['Delicious Wok', '5952 Summerfield St, Ridgewood, NY 11385', '4.5', '+17183668882']]


def buildMessage(people, time, data):
    base = "Here are top suggestions for {} people, for today at {}. ".format(people, time)
    base = ""
    i = 0
    flag = True
    while flag and i < 3:
        temp = "{} located at {} reachable at {}. ".format(data[i][0], data[i][1][:-6], data[i][3])
        if len(temp) + len(base) < 160:
            base += temp
            i += 1
        else:
            flag = False
    print(base)


buildMessage(2, '4 pm', data)
