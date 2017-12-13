#!/usr/bin/env python2.7
import os
import string
from os import listdir
from os.path import basename, isdir, isfile, join
import re
import cgi
import sys
import cgitb
cgitb.enable()

AND = "AND"
OR = "OR"
index_file = "/usr/local/bin/html_index.txt"
stop_file = "/usr/local/bin/stopwords.txt"

def parseTerms(terms):
	found = []
	buf = ""
	inquote = 0
	terms = terms.strip()

	for c in terms:
		if c == "\"":
			if inquote == 0:
				inquote = 1
			else:
				inquote = 0
				found.append(buf)
				buf = ""
			continue
		if c.isspace():
			if inquote == 0:
				if len(buf) > 0:
					found.append(buf)
					buf = ""
				continue
 		buf += c

	if len(buf) > 0:
		found.append(buf)
	if inquote:
		raise NameError, 'Too many quotes'

	stop_words = []
	with open(stop_file) as file:
		for line in file:
			stop_words.append(line.strip())
	found = list(set(found) - set(stop_words))
	return found

def search(terms, searchtype, index):
	found = []

	if index:
		for file in index:
			items = file.split(",")
			path = items.pop(0)
			if searchtype == "AND":
				if andSearch(terms, items):
					found.append(getPath(path))
			else:
				if orSearch(terms, items):
					found.append(getPath(path))
	return found

def orSearch(a, b):
	return not set(a).isdisjoint(set(b))

def andSearch(a, b):
	return set(a).issubset(set(b))

def getPath(path):
	new = path.replace("/usr/local/apache2/htdocs/", "")
	return new

def doresultspageempty():
	for line in open("SearchResults.html", 'r'):
		if line.find("${SEARCH_RESULTS_GO_HERE}") != -1:
			print line.replace("${SEARCH_RESULTS_GO_HERE}", "")
		elif line.find("${SEARCH_TERMS_GO_HERE}") != -1:
			print line.replace("You searched for: ${SEARCH_TERMS_GO_HERE}", "No Search Terms Were Entered")	
		else:
			print line		

def doresultspage(terms = [], results = []):
	for line in open("SearchResults.html", 'r'):
		if line.find("${SEARCH_RESULTS_GO_HERE}") != -1:
			doresults(terms, results)
		elif line.find("${SEARCH_TERMS_GO_HERE}") != -1:
			termindex = line.find("${SEARCH_TERMS_GO_HERE}")
			searchterms = "<span id=\"search_terms\">" + terms + "</span>\n"
			print line.replace("${SEARCH_TERMS_GO_HERE}", searchterms)	
		else:
			print line

def doresults(terms = [], results = []):
	print "<div id=\"search_results\">\n<ol>"
	if len(results) == 0:
		print "<h3>Your search did not return any results.</h3>"
	for i, file in enumeratez(results):
		print "<li><a href=/" + results[i] + "?search=true&term=" + terms.replace("\"", "%22") + "\">"
		print results[i] + "</a>\n"
	print "</ol>\n</div>\n"

def enumeratez(seq):
	i = 0
	result = []
	for elem in seq:
		t = i, elem
		result.append(t)
		i += 1
	return result

print "Content-type: text/html\n\n"
print ""
print "<html>"
form = cgi.FieldStorage()
results = []
terms = ""
index = []

try:
	if form.has_key("keywords"):
		terms = parseTerms(form.getvalue("keywords").lower())
		if terms:
			with open(index_file) as file:
				for line in file:
					index.append(line.strip())
			results = search(terms, "AND", index)
		doresultspage(" ".join(terms), results)
	else:
		doresultspageempty()
except NameError:
	print "There was an error understanding your search request.  Please press the back button and try again."
except:
	print "Really Unexpected error:", sys.exc_info()[0]

print "</html>"
