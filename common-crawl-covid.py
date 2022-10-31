from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys
import sys
import zlib
import urllib
import gzip
import urllib.request


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


# Read individual warc file urls into an array
f=urllib.request.urlopen(file_name) 
decompressed_data=zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
data = decompressed_data.decode('utf-8')

file_names = []
for line in data.splitlines():
  fullURL = "http://data.commoncrawl.org/" + line # + "\n"
  file_names.append(fullURL)


# Check each individual warc file for relevance
hits = 0
entries = 0
results_file = open("myfile.txt", "w")  # write mode

for file_name in file_names:
  stream = requests.get(file_name, stream=True).raw

  for record in ArchiveIterator(stream, arc2warc=True):
      if record.rec_type == "warcinfo":
          continue

      entries = entries + 1
      contents = (
          record.content_stream()
          .read()
          .decode("utf-8", "replace")
      )

      # TODO: write a more clever isRelevant(file) method
      if 'COVID' in contents:
        hits = hits + 1
        webUrl = record.rec_headers.get_header("WARC-Target-URI")
        results_file.write(webUrl + "\n")

results_file.close() 
print("Found" + str(hits) + " pages related to COVID-19 and economics out of " + str(entries) + " total pages")