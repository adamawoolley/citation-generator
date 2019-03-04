from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime

def date_config(date):
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  date = date.split("-")
  return f"{months[int(date[1]) - 1]} {date[2]}, {date[0]}"

def date_accessed():
  return date_config(datetime.today().strftime("%Y-%m-%d")) 

def site_title(soup):
  for meta in soup.find_all("meta"):
        if meta.get("property") == "og:site_name":
            return meta.get("content")

def find_title(soup):
    for meta in soup.find_all("meta"):
        if meta.get("property") == "og:title":
            return meta.get("content")
    return soup.title.string

def find_author(soup):
    classtypes = [
        "author", "author_url", "by", "css-1baulvz", "atavist-byline-name",
        "article-author-name", "c-byline__item", "post__by", "byline-name",
        "publisher_url"
    ]

    for meta in soup.find_all("meta"):
        if meta.get("name") == "author" or meta.get("property") == "author":
            return meta.get("content")

    for a in soup.find_all("a"):
        try:
            for style in a.get("class"):
                if style in classtypes:
                    return a.get_text().strip()
        except TypeError:
            pass

    for a in soup.find_all("a"):
        try:
            for rel in a.get("rel"):
                if rel == "author":
                    return a.get_text().strip()
        except TypeError:
            pass

    for line in soup.find_all("span"):
        try:
            for rel in line.get("rel"):
                if rel == "author":
                    return line.get_text().strip()
        except TypeError:
            pass

    for line in soup.find_all("span"):
        try:
            for style in line.get("class"):
                if style in classtypes:
                    return line.get_text().strip()
        except TypeError:
            pass

    for h5 in soup.find_all("h5"):
        try:
            for style in h5.get("class"):
                if style in classtypes:
                    return h5.get_text().strip()
        except TypeError:
            pass

    for cite in soup.find_all("cite"):
        try:
            for style in cite.get("class"):
                if style in classtypes:
                    print("class cite")
                    return cite.get_text().strip()
        except TypeError:
            pass
    return ''

def date_updated(soup):
  for time in soup.find_all("time"):
        return time.get("datetime")[0:10]
  return ''

def date_published(soup):
    for meta in soup.find_all("meta"):
        if meta.get("property") == "article:published_time":
            return date_config(meta.get("content")[0:10])

    for time in soup.find_all("time"):
        if time.get("itemprop") == "datePublished":
            return date_config(time.get("datetime")[0:10])
    return date_config(date_updated(soup))

def chicago_format(soup, url):
  return ["author", find_author(soup), "title", find_title(soup), "site name", site_title(soup), "url", url, "date accessed", date_accessed()], ["author", "title", "site name", "url", "date accessed"]

def apa_format(soup, url):
  return ["author", find_author(soup), "date published", date_published(soup), "title", find_title(soup), "url", url], ["author", "date published", "title", "url"]

def cite(cite_type, url):
  soup = BeautifulSoup(request.urlopen(url).read().decode("utf-8"), "html.parser")
  if cite_type == "apa":
    return apa_format(soup, url)
  elif cite_type == "chicago":
    return chicago_format(soup, url)
#  else:
#    return mla_format(soup)
