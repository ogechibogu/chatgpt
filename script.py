import requests
import os
import json

FRESH_SERVICE_DOMAIN = "sendkobo.freshservice.com"
API_ENDPOINT = 'https://sendkobo.freshservice.com/api/v2/tickets/filter?query="tag:adobe"'

API_KEY = os.environ.get('API_KEY')
headers = {'Content-Type': 'application/json'}

response = requests.get(API_ENDPOINT, auth=(API_KEY, 'X'))
tickets = json.loads(response.text)['tickets']
ticket_ids = [ticket['id'] for ticket in tickets]




approved_tickets = []

for ticket_id in ticket_ids:
    end_point = f"https://{FRESH_SERVICE_DOMAIN}/api/v2/tickets/{ticket_id}"
    activity_response = requests.get(end_point, auth=(API_KEY, 'X'))
    try:
        approval_status = json.loads(activity_response.text)['ticket']['approval_status']
        print(approval_status)
        if approval_status == 1:
            approved_tickets.append(ticket_id)
            print(f'The approved tickect number is: {approved_tickets}')
    except KeyError:
        print(f"No approval status found for ticket {ticket_id}")


for approved in approved_tickets:
    approved_end_point = f"https://{FRESH_SERVICE_DOMAIN}/api/v2/tickets/{approved}?include=requester"
    approved_response = requests.get(approved_end_point, auth=(API_KEY, 'X'))
    response_dict = json.loads(approved_response.text)
    requester_name = response_dict['ticket']['requester']['name']
    requester_email = response_dict['ticket']['requester']['email']
    requester_login = response_dict['ticket']['custom_fields']['login']
    requester_key = response_dict['ticket']['custom_fields']['rsa']
    print(requester_name)
    print(requester_email)
    print(requester_login)
    print(requester_key)

