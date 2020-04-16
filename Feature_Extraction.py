import re
import whois
import time
import datetime
from global_variables import DEBUG, TESTING

Suspicious_Words=['secure','account','update','banking','login','click','confirm','password','verify','signin','ebayisapi','lucky','bonus']
Suspicious_TLD=['zip','cricket','link','work','party','gq','kim','country','science','tk']


# take a string and output 1 if it contains an ip address
def is_ip_present(domain):
	valid_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	return 1 if valid_ip.match(domain) else 0


# return number of delemiters(- _ ? , = &) in text 
def count_delims(text):
	return len(re.findall(r'[-_?,=&]', text))


# either return the day pass by the target_date from now or -1 for invalid date
def calculate_days(target_date):
	try:
		if not target_date or type(target_date) is str:
			return -1

		# if list take the last element from list (datetime object)
		if type(target_date) is list:
			target_date = target_date[0]
		
		if type(target_date) is datetime.datetime:	
			today = datetime.datetime.now()
			return (today - target_date).days
		else:
			return -1
	except:
		return -1


# return a vector containing lexical features
def lexical_features(url):
	# vector storing lexical features
	vec = []

	# protocol use by website
	protocol = re.match(r'^http(s*)', url)
	if not protocol:
		vec.append(-1)
	elif protocol.group(0) == 'https':
		vec.append(1)
	elif protocol.group(0) == 'http':
		vec.append(0)
	else:
		vec.append(-1)

	# remove http:// or https:// from url if any
	without_protocol = re.sub(r'^http(s*)://', '', url)
	
	domain = re.match(r'^[^/]*', without_protocol).group(0)
	path = re.findall(r'/[^/]*', without_protocol)

	# check if any ip present in Domain
	ip_present = is_ip_present(domain)
	vec.append(ip_present)

	# URL_length
	vec.append(len(without_protocol))
	# dots_in_url
	vec.append(without_protocol.count('.'))

	# domain tokens, filter NULL values
	domain_tokens = list(filter(lambda token: token, domain.split('.'))) if not ip_present else domain
 
	# path tokens, without filtering Null values
	path_tokens = [re.sub('/', '', token) for token in path]

	# arguments for query or file in URL
	other_info = path_tokens[-1] if path_tokens else ''
	
	# Remove the above part from path tokens
	path_tokens = path_tokens[:-1]
	
	# Filter Null values from path
	path = list(filter(lambda token: token, path))

	# Domain length
	vec.append(len(domain))
	# Number of all domains
	vec.append(len(domain_tokens))
	# hyphen_count_in_domain
	vec.append(domain.count('-'))
	# Largest domain name length
	largest_domain_length = max([len(token) for token in domain_tokens]) if domain_tokens else 0
	vec.append(largest_domain_length)
	# Average of all domain length
	avg_domain_length = sum([len(token) for token in domain_tokens]) / len(domain_tokens) if domain_tokens else 0
	vec.append(avg_domain_length)

	# slashes
	slashes = len(path)

	# length of directory / path length including all slashes
	dir_length = sum([len(token) for token in path_tokens]) + slashes
	vec.append(dir_length)
	# sub-directories count
	subdir_count = len(path_tokens)
	vec.append(subdir_count)
	# Largest directory name length
	largest_path_token_length = max([len(token) for token in path_tokens]) if path_tokens else 0
	vec.append(largest_path_token_length)
	# Average of all directory length
	avg_path_length = sum([len(token) for token in path_tokens]) / len(path_tokens) if path_tokens else 0
	vec.append(avg_path_length)

	# Top Level Domain, there can be subdomains but not counting
	TLD = domain_tokens[-1] if domain else ''
	# presence of any suspicious word in top level domain
	if not ip_present:
		for suspect in Suspicious_TLD:
			if re.search(suspect, TLD, re.IGNORECASE):
				vec.append(1)
				break
		else:
			vec.append(0)
	else:
		vec.append(0)
	
	# Any files or arguments if present in the url 
	file, args = '', ''
	if other_info:
		# split file and arguments
		temporary = other_info.split('?')
		
		# file name
		file = temporary[0]
		# Length of file name
		vec.append(len(file))
		# dots in file name
		vec.append(file.count('.'))
		# Count delimeters in file name
		vec.append(count_delims(file))

		# Arguments present in URL
		args = temporary[1] if len(temporary) > 1 else ''
		# POST or PUT arguments present
		if args:
			# Argument length
			vec.append(len(args)+1)
			# Split all arguments as tokens 
			args_token = args.split('&')
			# Number of arguments
			vec.append(len(args_token))
			
			# largest argument name length
			largets_argument_length = 0
			# maximum number of delimeters in any argument 
			max_delims_count = 0
			for argument in args_token:
				query = argument.split('=')
				largets_argument_length = max(largets_argument_length, len(query[0]))
				max_delims_count = max(max_delims_count, count_delims(query[0]))
				if len(query) > 1:
					max_delims_count = max(max_delims_count, count_delims(query[1]))
			vec.append(largets_argument_length)
			vec.append(max_delims_count)
		else:
			vec.extend([0, 0, 0, 0])
	else:
		vec.extend([0, 0, 0, 0, 0, 0, 0])


	if DEBUG:
		print("Domain :",domain)
		print("Domain Tokens : ", domain_tokens)
		print("Path :", path)
		print("Path Tokens :", path_tokens)
		print("Other information :", other_info)
		print("Directory Length :", dir_length)
		print('Sub Directory Count :', subdir_count)
		print('Domain Length :', len(domain))
		print('Domain Count :', len(domain_tokens))
		print('IP present :', ip_present)
		print('Largest Domain name Length :', largest_domain_length)
		print('Average Domain name Length :', avg_domain_length)
		print('Largest sub-directory/path name length:', largest_path_token_length)
		print('Average sub-directory/path name length :', avg_path_length)
		print('File :', file)
		print('Arguments :', args)
		print('lexical features extracted :', len(vec))
		print()

	return vec


# return a vector containing host based features 
def host_based_features(url):
	vec = []
	# remove protocol and extract the domain name from start
	domain = re.match(r'^[^/]*', re.sub(r'http(s*)://', '', url)).group(0)
	
	# Retriving information from whois server, might be slow !
	try:
		who = whois.whois(domain)
	except:
		print('No host information about', domain)
		return [-1, -1, -1, -1]

	# Finding days until / from created, updated, expiration
	try:
		domain = who.domain_name[0] if type(who.domain_name) is list else who.domain_name
		created_days_ago = calculate_days(who.creation_date)
		updated_days_ago = calculate_days(who.updated_date)
		expiration_days_remaining = 0 - calculate_days(who.expiration_date)
		vec.extend([created_days_ago, updated_days_ago, expiration_days_remaining])
	except:
		# print('Error in extracting dates from whois')
		vec.extend([-1, -1, -1])

	# Country zip code
	try:
		zipcode = who.zipcode
		# remove extra character from zipcode
		if '-' in zipcode:
			zipcode = re.sub(r'-*', '', zipcode)
		zipcode = re.sub(r'[A-Za-z\s]*', '', zipcode)
		vec.append(int(zipcode))
	except:
		# print('Error in extracting zipcode from whois')
		vec.append(-1)

	if DEBUG:
		# print('WHO information :', who)
		print('Domain name :', domain)
		print('Created days ago :', created_days_ago)
		print('Update days ago :', updated_days_ago)
		print('Expired in days :', expiration_days_remaining)
		print('Country Zipcode :', zipcode)
		print('host based features extracted :', len(vec))
		print()

	return vec


# URL will be converted into feature vector 
def vector_construction(url):
	# columns=('protocol', 'ip present', 'len of url','no of dots','security sensitive words','no of hyphens in dom',\
	# 'dir_len','no of subdir','domain len','domain token count','path token count','largest domain_tok_len',\
	# 'avg_dom_token_len','largest path token length','avg path token length','suspicious tld','len_of_file','total dots in file',\
	# 'total delims in file','len_of_argument','no_of_variables','len_of_largest_variable_val',\
	# 'max_no_of_argum_delims','create_age(months)','expiry_age(months)','update_age(days)','zipcode')
	
	url = url.strip()
	if DEBUG:
		print("URL :", url)
	
	feature_vector = []

	# Lexical features
	feature_vector.extend(lexical_features(url))

	# Hots based features
	feature_vector.extend(host_based_features(url))

	return feature_vector

# for testing only
if TESTING:
	testing_url = 'http://www.g00gle.naeemakhtar.com/path/end/here/virus.php'
	url = input("Enter Url or press enter to use testing url: ")
	print(vector_construction(url if url else testing_url))
