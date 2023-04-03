import requests


class Wmata_API:
    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey

    def fetch_predition(self, station, platform):
        response = requests.get(self.url + station,
                                headers={'api_key': self.apikey})
        res = response.json()['Trains']
        #print(res)
        trains = []
        for t in res:
            if t['Group'] == platform:
                if t['Line'] == 'No':
                    t['Line'] = 'No'
                    t['Car'] = 'Passenger'
                    t['Destination'] = None
                trains.append([t['Line'], t['Car'], t['Destination'], t['Min']])

        return trains
