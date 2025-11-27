#!/usr/bin/python

import requests
import sys

from urllib import parse
from re import sub, search
from lxml import html

# PROCESS COMMAND-LINE SETTINGS
if "--target-file" in sys.argv:
	try:
		target_file = sys.argv[sys.argv.index("--target-file") + 1]
	except:
		print("Invalid target file specified. Defaulting to targets.txt")
		target_file = "targets.txt"
else:
	target_file = "targets.txt"

if "--dynamic-directories" in sys.argv:
	try:
		dynamic_directories_file = sys.argv[sys.argv.index("--dynamic-directories")+1]
	except:
		print("Invalid dynamic directories specified. Defaulting to dynamic_directories.txt")
		dynamic_directories_file = "dynamic_directories.txt"
else:
	dynamic_directories_file = "dynamic_directories.txt"

if "--dynamic-files" in sys.argv:
	try:
		dynamic_files_file = sys.argv[sys.argv.index("--dynamic-files")+1]
	except:
		print("Invalid dynamic files specified. Defaulting to dynamic_files.txt")
		dynamic_files_file = "dynamic_files.txt"
else:
	dynamic_files_file = "dynamic_files.txt"

if "--dynamic-file-extensions" in sys.argv:
	try:
		dynamic_file_extentions_file = sys.argv[sys.argv.index("--dynamic-file-extensions")+1]
	except:
		print("Invalid dynamic file extensions specified. Defaulting to dynamic_file_extensions.txt")
		dynamic_file_extensions_file = "dynamic_file_extensions.txt"
else:
	dynamic_file_extensions_file = "dynamic_file_extensions.txt"

if "--static-files" in sys.argv:
	try:
		static_files_file = sys.argv[sys.argv.index("--static-files")+1]
	except:
		print("Invalid static files specified. Defaulting to static_files.txt")
		static_files_file = "static_files.txt"
else:
	static_files_file = "static_files.txt"

if "--deny-cookies" in sys.argv:
	use_cookies = False
else:
	use_cookies = True

if "--xpath" in sys.argv:
	try:
		xpath = sys.argv[sys.argv.index("--xpath")+1]
	except:
		xpath = False
else:
	xpath = False

if "--regex" in sys.argv:
	try:
		regex = sys.argv[sys.argv.index("--regex")+1]
	except:
		regex = False
else:
	regex = False

if "--status-code" in sys.argv:
	try:
		status_code = int(sys.argv[sys.argv.index("--status-code")+1])
	except:
		status_code = 0
else:
	status_code = 0

if "--output" in sys.argv:
	try:
		output_file = sys.argv[sys.argv.index("--output")+1]
	except:
		output_file = "dir_buster_output.txt"
else:
	output_file = "dir_buster_output.txt"

# FUNCTION DEFINITIONS

# read from the supplied filename, and return an array of the line-by-line contents of the file
# newlines stripped out
def readFileLines(filename):

	try:
		handler = open(filename, "r")
	except FileNotFoundError:
		print("Could not open file " + filename)
		sys.exit(1)

	completed_file_lines = []
	file_lines = handler.readlines()
	handler.close()

	for index in range(0, len(file_lines)):
		completed_file_line = file_lines[index].strip()
		if completed_file_line:
			completed_file_lines.append(completed_file_line)

	return completed_file_lines

# given a list of lines from the targets file, use a regular expression to strip out everything in the file
# that is not the URL
# at the same time, this function also strips out any redundancies of URLs that have the same path
# even if the parameters are different
def parseUrlLines(lines):

	new_lines = []

	for line in lines:

		new_line = sub("^(GET|POST)\\s", "", line)
		if not new_line:
			continue

		parsed_url = parse.urlparse(new_line)
		complete_url_and_path = parsed_url.scheme + "://" + parsed_url.hostname + parsed_url.path

		if complete_url_and_path not in new_lines:
			new_lines.append(complete_url_and_path)

	return new_lines

# strip redundant elements from the supplied array
# and return a new array with such redundancies removed
def stripRedundancies(array):

	new_array = []

	for item in array:
		if item not in new_array:
			new_array.append(item)

	return new_array

# given an array, strip all null elements
def stripNulls(array):

	new_array = []

	for item in array:
		if item:
			new_array.append(item)

	return new_array

# given a list of items (namely, words), this function will return an array consisting of each
# supplied word in three variations:
# (1) the word, being entirely lowercase,
# (2) the word, being entirely capitalized, and
# (3) the first character being uppercase, and the rest being lowercase
def generateDynamicList(words):

	completed_words = []

	for word in words:

		lowercase_word = word.lower()
		uppercase_word = word.upper()

		if len(word) > 1:
			hybrid_word = word[0].upper() + word[1:].lower()
		else:
			hybrid_word = False

		if lowercase_word not in completed_words:
			completed_words.append(lowercase_word)

		if uppercase_word not in completed_words:
			completed_words.append(uppercase_word)

		if hybrid_word != False and hybrid_word not in completed_words:
			completed_words.append(hybrid_word)

	return completed_words

# Given two supplied lists (the first being an array of URL nodes, and the second being an array of words)
# this function will return a new array of URLs,
# with each node in the URL path being replaced with all the items in the array of supplied words
def generateUrlList(scheme, host, nodes, words):

	base_url = scheme + "://" + host + "/"
	new_urls = []

	# we will consturct URLs based on the inner nodes
	for node_index in range(0, len(nodes)+1):

		for word in words:

			# we will construct a string, consisting of the entire node path up until this point
			prior_path = ""
			for previous_nodes_index in range(0, node_index):
				prior_path += nodes[previous_nodes_index] + "/"

			new_urls.append(base_url + prior_path + word)

	return new_urls


# READ FILE CONTENTS

target_urls = parseUrlLines(readFileLines(target_file))

dynamic_file_extensions = stripRedundancies(readFileLines(dynamic_file_extensions_file))
static_files = stripRedundancies(readFileLines(static_files_file))

dynamic_directories = generateDynamicList(stripRedundancies(readFileLines(dynamic_directories_file)))
dynamic_files = generateDynamicList(stripRedundancies(readFileLines(dynamic_files_file)))


# AND NOW WE CAN BEGIN GENERATING URLs

all_urls = []

for target_url in target_urls:

	parsed_url = parse.urlparse(target_url)
	nodes = stripNulls(parsed_url.path.split("/"))

	# let us arbitrarily begin by generating the static files
	all_urls += generateUrlList(parsed_url.scheme, parsed_url.hostname, nodes, static_files)

	# and now let us generate the dynamic files
	dynamic_files_with_extensions = []
	for dynamic_file in dynamic_files:
		for dynamic_file_extension in dynamic_file_extensions:
			dynamic_files_with_extensions.append(dynamic_file + dynamic_file_extension)

	all_urls += generateUrlList(parsed_url.scheme, parsed_url.hostname, nodes, dynamic_files + dynamic_files_with_extensions)


	# and finally, the dynamic directories
	all_urls += generateUrlList(parsed_url.scheme, parsed_url.hostname, nodes, dynamic_directories)

all_urls = stripRedundancies(all_urls)

# CONSTRUCT THE REQUEST OBJECT

user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
session = requests.session()
session.headers.update({"User-Agent":user_agent})

# AND NOW WE CAN BEGIN VISITING THE URLs

matching_urls = []

num_of_urls = len(all_urls)
current_url_number = 1
print(str(num_of_urls) + " URLs found. Making HTTP requests...")

for target_url in all_urls:

	sys.stdout.write(f"\rVisiting URL {current_url_number}")
	sys.stdout.flush()
	current_url_number += 1

	parsed_url = parse.urlparse(target_url)
	session.headers.update({"Host":parsed_url.hostname})

	if not use_cookies:
		sessions.cookies.clear()

	try:
		http_response = session.get(target_url, timeout=5)
	except:
		# HTTP timeout, most likely
		continue

	http_response_text = http_response.text

	# the user wants to display pages found that match an xpath query
	if xpath != False:

		try:
			http_response_text_bytes = http_response_text.encode()
		except:
			http_response_text_bytes = http_response_text

		tree = html.fromstring(http_response_text_bytes)
		xpath_results = tree.xpath(xpath)

		if xpath_results:

			matching_urls.append({"url":target_url, "reason":"xpath match"})
			continue

	# the user wants to display pages found that yielded a certain status code
	if status_code != 0:
		if http_response.status_code == status_code:
			matching_urls.append({"url":target_url, "reason":"status code match"})

	# the user wants to display pages found that match a regular expression
	if regex != False:
		if search(regex, http_response_text):
			matching_urls.append({"url":target_url, "reason":"regex match"})


matching_urls = stripRedundancies(matching_urls)

# and now we can output the file
handler = open(output_file, "w")
for matching_url in matching_urls:
	handler.write(matching_url["url"] + " " + matching_url["reason"] + "\n")
handler.close()
