import urllib2
from bs4 import BeautifulSoup


def format_web_string(string):
    """
    Format and return a string to remove <p> tags
    string -- html tree to be formated
    """
    cache = ""
    found_tag = False
    for c in string:
        if c == '<':
            found_tag = True

        if c == '>':
            found_tag = False
            cache = cache + c

        if found_tag:
            cache = cache + c

        if not found_tag and len(cache) > 0:
            string = string.replace(cache, "")
            cache = ""
    return string

def get_string_from_url(url):
    """
    Collect a url, extract an article from it, format the article to
    human-readble string and return it.
    url -- url to collect and extract data from
    """
    website = urllib2.urlopen(url).read()
    soup = BeautifulSoup(website, "html5lib")
    string = ""
    for p in soup.findAll('p'):
        if "twite" not in str(p) and "promo" not in str(p):
            string = string + str(p) + '\n'
    title = str(soup.findAll("title"))
    title = title[1:len(title) - 1]
    string = title + string
    string = string.replace(" -", "")
    return string

articles = []  # Store links to articls here


def fetch_articles(url, num_of_articles=5):
    """
    Retrieve an amount of urls directing to top stories from the site
    url -- website to collect from
    num_of_articles -- how many urls to collect
    """

    website = urllib2.urlopen(url).read()
    soup = BeautifulSoup(website, "html5lib")

    for c in soup.findAll("a", {"class": "top-story"}):
        if len(articles) < num_of_articles:
            articles.append(c['href'])

# Example usage below
fetch_articles("http://www.bbc.co.uk")
print format_web_string(get_string_from_url(articles[0]))
