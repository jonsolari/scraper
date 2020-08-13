## eBay Scraper

This (`ebay.py`) is an HTML scraper made in python using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).

Runs on the command line, requires python3.

Expects a search string as an argument variable, for example:

```python3 ebay.py "mountain goats sweden lp"```

Will return 'None' if there are no results including all the words in the string. 

Otherwise will return the Title, Current Bid, and URL of the lowest-priced auction listing.

`scrapecompare.py` is a separate script, meant to compare Discogs and eBay prices for a certain set of vinyl record releases. 
