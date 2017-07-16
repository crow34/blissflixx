from chanutils import get_doc, select_all, select_one
from chanutils import get_attr, get_text, get_text_content
from playitem import PlayItem, PlayItemList, MoreEpisodesAction

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

_SHOWLIST = []

def name():
  return 'vhsheaven'

def image():
  return 'icon.png'

def description():
   return "vhsheaven Player Channel (<a target='_blank' href='http://woodytv.esy.es/'>http://woodytv.esy.es/</a>). Geo-restricted to UK."

def feedlist():
  return _FEEDLIST

def feed(idx):
  url = _FEEDLIST[idx]['url']
  doc = get_doc(url)
  rtree = select_all(doc, "a.complex-link")
  results = PlayItemList()
  for l in rtree:
    url = get_attr(l, 'href')
    el = select_one(l, '.tout__title')
    if el is None:
      continue
    title = get_text(el)
    el = select_one(l, 'img.fluid-media__media')
    img = get_attr(el, 'src')
    el = select_one(l, 'p.tout__meta')
    subtitle = get_text_content(el)
    if subtitle == 'No episodes available':
      continue    
    item = PlayItem(title, img, url, subtitle)
    if subtitle != '1 episode':
      item.add_action(MoreEpisodesAction(url, title))
    results.add(item)
  if idx == 0:
    global _SHOWLIST
    _SHOWLIST = results
  return results

def search(q):
  results = PlayItemList()
  items = _SHOWLIST.to_list()
  for i in items:
    title = i.title 
    if q.lower() in title.lower():
      results.add(i)
  return results

def showmore(link):
  doc = get_doc(link)
  rtree = select_all(doc, "a.complex-link")
  results = PlayItemList()
  for l in rtree:
    url = get_attr(l, 'href')
    el = select_one(l, 'img.fluid-media__media')
    img = get_attr(el, 'src')
    el = select_one(l, 'h3')
    title = get_text(el)
    el = select_one(l, 'time')
    subtitle = ""
    if el is not None and el.text is not None:
      subtitle = get_text(el)
    el = select_one(l, 'p.tout__summary')
    synopsis = get_text(el)
    item = PlayItem(title, img, url, subtitle, synopsis)
    results.add(item)
  return results
