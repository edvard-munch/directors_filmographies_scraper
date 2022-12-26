import bs4

PARSER = 'html5lib'
FILMS_ID = 'boxes'
FILM_TAG_NAME = 'li'


def list_of_movies(filename):
	with open(filename) as fp:
		soup = bs4.BeautifulSoup(fp, PARSER)

	result_set = soup.find(id=FILMS_ID)

	movies = []
	for res in result_set:
		if res.name == FILM_TAG_NAME:
			movie_data = [res.contents[1].attrs['title']]

			if res.contents[1].string == None:
				movie_data.append(f'{res.contents[1].contents[0]} {res.contents[1].contents[1].string}')

			else:
				movie_data.append(res.contents[1].string)

			movies.append(movie_data)

	return movies
