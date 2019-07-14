import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import id, password, change
import json

from addContacts import addingContacts




if id == '' or password == '':
    change()

    with open('credentials.json', 'r') as f:
        details = json.loads(f.read())
        id = details['id']
        password = details['password']

MY_ADDRESS = id
PASSWORD = password


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    addingContacts()

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main(productName, price, websiteName, url):
    names, emails = get_contacts('contacts.txt') # read contacts
    message_template = read_template('EmailTemplate.txt')

    # set up the SMTP server
    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    # s.starttls()
    s.login(id, password)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name, PRODUCT_NAME=productName, PRODUCT_PRICE=str(price), WEBSITE_NAME=websiteName, LINK=url)
        
        # Prints out the message body for our sake
        # print(message)

        # setup the parameters of the message
        msg['From']=id
        msg['To']=email
        msg['Subject']="Reduced price for you, master."
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
# if __name__ == '__main__':
#     main()