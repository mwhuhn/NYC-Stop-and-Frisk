#!/usr/bin/env python

# filename: acsAPI-json.py
# purpose: get 5-year ACS data from API, save as csv

# import
import requests
import csv
from StringIO import StringIO
import json

# set up request
key = "" # ADD HERE
state = "36"
counties = ["005", "047", "061", "081", "085"]
years = ["2015"]
variables = ["B01001_001E","B01001_002E","B01002_001E","B02001_003E",
			 "B02009_001E","B02001_002E","B03003_003E","B20002_001E",
			 "B15003_001E","B15003_002E","B15003_003E","B15003_004E",
			 "B15003_005E","B15003_006E","B15003_007E","B15003_008E",
			 "B15003_009E","B15003_010E","B15003_011E","B15003_012E",
			 "B15003_013E","B15003_014E","B15003_015E","B15003_016E",
			 "B17021_019E"]
fileprefix = "../data/acs"

for year in years: # for multiple years
	urls=[]
	# generate urls for each county
	for county in counties:
		if year == "2015": # different url for 2015
			url = "https://api.census.gov/data/{}/acs/acs5?get=".format(year) + ",".join(variables) + "&for=block%20group:*&in=state:{}%20county:{}&key={}".format(state,county,key)
		else:
			url = "https://api.census.gov/data/{}/acs5?get=".format(year) + ",".join(variables) + "&for=block%20group:*&in=state:{}%20county:{}&key={}".format(state,county,key)
		urls.append(url)
	# run request
	with open(fileprefix + year +"-json.csv","w") as f:
		wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		for i in range(len(urls)):
			response = requests.get(urls[i]).text
			jsonReader = json.loads(response)
			j = 0
			for line in jsonReader:
				if i != 0 and j == 0: # skip header after first county
					j += 1
				else:
					wr.writerow(line)

