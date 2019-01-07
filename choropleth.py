### choropleth.py

import csv
from bs4 import BeautifulSoup

CSV_PATH = 'inputs/data/unemployment09.csv'
MAP_PATH = 'inputs/map.svg'

# Read in unemployment data from CSV
unemployment = {}
reader = csv.reader(open(CSV_PATH), delimiter=",")
for row in reader:
	try:
		fips = int(row[1] + row[2]) # FIPS code = state + country (cols 2, 3)
		rate = float(row[8].strip()) # Unemployment rate (col 8)
		unemployment[fips] = rate
	except:
		pass

# Load the map & parse using BS4
map = open(MAP_PATH, 'r').read()
soup = BeautifulSoup(map, 'lxml')

# Isolate counties
counties = soup.findAll('path')

# Set map colors & style
colors = ["#edf8fb", "#bfd3e6", "#9ebcda", "#8c96c6", "#8856a7", "#810f7c"]
style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:0;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# Color map based on unemployment data
for c in counties:

	if c['id'] == "State_Lines":
		
		c['stroke'] = "#ffffff"
		c['stroke-width'] = ".25"
		
	elif c['id'] == "separator":
	
		c['stroke-width'] = ".25"
	
	else:

		try:
			fips = int(c['id'].split("_", 1)[1])
			rate = unemployment[fips]
		except:
			continue
		 
		if rate < 2:
			color_class = 0
		elif rate < 4:
			color_class = 1
		elif rate < 6:
			color_class = 2
		elif rate < 8:
			color_class = 3
		elif rate < 10:
			color_class = 4
		else:
			color_class = 5
		
		color = colors[color_class]
		c['style'] = style + color


# Output map
print(soup.prettify())