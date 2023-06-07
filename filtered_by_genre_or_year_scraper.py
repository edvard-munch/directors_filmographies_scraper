import bs4
import easygui
import re

import all_films_rated_scraper


ALL_MOVIES = 'all_movies_ranked.html'
SHORT_MOVIES = 'short_movies_ranked.html'

PARSER = 'html5lib'
ITEM_ID_PATTERN = r'page_catalog_item_\d+'
CATALOGIZATION_FIELD_ID = 'or_q_rating'
FILM_LINK_CLASS = 'film'
FILM_GENRE_CLASS = 'film_genre'
FILE_OPEN_BOX_TITLE = 'Open one or more files'
EXCLUDE_GENRE_PATTERN = 'Neo'


def run_script():
	filenames = easygui.fileopenbox(title=FILE_OPEN_BOX_TITLE, multiple=True)

	all_movies = all_films_rated_scraper.list_of_movies(ALL_MOVIES)
	all_movies_link_titles = [movie[0] for movie in all_movies]

	short_movies = all_films_rated_scraper.list_of_movies(SHORT_MOVIES)
	short_movies_link_titles = [movie[0] for movie in short_movies]

	result_set = []
	for file in filenames:

		with open(file) as fp:
			soup = bs4.BeautifulSoup(fp, PARSER)

		result_set += soup.find_all(id=re.compile(ITEM_ID_PATTERN))

	rated_movies = []
	for result in result_set:
		my_rating = result.find(class_=CATALOGIZATION_FIELD_ID).string.strip()

		if my_rating:
			try:
				film_link = result.find(class_=FILM_LINK_CLASS)

			except AttributeError:
				continue

			film_link_title = film_link.attrs['title']
			film_title = film_link.contents[0]

			try:
				rank = all_movies_link_titles.index(film_link_title) + 1
			except ValueError:
				short_movie = short_movies_link_titles.index(film_link_title)

				if short_movie:
					print(f"{film_title} is a short movie\n")
				else:
					print("Movie is not in the list!")
				continue

			genres_links = result.find_all(class_=FILM_GENRE_CLASS)
			genres = ', '. join([genre.string for genre in genres_links])

			rated_movies.append([rank, film_title, my_rating, genres])

	for index, movie in enumerate(sorted(rated_movies)):
		movie[0] = index + 1

		if EXCLUDE_GENRE_PATTERN in movie[3]:
			print(f'{index+1}. {movie[1]} {movie[2]} ({movie[3]})')
		else:	
			print(f'{index+1}. {movie[1]} {movie[2]}')


if __name__ == "__main__":
	run_script()
