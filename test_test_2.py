import pytest
import csv
import requests
import requests_mock
from test_2 import get_data_from_csv, process_csv_row, get_nearest_relevant_court, generate_output, get_list_of_relevant_courts, get_nearest_court_from_list, get_court_list_from_api
import json
from unittest.mock import patch


# The following tests are for get_data_from_csv():

def test_get_data_from_csv_returns_list_of_dicts():
    """
    Checks that the function, when given a valid input,
    returns a list of dictionaries
    """
    result = get_data_from_csv("people.csv")

    assert isinstance(result, list)
    
    for item in result:
        assert isinstance(item, dict)


def test_get_data_correctly_retrieves_data_from_people_csv_file():
    """
    Tests that the data returned by the function
    matches the data in people.csv
    """
    result = get_data_from_csv("people.csv")

    expected_result = [{'name': 'Iriquois Pliskin', 'postcode': 'SE17TP', 'court_type': 'Crown Court'}, 
                       {'name': 'Robert Loggia', 'postcode': 'NP108XG', 'court_type': 'Crown Court'}, 
                       {'name': 'Alexander Hamilton', 'postcode': 'HA13HP', 'court_type': 'County Court'}, 
                       {'name': 'Linus Torvalds', 'postcode': 'WC2R0BL', 'court_type': 'County Court'}, 
                       {'name': 'Miles Meraki', 'postcode': 'EC2A1AF', 'court_type': 'Tribunal'}, 
                       {'name': 'George Canning', 'postcode': 'SW1A2AA', 'court_type': 'Tribunal'}, 
                       {'name': 'Seymour Skinner', 'postcode': 'SW1A1AA', 'court_type': 'Tribunal'}, 
                       {'name': 'Yuri Gagarin', 'postcode': 'SN21SZ', 'court_type': 'Crown Court'}, 
                       {'name': 'Hideo Kojima', 'postcode': 'EH88AS', 'court_type': 'Tribunal'}, 
                       {'name': 'Guido Van Rossum', 'postcode': 'NR162HE', 'court_type': 'County Court'}]

    assert result == expected_result


# The following tests are for process_csv_row():

def test_process_csv_row_returns_dict():
    """
    Tests that, if given a valid list, the function returns a dict
    """
    result = process_csv_row(['Iriquois Pliskin', 'SE17TP', 'Crown Court'])

    assert isinstance(result, dict)


def test_process_csv_row_returns_dict_with_required_fields():
    """
    Tests that a person's data dictionary has
    the required keys
    """
    result = process_csv_row(['Iriquois Pliskin', 'SE17TP', 'Crown Court'])

    assert 'name' in result
    assert 'postcode' in result
    assert 'court_type' in result


def test_process_csv_row_processes_list_correctly():
    """
    Tests that the right values are assigned 
    to the right keys
    """
    result = process_csv_row(['Iriquois Pliskin', 'SE17TP', 'Crown Court'])

    assert result['name'] == 'Iriquois Pliskin'
    assert result['postcode'] == 'SE17TP'
    assert result['court_type'] == 'Crown Court'


def test_process_csv_row_returns_dict_with_no_extra_fields():
    """
    Tests that the returned dictionaries
    are of uniform length, without extra keys
    """
    result = process_csv_row(['Iriquois Pliskin', 'SE17TP', 'Crown Court'])

    required_keys = ['name', 'postcode', 'court_type']

    extra_keys = [key for key in result if key not in required_keys]

    assert len(extra_keys) == 0


def test_process_csv_row_skips_row_if_index_error():
    """
    Nothing will be returned if an IndexError
    is encountered
    """
    result = process_csv_row(['Iriquois Pliskin', 'SE17TP'])

    assert result == None


# The following tests are for get_nearest_relevant_court():

def test_get_nearest_relevant_court_returns_dict():
    """
    Tests that the function returns a dictionary
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    result = get_nearest_relevant_court("Tribunal", court_list)

    assert isinstance(result, dict)


def test_get_nearest_relevant_court():
    """
    Tests that the function correctly identifies
    the nearest court of the correct type
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    result = get_nearest_relevant_court("Tribunal", court_list)

    assert result['name'] == 'Norwich Social Security and Child Support Tribunal'


# The following tests are for get_court_list_from_api():

def test_get_court_list_from_api():
    """
    Tests that the function retrieves a list of dictionaries,
    where each dictionary holds information about a specific
    court
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    postcode = "NR162HE"

    with requests_mock.Mocker() as m:

        m.get(f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}", json=court_list)

        result = get_court_list_from_api(postcode)

    expected_result = court_list

    assert result == expected_result

    assert m.call_count == 1


# The following tests are for get_list_of_relevant_courts():

def test_get_list_of_relevant_courts_returns_list_of_dicts():
    """
    Tests that the function returns a list of dictionaries
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    relevant_courts = get_list_of_relevant_courts(court_list, "Tribunal")

    assert isinstance(relevant_courts, list)

    for court in relevant_courts:

        assert isinstance(court, dict)


def test_get_list_of_relevant_courts_correctly_filters_by_desired_court_type():
    """
    Tests that the result contains only the desired
    type of court
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    relevant_courts = get_list_of_relevant_courts(court_list, "Tribunal")

    for court in relevant_courts:

        assert "Tribunal" in court['types']


# The following tests are for get_nearest_court_from_list():

def test_get_nearest_court_from_list_returns_dict():
    """
    Tests that the result is a dictionary
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    relevant_courts = get_list_of_relevant_courts(court_list, "Tribunal")

    closest_relevant_court = get_nearest_court_from_list(relevant_courts)

    assert isinstance(closest_relevant_court, dict)


def test_get_nearest_court_correctly_identifies_nearest_court():
    """
    Tests that the result has the shortest distance out
    of the given list of courts
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    relevant_courts = get_list_of_relevant_courts(court_list, "Tribunal")

    distances = []

    for court in relevant_courts:

        if court['distance']:

            distances.append(float(court['distance']))
    
    shortest_distance = min(distances)

    closest_relevant_court = get_nearest_court_from_list(relevant_courts)

    assert shortest_distance == float(closest_relevant_court['distance'])


# The following tests are for generate_output():

def test_generate_output_returns_string():
    """
    Tests that the result is a string
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    with patch("test_2.get_court_list_from_api", return_value=court_list):

        result = generate_output({'name': 'Guido Van Rossum', 'postcode': 'NR162HE', 'court_type': 'Tribunal'})

    assert isinstance(result, str)


def test_generate_output_returns_correct_output():
    """
    Tests that the result contains the correct
    and required information
    """
    with open("test_data_challenge_2.txt", 'r') as file:
        court_list = json.load(file)

    with patch("test_2.get_court_list_from_api", return_value=court_list):

        result = generate_output({'name': 'Guido Van Rossum', 'postcode': 'NR162HE', 'court_type': 'Tribunal'})

    assert "16.66 miles" in result
    assert "Guido Van Rossum" in result
    assert "Norwich Social Security and Child Support Tribunal" in result
    assert "Tribunal" in result
    assert "NR162HE" in result
