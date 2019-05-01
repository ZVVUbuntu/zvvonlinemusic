"""Parser module"""
import re
import bs4
from bs4 import BeautifulSoup as BS
import urllib.parse
import urllib.request
from urllib.request import Request, urlopen
from . import requests
from PyQt5.QtCore import QCoreApplication


class Parser():
	"""Parser class"""
	def __init__(self, get_widget):
		self.GET_WIDGET = get_widget
		self.LIST_SITES = [
							'https://drivemusic.me',
					 		'https://mp3-tut.com',
					 		'http://poiskm.co',
					 	]
		self.PARSER = "html.parser"
		self.HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		
	def get_params(self, url):
		"""Get params"""
		if url == self.LIST_SITES[0]:
			ORIG_SITE = "{0}/novinki_muzyki/".format(url)
			FULL_SITE_PARAMS = urllib.parse.urljoin(url, '/?do=search&subaction=search&story={0}&sbutt=')
		if url == self.LIST_SITES[1]:
			ORIG_SITE = "{0}/new-hits".format(url)
			FULL_SITE_PARAMS = urllib.parse.urljoin(url, 'search?query={0}')
		if url == self.LIST_SITES[2]:
			ORIG_SITE = url
			FULL_SITE_PARAMS = urllib.parse.urljoin(url, 'show/{0}')
		return ORIG_SITE, FULL_SITE_PARAMS
	
	def get_format_text(self, text):
		"""Get format text"""
		format_text = text.lower()
		format_text = format_text.replace(" ",'+')
		format_text = urllib.request.quote(format_text)
		return format_text
		
	def parse(self, text='', url=''):
		"""Parse"""
		ORIG_SITE, FULL_SITE_PARAMS = self.get_params(url)
		if text:
			text = self.get_format_text(text)
			webpage = requests.get(FULL_SITE_PARAMS.format(text)).text
		else:
			webpage = requests.get(ORIG_SITE).text
		if webpage:
			soup = BS(webpage, self.PARSER)
			if self.LIST_SITES.index(url) == 0:
				divs = soup.find_all('div', attrs={'class':'music-popular-wrapper'})
				self.get_drivers_items(divs)
			if self.LIST_SITES.index(url) == 1:
				divs = soup.find_all("div", attrs={"class":"audio-list-entry-inner"})
				self.get_mp3tut_items(divs)
			if self.LIST_SITES.index(url) == 2:
				divs = soup.find_all("div", attrs={"class":"title_wrap"})
				self.get_poiskm_items(divs)

	def get_drivers_items(self, divs):
		"""Get drivers items"""
		for item in divs:
			QCoreApplication.processEvents()
			links = item.find_all('a')
			if len(links) > 1:
				download, name, artist = links[0], links[1], links[2]
				music_text = artist.text + " - " + name.text
				href = urllib.parse.urljoin(self.LIST_SITES[0], download.get('data-url'))
				duration = item.find('div', attrs={'class':'popular-download-number'}).text.strip()
			if music_text and href:
				self.GET_WIDGET.add_row(music_text, href, duration)
				
	def get_mp3tut_items(self, divs):
		"""Get mp3tut items"""
		for item in divs:
			QCoreApplication.processEvents()
			music_text = item.button.get('data-title')
			href = item.button.get('data-audiofile')
			duration = item.find('div', attrs={'class':'audio-duration'}).text.strip()
			self.GET_WIDGET.add_row(music_text, href, duration)
			
	def get_poiskm_items(self, divs):
		"""Get poiskm items"""
		for item in divs:
			QCoreApplication.processEvents()
			music_text = item.find("span", attrs={"class":"songname px"}).text.strip()
			href = "{0}/?do=getById&id={1}&n=1".format(self.LIST_SITES[2], item.get('data-songid'))
			duration = item.find('span', attrs={'class':'duration'}).text.strip()
			self.GET_WIDGET.add_row(music_text, href, duration)
			
