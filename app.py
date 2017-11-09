from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/<q>")
def index(q):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
	}

	with requests.Session() as s:
		s.headers = headers
		search_query = q
		search_query = search_query.replace(" ","+")
		base_url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
		r = s.get(base_url + search_query)
		soup = BeautifulSoup(r.content, "html.parser")
		items = soup.findAll('div', {'class', "s-item-container"})
		final_list = {}
		for i in items:
			content_soup = BeautifulSoup(str(i),"html.parser")
			heading_tag = str(content_soup.findAll('h2'))
			heading_text = heading_tag[heading_tag.find('data-attribute="') + 16:heading_tag.find('"',heading_tag.find('data-attribute="') + 16)]

			price_tag = str(content_soup.findAll('span',{"class": "s-price"}))
			if len(price_tag) == 2:
				price_tag = str(content_soup.findAll('span',{"class": "a-size-base"}))

			price_text = price_tag[price_tag.find('">')+2:price_tag.find("</span>",price_tag.find('">')+2)]

			if price_text != "":
				final_list[heading_text] = str(price_text)

	return jsonify(final_list)

if __name__ == '__main__':
	app.run(debug = True)

