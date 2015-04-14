import requests
import re
import urlparse

# In this example we're trying to collect e-mail addresses from a website

# Basic e-mail regexp:
# letter/number/dot/comma @ letter/number/dot/comma . letter/number
email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

# HTML <a> regexp
# Matches href="" attribute
link_re = re.compile(r'href="(.*?)"')

def crawl(url, maxlevel):
    # Limit the recursion, we're not downloading the whole Internet
    if(maxlevel == 0):
        return

    # Get the webpage
    res = requests.get(url)
    result = []

    # Check http response code
    if(res.status_code != 200):
        return []

    # Find all emails on current page
    result += email_re.findall(res.text)

    # Recursively scrawl other pages
    links = link_re.findall(res.text)
    for link in links:
        # Get an absolute URL for a link
        link = urlparse.urljoin(url, link)
        result += crawl(link, maxlevel - 1)

    return result

emails = crawl('http://127.0.0.1:8000', 3)

print "Scrapped e-mail addresses:"
for e in emails:
    print e