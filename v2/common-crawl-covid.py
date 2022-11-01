from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys
import sys
import zlib
import urllib
import gzip
import urllib.request

# MARK: - Global constants

OUTPUTFILE_SUFFIX = "crawled_results"

# MARK: - Function declarations

def parseWarcFiles():
  # Get url name from user, or use default if none provided
  file_name = "http://data.commoncrawl.org/crawl-data/CC-MAIN-2020-24/warc.paths.gz"
  if len(sys.argv) > 1:
      file_name = sys.argv[1]

  # Fetch the warc paths file
  stream = None
  if file_name.startswith("http://") or file_name.startswith("https://"):
      stream = requests.get(file_name, stream=True).raw
  else:
      stream = open(file_name, "rb")

  # Put each warc file path into an array, file_names
  f=urllib.request.urlopen(file_name) 
  decompressed_data=zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
  data = decompressed_data.decode('utf-8')
  file_names = []
  for line in data.splitlines():
    fullURL = "http://data.commoncrawl.org/" + line # + "\n"
    file_names.append(fullURL)

  # Parse for relevant pages
  parseWarcFilesForRelevantPages(file_names)

def parseWarcFilesForRelevantPages(file_names):
  hits = 0
  entries = 0
  outputfile_count = 1
  results_file = open(OUTPUTFILE_SUFFIX + str(outputfile_count) + ".txt", "w")
  lastCheckedUrl = "" # this check is necessary to prevent the same files from being checked three times

  for file_name in file_names:
    stream = requests.get(file_name, stream=True).raw
    try:
      for record in ArchiveIterator(stream, arc2warc=True):
        if record.rec_type == "warcinfo":
            continue
        entries = entries + 1
        webUrl = record.rec_headers.get_header("WARC-Target-URI")
        if lastCheckedUrl != webUrl and isRelevant(record):
          hits = hits + 1
          if hits % 100 == 0:
            print("closing a file, opening a new one")
            results_file.close() 
            outputfile_count += 1
            if outputfile_count == 11:
              break
            else:
              results_file = open(OUTPUTFILE_SUFFIX + str(outputfile_count) + ".txt", "w")
          results_file.write(webUrl + "\n")
          lastCheckedUrl = webUrl
          print("adding: " + webUrl)
    except Exception as e:
      print(e)
    if outputfile_count == 11:
      break
  print("Check out output files for " + str(hits) + " pages related to COVID-19's economic impact, out of " + str(entries) + " total pages crawled.")

def isRelevant( record ):
  contents = (
      record.content_stream()
      .read()
      .decode("utf-8", "replace")
  )
  webUrl = record.rec_headers.get_header("WARC-Target-URI")

  if 'covid' in webUrl.lower():
    econWords = ["business", "capital", "wage", "market", "finance", "econom", "retail", "advertis", "bank", "cash", "debt", "inflation", "loan", "invest", "corporat", ]
    if any(x in webUrl.lower() for x in econWords):
      return True
  return False


# MARK: - Main

parseWarcFiles()






# MARK: - Not in use

def isFileInEnglish(record):
  if record.http_headers is not None:
    for header in record.http_headers.headers:
      if header[0] == 'Accept-Language':
        if 'en-US' in header[1]:
          return True
        else: 
          return False

def doesFileBodyContain(contents, targetPhrase):
  bodystart = '<body'
  bodyend = '</body'
  pagebody = contents[contents.find(bodystart)+len(bodystart):contents.rfind(bodyend)]
  return targetPhrase in contents
  # idea: it actually takes a long time to parse the body of articles. we can probably tell more from just the titles of them?
  #odds are, if the page contains one of these words, it will be an english page. no need to check for english on top of that