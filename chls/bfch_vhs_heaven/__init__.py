from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList, MoreEpisodesAction

_SEARCH_URL = 'http://woodytv.esy.es/'

_FEEDLIST = [
  {'title':'Popular', 'url':'http://woodytv.esy.es/'},
  {'title':'All videos', 'url':'http://woodytv.esy.es//videos'},
  {'title':'free', 'url':'http://woodytv.esy.es/category/13/free'},
  {'title':'horror', 'url':'http://woodytv.esy.es/category/12/horror'},
  {'title':'sci-fi', 'url':'http://woodytv.esy.es/category/11/sci-fi'},
  {'title':'documentary', 'url':'http://woodytv.esy.es/category/10/documentary'},
  {'title':'cartoon', 'url':'http://woodytv.esy.es/category/9/cartoon'},
  {'title':'Fantasy', 'url':'http://woodytv.esy.es/category/8/fantasy'},
  {'title':'medieval', 'url':'http://woodytv.esy.es/category/7/medieval'},
  {'title':'comedy', 'url':'http://woodytv.esy.es/category/5/comedy'},
  {'title':'action', 'url':'http://woodytv.esy.es/category/4/action'},
  {'title':'thriller', 'url':'http://woodytv.esy.es/category/3/thriller'},
  {'title':'drama', 'url':'http://woodytv.esy.es/category/2/drama'},
]
def name():
  return 'http://woodytv.esy.es/'

def image():
  return 'icon.png'

def description():
  return "vhsheaven (<a target='_blank' href='http://www.bbc.co.uk/iplayer'>http://www.bbc.co.uk/iplayer</a>). Geo-restricted to UK."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  return _extract(doc)

def search(q):
  doc = get_doc(_SEARCH_URL, params = { 'q':q })
  return _extract(doc)

def showmore(link):
  doc = get_doc(link)
  return _extract(doc)

def _extract(doc):
  rtree = select_all(doc, 'li.list-item')
  results = PlayItemList()
  for l in rtree:
    a = select_one(l, 'a')
    url = get_attr(a, 'href')
    if url is None or not url.startswith('/iplayer'):
      continue
    url = "http://woodytv.esy.es/" + url

    pdiv = select_one(l, 'div.primary')
    idiv = select_one(pdiv, 'div.r-image')
    if idiv is None:
      idiv = select_one(pdiv, 'div.rs-image')
      idiv = select_one(idiv, 'source')
      img = get_attr(idiv, 'srcset')
    else:
      img = get_attr(idiv, 'data-ip-src')

    sdiv = select_one(l, 'div.secondary')
    title = get_text(select_one(sdiv, 'div.title'))
    subtitle = get_text(select_one(sdiv, 'div.subtitle'))
    synopsis = get_text(select_one(sdiv, 'p.synopsis'))
    item = PlayItem(title, img, url, subtitle, synopsis)
    a = select_one(l, 'a.view-more-container')
    if a is not None:
      link = "http://woodytv.esy.es/" + a.get('href')
      item.add_action(MoreEpisodesAction(link, title))
    results.add(item)
  return results
