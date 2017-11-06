from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
	"""
	Add Event Demo
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	# Refer to the Python quickstart on how to setup the environment:
	# https://developers.google.com/google-apps/calendar/quickstart/python
	# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
	# stored credentials.

	event = {
	  'summary': '這是summary',
	  'location': '某個地點',
	  'description': '敘述文字~\n敘述',
	  'start': {
		'dateTime': '2017-11-06T09:00:00+08:00',
		'timeZone': 'Asia/Taipei',
	  },
	  'end': {
		'dateTime': '2017-11-06T11:00:00+08:00',
		'timeZone': 'Asia/Taipei',
	  },
	  'recurrence': [
		
	  ],
	  'attendees': [
		
	  ],
	  'reminders': {
		'useDefault': False,
		'overrides': [
		],
	  },
	}
	
	# get calendarId
	page_token = None
	while True:
		calendar_list = service.calendarList().list(pageToken=page_token).execute()
		print(calendar_list)
		for calendar_list_entry in calendar_list['items']:
			print(calendar_list_entry['summary'])
		page_token = calendar_list.get('nextPageToken')
		if not page_token:
			break
	
	#event = service.events().insert(calendarId='9lersenlq2540oa28ntre3odmg@group.calendar.google.com', body=event).execute()
	#print(event)
	#print("Event created:{} ".format(event.get('htmlLink')))
	
	import DataParser
	for item in DataParser.getEvents():
		event = {
			'summary': item['country']+ "-" +item['title'],
			'description': '前值：{}\n預測：{}\n'.format(item['history'], item['prediction']),
			'start': {
			'dateTime': item['datetime'],
			'timeZone': 'Asia/Taipei',
		  },
		  'end': {
			'dateTime': item['datetime'],
			'timeZone': 'Asia/Taipei',
		  },
		}
		#print(event)
		#newEvent = service.events().insert(calendarId='9lersenlq2540oa28ntre3odmg@group.calendar.google.com', body=event).execute()
		#print(newEvent)
		

if __name__ == '__main__':
    main()
