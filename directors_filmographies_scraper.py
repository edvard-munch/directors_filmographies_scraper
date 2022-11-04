# need to recognize short movies somehow
# check for co-director involvements

import bs4
import easygui
import re

import all_films_rated_scraper


PARSER = 'html5lib'
FILMS_ID = 'films'
FILM_TAG_NAME = 'li'
HEADER_CLASS = 'disco_header_top'
CATALOGIZATION_ID = 'film_cat_catalog_msg'
HEADER_STRING = 'other roles'
RATING_MULTIPLIER = 2
HTML_WRAPPER = '{}. {} [color navy][b]{}[/b][/color]'


def run_script():
	filename = easygui.fileopenbox(title='path to file')
	print(filename)

	movies = all_films_rated_scraper.list_of_movies()

	with open(filename) as fp:
		soup = bs4.BeautifulSoup(fp, PARSER)

	result_set = soup.find(id=FILMS_ID)

	top_billing = []
	cleaned = []

	for el in result_set:
		if el.name == FILM_TAG_NAME:
			top_billing.append(el)

		try:
			header = el.next_element
			try:
				if HEADER_CLASS in header.attrs['class']:
					if header.contents[1].string.lower() == HEADER_STRING:
						break

			except KeyError:
				pass

		except AttributeError:
			pass

	if top_billing:
		for item in top_billing:
			involvement = item.find(class_='film_subline').contents[2]
			if 'Director' in involvement:
				catalogization = item.find(id=re.compile(CATALOGIZATION_ID))

				try:
					my_rating = int(float(catalogization.string) * RATING_MULTIPLIER)

				except ValueError:
					continue

				try:
					header = item.next_element.attrs

				except AttributeError:
					pass	

				link = catalogization.parent.parent.find('a').attrs['title']
				rank = movies.index(link) + 1
				cleaned.append((rank, link, my_rating))
	else:
		exit(0)

	for index, movie in enumerate(sorted(cleaned)):
		print(HTML_WRAPPER.format(index + 1, movie[1], movie[2]))

if __name__ == '__main__':
	run_script()
