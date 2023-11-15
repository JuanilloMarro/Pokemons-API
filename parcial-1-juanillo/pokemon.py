from __future__ import annotations
from pokemon_type import PokemonType
import requests


class Pokemon:
    def __init__(self, name: str, url: str):
        self.name: str = name
        self.is_completed = False
        self.url: str = url
        self.id: int | None = None
        self.height: int | None = None
        self.weight: int | None = None
        self.description: str | None = None
        self.pokemon_types: list[PokemonType] | None = None
        self.image: str | None = None

    def get_specie(self):
        if type(self.id) is int:
            endpoint = f'https://pokeapi.co/api/v2/pokemon-species/{self.id}/'
            response = requests.get(endpoint).json()
            for entry in response['flavor_text_entries']:
                language = entry['language']
                if language['name'] == 'es':
                    self.description = entry['flavor_text']
                    break

            for entry in response['names']:
                if entry['language']['name'] == 'es':
                    self.name = entry['name']
                    break

    def get_data(self):
        self.pokemon_types = []
        response = requests.get(self.url).json()
        self.id = response['id']
        self.image = response['sprites']['front_default']
        self.get_specie()

        for item in response['types']:
            pokemon_type = PokemonType(item['type']['url'])
            self.pokemon_types.append(pokemon_type)

    @staticmethod
    def get_pokemon_list(page: int = 0) -> list[Pokemon]:
        pokemon_list = []
        endpoint = 'https://pokeapi.co/api/v2/pokemon'
        response = requests.get(
            endpoint,
            params={
                'limit': 20,
                'offset': page * 20
            }
        ).json()

        for result in response['results']:
            pokemon = Pokemon(result['name'], result['url'])
            pokemon_list.append(pokemon)

        return pokemon_list
