import requests

def get_lat_lng(input_address):
    GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': input_address
    }
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    print(res)

    # Use the first result
    result = res['results'][0]
    print(result)

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    geodata['address'] = result['formatted_address']
    input_address_lat = geodata['lat']
    input_address_lng = geodata['lng']
    print(input_address_lat, input_address_lng)
    return input_address_lat, input_address_lng

get_lat_lng('San Francisco')

    # print(geodata['lat'])
    # print(geodata['lng'])
    # print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))

# self.start = start
# self.destination = destination

#endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
#api_key = 'AIzaSyC-g2jSdIeWUogOM5Kvs5D1wFAJ5ePDvcs'
# #Asks the user to input Where they are and where they want to go.
# origin = start.replace(' ','+')
# end = destination.replace(' ','+')
# #Building the URL for the request
# nav_request = 'origin={}&destination={}&key={}'.format(origin,end,api_key)
# request = endpoint + nav_request
# #Sends the request and reads the response.
# response = urllib.request.urlopen(request).read()
# #Loads response as JSON
# directions = json.loads(response)