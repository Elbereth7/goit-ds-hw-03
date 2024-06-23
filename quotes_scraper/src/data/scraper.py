import requests
from bs4 import BeautifulSoup
from functools import wraps

URL = "https://quotes.toscrape.com/"

quotes_dump = []
author_dump = []
authors_links = set()

def scrape_pages(func):
    @wraps(func)
    def inner(url:str = URL):
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")
                result = func(soup)                
                next_page = soup.select_one("nav ul.pager li.next a")
                url = f'{URL}{next_page['href']}' if next_page else None
            else:
                url = None
        return result
    return inner  


@scrape_pages
def scrape_quotes(soup):    
    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        quote_text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags_html = quote.find("div", class_="tags").find_all("a", class_="tag")
        tags = [tag.text for tag in tags_html]
        quotes_dump.append({"tags": tags, "author": author, "quote": quote_text})
    return quotes_dump


def scrape_authors(links: list) -> list:
    for link in links:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            fullname = soup.find("h3", class_="author-title").text
            born_date = soup.find("span", class_="author-born-date").text
            born_location = soup.find("span", class_="author-born-location").text
            description = soup.find("div", class_="author-description").text.strip()
            author_dump.append(
                {
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description,
                }
            )
    return author_dump


@scrape_pages
def scrape_authors_links(soup):
    links = soup.find_all("a")
    authors_links.update({f'{URL}{link["href"]}' for link in links if link["href"].startswith("/author/")})
    return authors_links

  

if __name__ == '__main__':
    scrape_quotes(URL)
    # print(quotes_dump)
    # quotes_authors = set()
    # for quote in quotes_dump:
    #     quotes_authors.add(quote['author'])
    # print(f'authors_names: {quotes_authors}')
    # print(f'len(authors_names): {len(quotes_authors)}')

    # print(len(scrape_authors_links(URL)))
    # print(f'authors_links: {authors_links}')
    # print(f'len(authors_links): {len(authors_links)}')

    

    print(len(scrape_authors(scrape_authors_links(URL))))
    # print(author_dump)