import bs4
import easygui
import re

import all_films_rated_scraper


ALL_MOVIES = 'all_movies_ranked.html'
TOP_250 = 'files/top 250.html'
OUTPUT_FILE = 'ranked.txt'
NOT_RATED_MESSAGE = '{} NOT RATED !!!!!'


def run_script():
	cleaned = []
	all_movies = all_films_rated_scraper.list_of_movies(ALL_MOVIES)
	top_250 = all_films_rated_scraper.list_of_movies(TOP_250)

	for movie in top_250:
		try:
			rank = all_movies.index(movie) + 1
			cleaned.append((rank, movie))
		except ValueError:
			print(NOT_RATED_MESSAGE.format((movie)))

	with open(OUTPUT_FILE, 'w') as file:
		for index, movie in enumerate(sorted(cleaned)):
			file.write(f'{index + 1}. {movie[1][1]}\n')


if __name__ == '__main__':
	run_script()
