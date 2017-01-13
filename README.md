# LetMeHack

Scrap MLH website to get new listed hackathons and send users a notification through Twitter DM.

## Prerequisites

All requirements are packed in the file requirements.txt. Just run the following command to install all needed libraries.

    pip3 install -r letmehack/requirements.txt

## First run

Before running the program for the first time, you'll need to get all listed hackathons and fill your database with it.

    python3 letmehack.util.fillDB


## Usage

    python3 -m letmehack.scrapper

## Built with

* [lxml](https://github.com/lxml/lxml) - Used for scrapping
* [requests](https://github.com/kennethreitz/requests) - HTTP requests

## Authors

* **Aitor Cubeles** - *Initial work* - [aitorct](https://github.com/aitorct)