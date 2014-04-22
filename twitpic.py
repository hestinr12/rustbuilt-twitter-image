import requests
from bs4 import BeautifulSoup
import wget
import os
import sys


def main(count):

	count = int(count)

	#print type(count)

	site = requests.get('http://rustbuilt.org')
	html = BeautifulSoup(site.text)

	#get twitter picture section
	list = html.find('div', {'id':'addedacc'})

	#get the target elements containing handles
	blocks = list.findAll('div', {'class':'twitter-anywhere-user'})

	#Extract handles
	names = []
	for block in blocks:
		names.append(block['rel'])

	#Slice the count of new handles...
	new = names[:count]


	dictionary = []

	#try to get the link for the user profile picture and append the dict into an arra of dicts, exceptions will not append yielding only correct images.
	for x in range(0,count):
		try:
			#this line will need adjusted should the layout of twitter changes
			soup = BeautifulSoup(requests.get('http://twitter.com/' + new[x]).text)
			src = soup.find('img', {'class':'avatar', 'class':'size73'})['src']
			dictionary.append({'user':new[x], 'link': src})
		except:
			print new[x] + ' failed for some reason...'
			pass

	#print dictionary

	for a in dictionary:
		filename = wget.download(a['link'])
		print filename
		os.rename(filename, a['user'].lower() + '.jpg')



if __name__ == "__main__":
    main(sys.argv[1])