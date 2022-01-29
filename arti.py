import json
filename = 'luc_data.rdf'
dict1 = {}
s='a'
with open(filename) as fh:
	for line in fh:
		b,c,d = line.strip().split(None, 2)
		if(s!=b):
		    dict2={}
		s=b
		dict2[c]= d.strip()
		dict1[s]= dict2
out_file = open("test.json", "w")
json.dump(dict1, out_file)
out_file.close()