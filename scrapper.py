import time
import json
import requests
from letmehack import classes 
from letmehack import notifier
from lxml import html

sleepTime = 1800

def getWebsite():
	try:
		response = requests.get('https://mlh.io/seasons/eu-2017/events')
		if not response.status_code == 200:
			return "Error: couldn't get data from server"
		return html.fromstring(response.content)

	except requests.exceptions.RequestException as e:
		return "Fatal error: {}".format(e)


def scrapData(website):
	events = website.xpath("//div[@class='event-wrapper']/a/div/h3/text()") 
	dates = website.xpath("//div[@class='event-wrapper']/a/div/p[1]/text()") 
	urls = website.xpath("//div[@class='event-wrapper']/a/@href") 
	city = website.xpath("//div[@class='event-wrapper']/a/div/div[@itemprop='address']/span[1]/text()") 
	country = website.xpath("//div[@class='event-wrapper']/a/div/div[@itemprop='address']/span[2]/text()")

	return events, dates, urls, city, country


def compare(events):
	with open('letmehack/data/db.json') as json_data:
		db = json.load(json_data)

	update = set(events) - set(db["hackathons"])

	index = []
	if update:
		for i in update:
			index.append(events.index(i))

	return index


def addToDB(hackathonList):
	with open('letmehack/data/db.json', 'r') as json_data:
			db = json.load(json_data)
	
	DBlist = db["hackathons"]
	for i in hackathonList:
		DBlist.append(i.name)
		
	with open('letmehack/data/db.json', 'w') as json_data:
		json.dump(db, json_data)


if __name__ == "__main__":
	while True:
		starttime=time.time()
		
		events, dates, urls, city, country = scrapData(getWebsite())
		updateIndex = compare(events)
		if updateIndex:
			hackathonList = []
			for e in range(0, len(updateIndex)):
				hackathonList.append(classes.hackathon(events[updateIndex[e]], dates[updateIndex[e]], urls[updateIndex[e]], "{city}, {country}".format(city=city[updateIndex[e]], country=country[updateIndex[e]])))
			notifier.notify(hackathonList)
			addToDB(hackathonList)

		processingTime = time.time() - starttime
		finalSleep = sleepTime - processingTime
		if finalSleep > 0:
			print("Sleeping for {time} seconds".format(time=finalSleep))
			time.sleep(finalSleep)
		else:
			print("YOLO: No time to sleep.")