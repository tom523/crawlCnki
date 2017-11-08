# crawlCnki
爬取知网论文
```
504
HTTP Error 504: Gateway Time-out
Traceback (most recent call last):
  File "C:/code/cnkiCrawl/crawl_cnki.py", line 108, in <module>
    crawler.download_paper(treedata, opener, localdir)
  File "C:\code\cnkiCrawl\crawler.py", line 60, in download_paper
    fail_log.write(paper_title + str(error) + str(error.code))
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-15: ordinal not in range(128)
```
