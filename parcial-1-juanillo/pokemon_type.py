import requests


class PokemonType:
    def __init__(self, url: str):
        self.url: str = url
        self.name: str = ''
        response = requests.get(url).json()
        for name in response['names']:
            if name['language']['name'] == 'es':
                self.name = name['name']
                break
