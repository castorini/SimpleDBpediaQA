import re
import sys
import json
import urllib
import multiprocessing
from joblib import Parallel, delayed
from SPARQLWrapper import SPARQLWrapper, JSON


# encodes the subject with url enconder from urllib.
def make_subject(subject):
	subject_page = subject.split("http://dbpedia.org/resource/")[1]
	subject_encoded = urllib.parse.quote(subject_page)
	subject_url = "http://dbpedia.org/resource/" + subject_encoded
	return subject_url


def processInput(item):
# finds the redirects list for each subject.
	redirected_pages = []
	redirected_pages.append(item["Subject"])
	subject = item["Subject"]

	# if there is (") in the subject, fix it with urlencoder. This is the only case that needs urlencode.
	if ('"' in subject):
		subject = make_subject(subject)

	q = "SELECT" + " *" + " {" + " ?redirects"  + " <http://dbpedia.org/ontology/wikiPageRedirects> <{}> ".format(subject) + "}"
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(q)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()


	for result in results["results"]["bindings"]:
		redirected_pages.append(result["redirects"]["value"])

	# query must be forward
	if (len(redirected_pages) == 1):
		q = "SELECT" + " *" + " {" + " <{}>".format(subject) + " <http://dbpedia.org/ontology/wikiPageRedirects> ?redirects }"
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery(q)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		for result in results["results"]["bindings"]:
			redirected_pages.append(result["redirects"]["value"])


	item["Subject"] = redirected_pages
	
	# finds objects for each subject and predicate.
	predicateList = item["PredicateList"]
	objectList = []

	for subject in item["Subject"]:
		if ('"' in subject):
			subject = make_subject(subject)
		for pr in predicateList:
			direction = pr["Direction"]
			constraint = pr["Constraint"]
			predicate = pr["Predicate"]
			if (direction == "backward"):
				if (constraint == None):
					q = "SELECT" + " *" + " {" + " ?object" + " <{}> <{}>".format(predicate, subject) + " }"
				else:
					q = "SELECT" + " *" + " {" + " ?object" + " <{}> <{}>".format(predicate, subject) + " ." + " ?object" + " <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}>".format(constraint) + " ." + " }"

			if (direction == "forward"):
				if (constraint == None):
					q = "SELECT" + " *" + " {"  + " <{}> <{}>".format(subject, predicate) + " ?object" + " }" 
				else:
					q = "SELECT" + " *" + " {" + " <{}> <{}>".format(subject, predicate) + " ?object" + " ." + " ?object" + " <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}>".format(constraint) + " ." + " }"

			try:
				sparql = SPARQLWrapper("http://dbpedia.org/sparql")
				sparql.setQuery(q)
				sparql.setReturnFormat(JSON)
				results1 = sparql.query().convert()
				objects = []

				for result in results1["results"]["bindings"]:
					objects.append(result["object"]["value"])
				
				if len(objects) > 0:
					objectList.append(
						{
						"Objects": objects,
						"Subject": subject,
						"Predicate": predicate
						})
			
			except:
				print("Query has an error!\t" + subject + "\t" + predicate)


	if len(objectList) > 0:
		item["ObjectList"] = objectList
	else:
		print("No Objects Found! \t" + item["Query"])
		item["ObjectList"] = objectList
		# sets (ObjectList = []) for queries that have no objects.

	return item


def main():

	input_file = sys.argv[1]
	with open(input_file) as file:
		data = json.load(file)

	num_cores = multiprocessing.cpu_count()
		
	results = Parallel(n_jobs=num_cores)(delayed(processInput)(item) for item in data["Questions"])

	data["Questions"] = results

	with open('output.json', 'w') as outfile:
		outfile.write(json.dumps(data, indent=4, sort_keys=True))
	  
	outfile.close()


if __name__ == "__main__":
	main()