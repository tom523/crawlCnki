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

1.请求搜索结果的列表页，需要发送两次请求，带cookie
2.请求下一页时，需要修改referer,下载论文时，一样需要修改referer
3.爬取失败后，修改UA，继续从失败页码开始新爬取
4.不要太粗暴，爬取一页，休息一会儿



