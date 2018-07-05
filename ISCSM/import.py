import csv

def Import_DB(file):
	lst=[]
	with open (file) as f:
		reader=csv.DictReader(f)
		for row in reader:
			lst.append(row)
	return lst
