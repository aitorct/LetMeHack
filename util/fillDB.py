from .. import scrapper

def fillDB():
	print("Scrapping data from MLH website...")
	events, dates, urls, city, country = scrapper.scrapData(scrapper.getWebsite())
	hackathonList = []

	print("Processing data...")
	for e in range(0, len(events)):
		hackathonList.append(scrapper.classes.hackathon(events[e], dates[e], urls[e], "{city}, {country}".format(city=city[e], country=country[e])))

	print("Generating DB...")
	db = {'hackathons': [], 'users': []}
	DBlist = db["hackathons"]

	for i in hackathonList:
		DBlist.append(i.name)

	print("Filling DB...")
	with open('letmehack/data/db.json', 'w+') as json_data:
		scrapper.json.dump(db, json_data)

	print("DONE! db.json created succesfully.")

try:
	open('letmehack/data/db.json', 'r')
except IOError:
	fillDB()
else:
	yes = set(['yes','y'])
	no = set(['no','n'])
	print("db.json already exists. Do you want to replace it? All DB data will be lost. [yes/no]")
	while True:
		choice = input().lower()
		if choice in yes:
		   fillDB()
		   exit(0)
		elif choice in no:
		   exit(0)
		else:
		   print("Please respond with either 'yes' or 'no'.")
