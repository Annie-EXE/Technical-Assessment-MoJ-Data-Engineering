import csv
import requests
import json

# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type

def get_data_from_csv(file_path: str) -> list:
    """
    Reads from a csv file and, for each row, creates a dictionary
    of the data (assuming the csv fields are name, postcode, and court type),
    and creates a list of each person's data
    """
    with open(file_path, 'r', newline='') as csvfile:

        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)

        people_data = []

        for row in csv_reader:

            data = process_csv_row(row)

            if data is not None:

                people_data.append(data)
            
        return people_data


def process_csv_row(row: list) -> dict:
    """
    Processes each row of a CSV file, returning a dictionary
    of the data
    """

    try:

        data = {
            'name': row[0],
            'postcode': row[1],
            'court_type': row[2]
        }

        return data
    
    except IndexError:

        print("Skipped invalid row: {row}")


def get_nearest_relevant_court(court_type: str, court_list_data: list) -> dict:
    """
    Returns information on the relevant nearest court, given a
    postcode and court type. Presents information in a user-friendly way.
    """
    court_type = court_type.title()

    relevant_courts = get_list_of_relevant_courts(court_list_data, court_type)

    closest_relevant_court = get_nearest_court_from_list(relevant_courts)

    return closest_relevant_court


def get_court_list_from_API(postcode: str) -> list[dict]:

    response = requests.get(f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}")
    court_list_data = response.json()
    return court_list_data


def get_list_of_relevant_courts(court_list: list, court_type) -> list[dict]:

    relevant_courts = []

    for court in court_list:

        if court_type in court["types"]:

            relevant_courts.append(court)

    return relevant_courts


def get_nearest_court_from_list(court_list: list) -> dict:

    closest_court = min(court_list, key=lambda x: x["distance"])

    return closest_court


def generate_output(person_data: dict) -> str:
    """
    Takes a dictionary storing one person's data
    Identifies their nearest court of the right type
    Prints the information in a readable way to the console
    """
    court_list_data = get_court_list_from_API(person_data['postcode'])

    closest_relevant_court = get_nearest_relevant_court(person_data['court_type'], court_list_data)

    court_name = closest_relevant_court['name']
    if closest_relevant_court['dx_number']:
        dx_number = closest_relevant_court['dx_number']
    else:
        dx_number = None
    distance = closest_relevant_court['distance']

    person_name = person_data['name']
    court_type = person_data['court_type']
    postcode = person_data['postcode']
    

    output_string = f"""\n{person_name}, the nearest {court_type} to your postcode ({postcode})
        is {court_name} ({distance} miles away). \n\n"""
    
    if dx_number:
        output_string += f"""The dx_number of this court is {dx_number}. \n\n"""
    
    output_string += "--------------------------------- \n"

    return output_string


if __name__ == "__main__": #pragma: no cover

    people_data = get_data_from_csv("people.csv")
    
    for person_data in people_data:
        print(person_data)
        print(generate_output(person_data))
