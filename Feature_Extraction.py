import re
import whois
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
# from Blacklist import blacklists
from global_variables import DEBUG, TESTING, Suspicious_TLD, Suspicious_Words

valid_ipv4 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
valid_link = re.compile('^http(s*)://*')

# take a string and output 1 if it contains an ip address
def is_ip_present(domain):
	return 1 if valid_ipv4.match(domain) else 0


# return number of delemiters(- _ ? , = &) in text 
def count_delims(text):
	return len(re.findall(r'[-_?,=&]', text))

# return number of digits in text / domains
def count_digits(text):
	return len(re.findall(r'[0-9]', text))


# either return the day pass by the target_date from now or -1 for invalid date
def calculate_days(target_date):
	# print(target_date)
	try:
		if not target_date:
			return -1

		# if list take the last element from list (datetime object)
		if type(target_date) is list:
			target_date = target_date[0]
		if type(target_date) is str:
			target_date = datetime.strptime(target_date, '%Y-%m-%d %H:%M:%S')
			
		today = datetime.now()
		return round((today - target_date).days)
	except Exception as error:
		print(error)
		return -1

# finding if any tag conatins external link
def any_external_link(site_domain, soup, tag, tag_attribute):
	try:
		if DEBUG:
			print('links in', tag, 'tag and', tag_attribute, 'attribute:')
		for current_tag in soup.find_all(tag):
			link = current_tag.get(tag_attribute)
			if valid_link.match(link):
				if DEBUG:
					print(link)
				link_domain = re.match(r'^[^/]*', re.sub(r'^www.', '', re.sub(r'^http(s*)://', '', link))).group(0)
				if link_domain != site_domain:
					return 1
		return 0
	except:
		return 0

# return href of favicon
def facivon_external_link_or_empty(site_domain, soup):
	try:
		icon_link = soup.find("link", rel="shortcut icon")
		if icon_link is None:
			icon_link = soup.find("link", rel="icon")
		if icon_link is None:
			icon_link = site_domain + '/favicon.ico'

		link = icon_link['href']
		if DEBUG:
			print('favicon link :', link)
		if valid_link.match(link):
			link_domain = re.match(r'^[^/]*', re.sub(r'^www.', '', re.sub(r'^http(s*)://', '', link))).group(0)
			if debug:
				print(site_domain, link_domain)
			if link_domain != site_domain:
				return 1
		return 0
	except:
		return 1


# Fast and easy to extract
def lexical_features(url, without_protocol):
	# vector storing lexical features
	vec = []

	domain = re.match(r'^[^/]*', without_protocol).group(0)
	path = re.findall(r'/[^/]*', without_protocol)
	
	# check if any ip present in Domain
	ip_present = is_ip_present(domain)
	vec.append(ip_present)

	# URL_length > 53
	vec.append(1 if len(url) > 53 else 0)
	# dots_in_url > 2
	vec.append(1 if without_protocol.count('.') > 2 else 0)
	# having_at_the_rate
	vec.append(1 if '@' in without_protocol else 0)
	# having_double_slash
	vec.append(1 if '//' in without_protocol else 0)
	# having_https
	vec.append(1 if re.match('https', without_protocol) else 0) 
	# url_shortening_service
	pass

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


	# hyphen_in_domain ?
	vec.append(1 if '-' in domain else 0)
	# digits_in_domain ?
	vec.append(1 if any([a.isdigit() for a in domain]) else 0)

	# length of directory / path length including all slashes > 25
	dir_length = len(re.sub(r'^[^/]*', '', without_protocol))
	vec.append(1 if dir_length > 25 else 0)

	# Largest directory name length > 11
	largest_path_token_length = max([len(token) for token in path_tokens]) if path_tokens else 0
	vec.append(1 if largest_path_token_length > 11 else 0)

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
		# Length of file name > 5
		vec.append(1 if len(file) > 5 else 0)

		# Arguments present in URL
		args = temporary[1] if len(temporary) > 1 else ''
		# arguments name length >  15
		vec.append(1 if len(args) > 15 else 0)
	else:
		vec.extend([0, 0])


	if DEBUG:
		print("Domain :",domain)
		print("Domain Tokens : ", domain_tokens)
		print("Path :", path)
		print("Path Tokens :", path_tokens)
		print("Other information :", other_info)
		print('Domain Length :', len(domain))
		print('Domain Count :', len(domain_tokens))
		print('IP present :', ip_present)
		print('File :', file)
		print('Arguments :', args)
		print('lexical features extracted :', len(vec))
		print()

	return vec


# slow but easy to extract
# whois_info is in form of dictionary now
def host_based_features(url, without_protocol):
	vec = []
	# domain name from start
	domain = re.match(r'^[^/]*', without_protocol).group(0)
	
	# Retriving information from whois server, might be slow !
	try:
		# who = whois_info
		who = whois.whois(domain)
	except:
		# print('NO information on whois')
		return [1 , 1]

	# Finding days until / from created, updated, expiration
	try:
		# domain = who['domain_name[0]] if type(who.domain_name) is list else who.domain_name
		created_days_ago = (calculate_days(who['creation_date']))
		print(created_days_ago)
		vec.extend([1 if created_days_ago < 365 else 0, 0])
	except Exception as error:
		print(error)
		vec.extend([1, 0])

	if DEBUG:
		print('WHO information :', who)
		# print('Domain name :', domain)
		print('Created days ago :', created_days_ago)
		print()

	return vec


# slow and difficult to extract
def content_based_features(url, without_protocol):
	valid_link = re.compile('^http(s*)://*')
	site_domain = re.match(r'^[^/]*', without_protocol).group(0)

	try:
		soup = BeautifulSoup(content_raw, "html.parser")

		# features
		vec = []

		# having iframe with external link
		vec.append(any_external_link(site_domain, soup, 'iframe', 'src'))
		# having <a> with external link
		vec.append(any_external_link(site_domain, soup, 'a', 'href'))
		# having favicon with external link
		vec.append(facivon_external_link_or_empty(site_domain, soup))
		# having an object (image, video, audio) with external link
		if any_external_link(site_domain, soup, 'img', 'src') or \
			any_external_link(site_domain, soup, 'source', 'src'):
			vec.append(1)
		else:
			vec.append(0)
		# redirecting to an external link
		# try:
		#     redirect_url = soup.find('meta')
		#     print(redirect_url)
		#     # vec.append(1 if )
		# except:
		#     vec.append(0)

		return vec
	except:
		return [1, 1, 1, 1]


# URL will be converted into feature vector 
def vector_construction(url):	
	url = url.strip()

	if DEBUG:
		print("URL :", url)
	
	feature_vector = []

	# remove http:// or https:// and www. from start of url if any
	without_protocol = re.sub(r'^www.', '', re.sub(r'^http(s*)://', '', url))

	# Lexical features
	feature_vector.extend(lexical_features(url, without_protocol))

	# Hots based features
	feature_vector.extend(host_based_features(url, without_protocol))

	# Content based features
	# feature_vector.extend(content_based_features(url, without_protocol))

	return feature_vector

# for testing only
if __name__ == '__main__':
	testing_url = 'https://www.google.com.naeemakhtar.com/path/end/here/virus.php'
	url = input("Enter Url or press enter to use testing url: ")
	print(vector_construction(url if url else testing_url))
