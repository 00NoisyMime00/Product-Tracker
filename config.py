from getpass import getpass
import json
import os.path
from os import path


if path.exists('credentials.json') == False:
    with open('credentials.json', 'w') as f:
        details = {}
        details['id'] = ""
        details['password'] = ""
        json.dump(details, f)


with open('credentials.json', 'r') as f:
    details = json.loads(f.read())
    id = details['id']
    password = details['password']
    

def change():
    id = input('Enter your Email ID, this email Id will be used to send you the updates: ')
    password = getpass()

    details={}
    details['id'] = id
    details['password'] = password

    with open('credentials.json', 'w') as f:
        json.dump(details, f)

    