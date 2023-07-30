import csv
import requests
import json


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

        return


def get_nearest_relevant_court(court_type: str, court_list_data: list) -> dict:
    """
    Returns information on the relevant nearest court, given a
    a list of courts and a desired court type
    """
    court_type = court_type.title()

    relevant_courts = get_list_of_relevant_courts(court_list_data, court_type)

    closest_relevant_court = get_nearest_court_from_list(relevant_courts)

    return closest_relevant_court


def get_court_list_from_api(postcode: str) -> list[dict]:
    """
    Connects to the API, supplies the postcode, and retrieves
    the ten nearest courts
    Returns this data in JSON format
    """
    response = requests.get(f"https://courttribunalfinder.service.gov.uk/search/results.json?postcode={postcode}")
    court_list_data = response.json()
    return court_list_data


def get_list_of_relevant_courts(court_list: list, court_type) -> list[dict]:
    """
    Filters a list of courts
    Returns a list of courts which are all of the 
    requested type
    """
    relevant_courts = []

    for court in court_list:

        if court_type in court["types"]:

            relevant_courts.append(court)

    return relevant_courts


def get_nearest_court_from_list(court_list: list) -> dict:
    """
    Sorts a list of courts (each of which is
    represented as a dictionary) by distance
    """
    closest_court = min(court_list, key=lambda x: x["distance"])

    return closest_court


def generate_output(person_data: dict) -> str:
    """
    Takes a dictionary storing one person's data
    Identifies their nearest court of the right type
    Prints the information in a readable way to the console
    """
    court_list_data = get_court_list_from_api(person_data['postcode'])

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
