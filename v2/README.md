# common-crawl-project, v2 Updates

Each of the ten crawled_results files contains 100 pages relevant to COVID-19's economic imipact pulled from the May and June 2020 Common Crawl archive.

## Improvements from v1

Pages were deeemd a hit if their url contains the word "covid" as well as one economics-related word in English.

This has several advantages over v1:
- **Increased speed.** Before, we checked the page's body for text containing economics-related words. The body is significantly longer than the url so iterating through the text in the page's body takes considerably more time.
- **Decreased irrelevant pages.** Often, the page's body is riddled with other hyperlinks and ads which could easily contain COVID-19 or an economics related word. It is difficult to extract only the body of the page, because each page has a significantly different format. Furthermore, there is a greater likelyhood that the body of the page contains an economics-related word without economics being a central theme of the page.
- **Increased relevant pages.** The URL contains two key components: the title of the page's source and the title of the page itself. By checking the page's source for economics-related words, we can include all posts about COVID-19 from papers like "The Economist" which are almost certain to be relevant. Furthermore, it turns out the title of the page is actually the best indication for its theme. The theme of "economic impact of COVID-19" is specific enough that there's a high likelihood that a page's title contains the word "COVID" and one economics-related word. We're fine passing on the occasional page which is only tangentially related to COVID's economic impact.

Pages were pulled from the May and June 2020 archive. Because we're aiming for 1000 pages, and given the sheer amount of data per archive, just pulling from one month's archive was enough.

Pages were accepted even if not written in English. Because we determine a page's relevance by the presence of certain economic-related root words, in English, in the url, the odds are high than the page will be written in English, and doing an explicit html-language check is just slightly more cosltly.


## Room for Improvement

If we wanted to turn this script into a useful tool, I would improve its customization and performance.

Customization
- Number of pages desired
- Number of pages per output file
- From what month of Common Crawl archive to begin pulling from
- If a specific language is desired (add support to non-English pages by matching each language with a set of economic root words in that language)
- If a specific publish date is desired (check the publish date on the html header)

Performance
- Add support for multithreading, and split the work sequentially between the number of available cores.

Accuracy
- Filter out strange pages like Amazon ads or WhatsApp message group public links by looking at the page's content type.
- Add an option to only include pages which are currently still useful. Many pages were useful two years ago but now appear dead.