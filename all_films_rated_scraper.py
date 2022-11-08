import bs4

FILENAME = 'files/all_movies_ranked'
PARSER = 'html5lib'
FILMS_ID = 'boxes'
FILM_TAG_NAME = 'li'


def list_of_movies():
	with open(FILENAME) as fp:
		soup = bs4.BeautifulSoup(fp, PARSER)

	result_set = soup.find(id=FILMS_ID)

	movies = []
	for res in result_set:
		if res.name == FILM_TAG_NAME:
			movies.append((res.contents[1].attrs['title']))
			# print(f"{res.contents[1].contents[0]} {res.contents[1].attrs['title']}")

	return movies
