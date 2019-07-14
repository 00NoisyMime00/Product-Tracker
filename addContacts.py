import os.path
from os import path


def addingContacts(addNew = False):
    if path.exists('contacts.txt') == False or addNew == True:
        with open('contacts.txt', 'a') as f:
            contacts = []
            while True:
                name = input('Enter new name, this is the name of the person recieving all the updates: ').strip()
                email = input('Enter Email ID: ').strip()
                contacts.append(name+" "+email+'\n')
                flag = input('want to enter more? y/n: ').lower()
                if flag == 'n':
                    break
            for contact in contacts:
                f.write(contact)

addingContacts()