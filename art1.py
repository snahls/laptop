import json


filename = './sravya.rdf'
dict1 = {}
s = 'a'
t='a'
from collections import defaultdict,OrderedDict
dl = defaultdict(list)

with open(filename) as fh:

	for line in fh:
		b,c,d = line.strip().split(None, 2)
		if(s!=b):
			dict2 = {}
			dl= defaultdict(list)

		s=b
		dict2[c] = d.strip()
		for k,v in dict2.items():
			# dl.setdefault(k,[]).append(v)
			if k in dl.keys():
				dl[k].append( list(OrderedDict.fromkeys(v)))				
			else:
				dl[k]=[v]
		
		print(dl)
		dict1[s] = dl
	
# print(dict1)
rdf1 = dict1
# print(rdf1)
out_file = open("final_thr_code_check.json", "w")
json.dump(dict1, out_file)
out_file.close()