
import csv
from datetime import datetime
import logging
import argparse
import urllib.request

#initialize_logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

#argument_parsing_for_URL
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL of the CSV file", required=True)
args = parser.parse_args()
url = args.url

def downloadData(url):
    response = urllib.request.urlopen(url)
    long_txt = response.read().decode()
    return long_txt

def processData(csv_data):
    person_data = {}
    csv_reader = csv.reader(csv_data.splitlines())
    next(csv_reader) 
    for line_num, row in enumerate(csv_reader, 1):
        try:
            id, name, birthday = int(row[0]), row[1], datetime.strptime(row[2], '%d/%m/%Y')
            person_data[id] = (name, birthday)
        except Exception as e:
            logging.error(f"Error processing line #{line_num} for ID #{row[0]}: {e}")
    return person_data

def displayPerson(id, person_data):
    if id in person_data:
        name, birthday = person_data[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y%m%d')}")
    else:
        print("No user found with that id")

def main():
    try:
        csv_data = downloadData(url)
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    
    person_data = processData(csv_data)
    
    while True:
        user_input = input("Enter an ID to look up: ")
        try:
            id = int(user_input)
            if id <= 0:
                print("Exiting the program.")
                break
            displayPerson(id, person_data)
        except ValueError:
            print("Please enter a valid integer ID.")

if __name__ == "__main__":
    main()
