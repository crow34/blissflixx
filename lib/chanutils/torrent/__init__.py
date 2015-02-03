import re
from torrentparse import TorrentParser
import base64
import subprocess
import chanutils

hash_re = re.compile("xt=urn:btih:([A-Za-z0-9]+)")
base32_re = re.compile("[A-Z2-7]{32}")
valid_re = re.compile("[A-F0-9]{40}")

torr_sites = ("torcache.net", "torrage.com", "zoink.it")

def torrent_from_hash(hashid):
  path = "/torrent/" + hashid + ".torrent"
  for site in torr_sites:
    try:
      r = chanutils.get("http://" + site + path)
      return r.content
    except Exception:
      pass
  return None

def magnet2torrent(link):
  matches = hash_re.search(link)
  if not matches or len(matches.groups()) != 1:
    raise Exception("Unable to find magnet hash")
  hashid = matches.group(1).upper()

  #If hash is base32, convert it to base16
  if len(hashid) == 32 and base32_re.search(hashid):
    s = base64.b32decode(hashid)
    hashid = base64.b16encode(s)
  elif not (len(hashid) == 40 and valid_re.search(hashid)):
    raise Exception("Invalid magnet hash")

  return torrent_from_hash(hashid)

def peerflix_metadata(link):
  s = subprocess.check_output(["peerflix", link, "-l"])
  lines = s.split('\n')
  files = []
  for l in lines:
    delim = l.rfind(':')
    if delim == -1:
      break
    files.append((l[20:delim-6], l[delim+7:-5]))
  return files

def torrent_files(link):
  if link.startswith("magnet:"):
    torrent = magnet2torrent(link)
  else:
    # Remove any parameters from torrent link
    # as some sites may not download if wrong
    idx = link.find('?')
    if idx > -1:
      link = link[:idx]
    r = chanutils.get(link)
    torrent = r.content

  files = None
  if torrent:
    try:
      parser = TorrentParser(torrent)
      files =  parser.get_files_details()
    except Exception:
      pass
  if not files:
    files = peerflix_metadata(link)
  return files

def showmore(link):
  files = torrent_files(link)
  if not files:
    raise Exception("Unable to retrieve torrent files")
  results = []
  idx = 0
  for f in files:
    subtitle = ''
    if isinstance(f[1], basestring):
      subtitle = 'Size: ' + f[1]
    else:
      subtitle = 'Size: ' + chanutils.byte_size(f[1])
    url = link
    if link.find('?') > -1:
      url = url + '&'
    else:
      url = url + '?'
    url = url + "fileidx=" + str(idx)
    img = '/img/icons/file-o.svg'
    results.append({'title':f[0], 'subtitle':subtitle, 'url':url, 'img':img})
    idx = idx + 1
  return results