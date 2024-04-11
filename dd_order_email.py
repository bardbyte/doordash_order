# author: bardbyte
import base64
import argparse
import csv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from datetime import datetime
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
      # The file token.pickle stores the user's access and refresh tokens, and is
      # created automatically when the authorization flow completes for the first
      # time.
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the tokens for the next run
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def parse_email_message(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    
    # Decode the email body.
    part = message['payload']['parts'][0]['body']['data']
    msg_str = base64.urlsafe_b64decode(part.encode('ASCII'))
    
    # Find the total amount in the message string.
    pattern = re.compile(r"Total: \$\d+\.\d{2}")
    matches = pattern.findall(str(msg_str))
    total_amount = matches[0].split('Total: $')[-1] if matches else 'Total Not found'
    
    # Convert the 'internalDate' from timestamp in milliseconds to seconds and parse to datetime
    email_date_seconds = int(message['internalDate']) / 1000
    date = datetime.utcfromtimestamp(email_date_seconds).strftime('%Y-%m-%d %H:%M:%S')

    return date, total_amount

def main():
    parser = argparse.ArgumentParser(description='Fetch DoorDash order history.')
    parser.add_argument('--credentials', help='Path to the credentials JSON file.', required=True)
    parser.add_argument('--output', help='Path to the output CSV file.', required=True)
    
    args = parser.parse_args()
    # Set the OAuth 2.0 login
    service = get_service()

    # Call the Gmail API to fetch DoorDash emails
    query = 'from:no-reply@doordash.com subject:"Order Confirmation"'  # Adjust the query to match the actual sender
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    orders_info = []
    
    # Keep getting messages using the nextPageToken until there are no more to get
    while 'nextPageToken' in results:
        page_token = results['nextPageToken']
        results = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        messages.extend(results.get('messages', []))
    
    print(len(messages))

    for message in messages:
        date, total_cost = parse_email_message(service, message['id'])
        orders_info.append({'date': date, 'total_cost': total_cost})

    # Write the data to a CSV file
    output_file = args.output
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'total_cost'])
        writer.writeheader()
        writer.writerows(orders_info)

if __name__ == '__main__':
    main()
