# common-crawl-project

## High Level

We want to get the:
- URL

of files which:
- relate to COVID-19
- relate to economics
- are a part of the 2020 common crawl archives

Constraints I added to make the search easier to start:
- only consider pages written in English
- only consider pages written from Mar/Apr 2020 until Dec 2020. Although there are certainly pages that relate to COVID-19 and the economy in January of Feburary, they were less frequent because the pandemic was still widely thought to be contained within China until Feb 2020. 

## My Approach

func fetchRelevantFiles
  for each month in 2020, fetch the batch of warc file paths (e.g. at "http://data.commoncrawl.org/crawl-data/CC-MAIN-2020-16/warc.paths.gz")
    for each warc file path, fetch all the warc files (e.g. at "http://data.commoncrawl.org/crawl-data/CC-MAIN-2019-30/segments/1563195523840.34/warc/CC-MAIN-20190715175205-20190715200159-00000.warc.gz")
    for each warc file
      if isRelevantFile(file)
        save the file's "WARC-Target-URI" into a text file

func isRelevantFile(file) 
  see below


## Determining a File's Relevance

Our goal is to find pages meeting the three criterion above.

The 2020 criterion isn't hard to meet—we can pull pages specifically from 2020 archives.

For the other two criterion, we have options. We could check the plaintext of every single page to check for COVID and economics related words. However, searching through all of the plaintext for certain words will probably take a long time.

We could check the page's metadata, like title or headers, instead of the entire plaintext, looking for keywords. We'll probably miss a lot of relevant articles this way, but that's ok. It's equally as bad to add an irrelevant article to our list as it is to add a relevant one, so we should be more selective when possible.

We could also further restrict the types of pages we look at. We could only consider pages that are from an economics-related magazine or news site, and then look for pages on that site with COVID related terminology.

If I had more time and could continue working on this, I would combine both of the above strategies into one algorithm.


## Potential Complications

Many pages archived in a given month were not necessarily created that month. Beyond just the Common Crawl index date, it would be important to check the original publication date of the journal or the website.


## Comments

I ran into several issues while working on this problem which slowed me down quite a bit. I code primarily in Swift, so switching over to Python on my own machine took longer than I expected it to. There were a number of other smaller issues and errors that I was eventually able to figure out towards the end.

I probably spent too much time trying to get the Python code to properly run and query Common Crawl data instead of focusing on the algorithm, but alas, I was able to get it to work at the end.
