import json
import oauth2 as oauth
from urllib.parse import quote


def generateMessage(event):
	return "\n{name} in {location}. {date}.\nMore info in our Twitter\n".format(name=event.name, 
																				location=event.location, 
																				date=event.date)


def sendDM(message):
	with open('letmehack/data/keys.json') as json_data:
		jsonData = json.load(json_data)
		keys = jsonData["keys"]

	consumer = oauth.Consumer(key=keys["consumer_key"], secret=keys["consumer_secret"])
	access_token = oauth.Token(key=keys["access_token"], secret=keys["access_token_secret"])
	client = oauth.Client(consumer, access_token)

	with open('letmehack/data/db.json') as json_data:
		db = json.load(json_data)

	for user in db["users"]:
		endpoint = "https://api.twitter.com/1.1/direct_messages/new.json?text="+message+"&screen_name="+user
		print("Notification sent to "+user)
		response, data = client.request(endpoint, method = "POST")


def notify(eventList):
	if len(eventList) == 1:
		message = "NEW HACKATHON!\n" + generateMessage(eventList[0])
	else:
		nEvents = len(eventList)
		message = "{number} NEW HACKATHONS!\n".format(number=nEvents)
		for i in range(0, nEvents):
			message += generateMessage(eventList[i])

	sendDM(quote(message))