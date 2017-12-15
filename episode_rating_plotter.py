import requests, sys
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from math import floor, ceil


def find_id(search):
	page = requests.get(f'http://www.imdb.com/search/title?title={search}&title_type=tv_series')
	soup = BeautifulSoup(page.content, 'html.parser')

	try:
		h3 = soup.find('h3', class_='lister-item-header')
		a = h3.find('a')
		id = a['href'].split('/')[2]
		title = a.text
		return id, title
	except:
		return None

def search_input():
	search = '%20'.join(input('Search: ').split())
	id, title = find_id(search)
	while(id == None):
		print("Not found")
		search = '%20'.join(input('Search: ').split())
		id, title = find_id(search)
	return id, title

def wrong_season(season, soup):
	real_season = int(soup.find('h3', id='episode_top').text.split()[-1])
	return season > real_season

def episode_rating(episode):
	div = episode.find('div', class_='ipl-rating-star')
	span = div.find('span', class_='ipl-rating-star__rating')
	rating = float(span.text)
	return rating

def season_ratings(id, season):
	page = requests.get(f'http://www.imdb.com/title/{id}/episodes?season={season}')
	soup = BeautifulSoup(page.content, 'html.parser')

	if wrong_season(season, soup): return None

	ratings = []
	for episode in soup.find_all('div', class_='list_item'):
		rating = episode_rating(episode)
		if rating > 0:
			ratings.append(rating)
		else:
			break
	return ratings

def show_ratings(id):
	seasons = []
	for season in range(1,1000):
		ratings = season_ratings(id, season)
		if ratings == None:
			break
		if len(ratings) > 0:
			seasons.append(ratings)
	return seasons

def plot(seasons, title):
	x = 1
	for i, season in enumerate(seasons):
		color = f'C{i}'
		newx = x + len(season)
		xx = range(x,newx)
		plt.plot(xx, season, f'{color}o')
		z = np.polyfit(xx, season, 1)
		p = np.poly1d(z)
		plt.plot(xx,p(xx), color)
		x = newx

	flat_seasons = [item for sublist in seasons for item in sublist]
	miny = max(0, floor(min(flat_seasons)))
	maxy = min(10, ceil(max(flat_seasons)))

	xx = range(1,x)
	z = np.polyfit(xx, flat_seasons, 1)
	p = np.poly1d(z)
	plt.plot(xx, p(xx), '0.7')

	plt.axis([0,x,miny,maxy])
	plt.title(title)
	plt.show()


if __name__ == '__main__':
	id, title = search_input()
	seasons = show_ratings(id)
	plot(seasons, title)