import requests
import os
from bs4 import BeautifulSoup
from setting import *


def run():
	res = requests.get(URL)
	html = res.text
	soup = BeautifulSoup(html, 'html.parser')
	test = soup.select('ul.search-results')

	for index in test:
		for extend in check_extend:
			if extend in index.select('li')[2].text.split(': ')[1]:
				sha256 = index.select('li')[8].text.split(': ')[1] + '.7z'
				dst_url = BASE_URL + sha256
				down_res = requests.get(dst_url)

				dst_file = FILE_PATH + sha256
				with open(dst_file, 'wb') as f:
					f.write(down_res.content)

				break


if __name__ == "__main__":
	run()