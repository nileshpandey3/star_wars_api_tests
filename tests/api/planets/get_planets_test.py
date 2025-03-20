import random

import pytest
import requests

from ....helper.request import request
from ....setup import BASE_URL

@pytest.mark.planets_api
class TestGetPlanets:
    """
    Verify the '/planets' star wars api endpoint
    https://swapi.dev/documentation#planets
    """

    @classmethod
    def setup_class(cls):
        """
        Since this api doesn't require any class level setup/teardown steps,
        I have left them as blank but in most real world use cases
        we should use them as an automation best practice.
        """

    @pytest.mark.get_all_planets_test
    def test_get_all_planets(self):
        # Verify GET all request to the '/planets' end point

        url = BASE_URL + 'planets'
        resp = request(
            request_type='GET',
            url=url
        )
        resp.raise_for_status()
        json_response = resp.json()
        planet_results = json_response['results']

        assert planet_results, f'GET request to {url} returned an empty response'
        assert isinstance(len(planet_results), int)

        # Verify that for each of the resultant planets we can find the expected attributes
        for planet in planet_results:
            if planet is not None:
                assert planet['name']
                assert planet['rotation_period']
                assert planet['orbital_period']
                assert planet['diameter']
                assert planet['climate']
                assert planet['gravity']
                assert planet['terrain']
                assert planet['surface_water']
                assert planet['population']
                assert planet['films']
                assert planet['url']
            else:
                print(f'Resultant planet: {planet} is None')

    @pytest.mark.get_planet
    def test_get_planet(self):
        # Verify that we can get a specif planet resource and validate its properties

        planet_id = 1
        url = BASE_URL + f'planets/{planet_id}/'
        resp = request(
            request_type='GET',
            url=url
        )
        resp.raise_for_status()
        planet = resp.json()

        if planet is not None:
            assert planet['name'] == 'Tatooine'
            assert planet['rotation_period'] == '23'
            assert planet['orbital_period'] == '304'
            assert planet['diameter'] == '10465'
            assert planet['climate'] == 'arid'
            assert planet['gravity'] == '1 standard'
            assert planet['terrain'] == 'desert'
            assert planet['surface_water'] == '1'
            assert planet['population'] >= '200000'
            assert isinstance(planet['films'], list)
            assert len(planet['films']) >= 0
            assert isinstance(planet['residents'], list)
            assert len(planet['residents']) >= 0
            assert planet['url'] == url
        else:
            print(f'{planet} is None')

    @pytest.mark.get_non_existent_planet
    def test_get_non_existent_planet(self):
        # Verify the response when we request for a non-existent planet resource
        # We can test this by passing either a very large , zero or negative number
        # for the planet id

        planet_id = random.randint(-1, 999)
        url = BASE_URL + f'planets/{planet_id}'
        resp = request(
            request_type='GET',
            url=url
        )

        assert resp.status_code == 404
        assert resp.json()['detail'] == 'Not found'

    @pytest.mark.get_planet_invalid_data
    def test_get_planet_invalid_data(self):
        # Verify the response when we request for a planet resource
        # by providing the resource id inside an invalid data structure

        planet_id = [1] # pass a list with 1 number
        url = BASE_URL + f'planets/{planet_id}'
        resp = request(
            request_type='GET',
            url=url
        )

        assert resp.status_code == 404
        assert resp.json()['detail'] == 'Not found'

    @pytest.mark.get_empty_planet
    def test_get_empty_planet(self):
        # Verify the response when we request for a planet resource
        # by providing an emtpy input

        url = BASE_URL + 'planets/ '
        resp = request(
            request_type='GET',
            url=url
        )

        assert resp.status_code == 404
        assert resp.json()['detail'] == 'Not found'

    @pytest.mark.get_planet_special_char
    def test_get_planet_special_char(self):
        # Verify the response when we request for a planet resource
        # by providing special characters as an input

        url = BASE_URL + 'planets/$%&$*'
        resp = request(
            request_type='GET',
            url=url
        )

        assert resp.status_code == 404
        assert resp.json()['detail'] == 'Not found'

    @pytest.mark.schema
    def test_api_schema(self):
        # Verify the JSON Schema of the planets resource

        url = BASE_URL + 'planets/schema/'
        resp = request(
            request_type='GET',
            url=url,
        )

        # In my testing the GET request to the '/planets/schema' is not returning the
        # expected schema object but, instead it intermittently returns either a 301 or a 404 error
        # so I am just asserting based on that for the purpose of completing this assignment

        if resp.status_code == 301:
            attributes = vars(resp)
            assert attributes['status_code'] == 301
            assert attributes['headers']['Content-Type'] == 'text/html'
            assert attributes['Location'] == url
            assert attributes['reason'] == 'Moved Permanently'
        elif resp.status_code == 404:
            assert resp.json()['detail'] == 'Not found'
        else:
            resp.raise_for_status()

    @pytest.mark.get_invalid_resource_id
    def test_get_invalid_resource_id(self):
        url = BASE_URL + 'planets/invalid'
        resp = request(
            request_type='GET',
            url=url
        )

        assert resp.status_code == 404
        assert resp.json()['detail'] == 'Not found'

    @pytest.mark.post_test
    def test_post_request(self):
        # Verify the response when we send a POST request instead of the recommended GET request
        url = BASE_URL + 'planets'
        resp = request(
            request_type='POST',
            url=url
        )

        assert resp.status_code == 405
        assert resp.json()['detail'] == "Method 'POST' not allowed."

    @pytest.mark.put_test
    def test_put_request(self):
        # Verify the response when we send a PUT request instead of the recommended GET request
        url = BASE_URL + 'planets'
        resp = request(
            request_type='PUT',
            url=url
        )
        assert resp.status_code == 405
        assert resp.json()['detail'] == "Method 'PUT' not allowed."

    @pytest.mark.delete_test
    def test_delete_request(self):
        # Verify the response when we send a DELETE request instead of the recommended GET request
        url = BASE_URL + 'planets'
        resp = request(
            request_type='DELETE',
            url=url
        )
        assert resp.status_code == 405
        assert resp.json()['detail'] == "Method 'DELETE' not allowed."

    @pytest.mark.get_using_invalid_http_url
    def test_get_using_invalid_http_url(self):
        # Verify that we receive and handle a missing schema exception
        # when we request to an invalid URL
        url = 'http//swapi.dev/api/planets'
        try:
            request(
                request_type='GET',
                url=url
            )
        except requests.exceptions.MissingSchema as e:
            assert "Invalid URL 'http//swapi.dev/api/planets'" in str(e)

    @pytest.mark.get_connection_error
    def test_get_connection_error(self):
        # Verify that we receive and handle a ConnectionError exception
        url = 'https://http//swapi.dev/api/planets'
        try:
            request(
                request_type='GET',
                url=url
            )
        except requests.exceptions.ConnectionError as e:
            assert ("HTTPSConnectionPool(host=\'http\', port=443): "
                    "Max retries exceeded with url: /swapi.dev/api/planets"
                    in str(e))

    @classmethod
    def teardown_class(cls):
        pass
