from src.data.scraper import scrape_quotes, scrape_authors, scrape_authors_links
from src.data.file_handler import to_json, from_json
from src.db.db import import_quotes, import_authors

quotes_file = "src/data/qoutes.json"
authors_file = "src/data/authors.json"

if __name__ == '__main__':
    to_json(scrape_quotes(), quotes_file)
    to_json(scrape_authors(scrape_authors_links()), authors_file)
    print(import_quotes(from_json(quotes_file)))
    print(import_authors(from_json(authors_file)))
