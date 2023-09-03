import csv

with open("./csv/infile/waresitat_kraftklub.csv","rb") as row:
	for cell in row:
		cell = cell.split(",")
		print cell
		