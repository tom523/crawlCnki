# -*- coding: utf-8 -*-
from lxml import etree
import urllib2


def download_paper(treedata, opener, localdir):
    '''
    传入参数：
        treedata:当前列表页的treedata数据
        opener: referer已修改为当前页
        localdir: 保存目录
    '''
    tr_node = treedata.xpath("//tr[@bgcolor='#f6f7fb']|//tr[@bgcolor='#ffffff']")

    for item in tr_node:
        paper_title = item.xpath("string(td/a[@class='fz14'])")
        paper_link = item.xpath("td/a[@class='fz14']/@href")
        paper_author = item.xpath("td[@class='author_flag']/a/text()")
        paper_source = item.xpath("td[4]/a/text()")
        paper_pub_date = item.xpath("td[5]/text()")
        paper_db = item.xpath("td[6]/text()")
        paper_cited = item.xpath("td[7]//a/text()")
        paper_download_count = item.xpath("td[8]/span/a/text()")
        print paper_title
        paper_title = paper_title.replace("\\", ""). \
            replace("/", ""). \
            replace(":", ""). \
            replace("*", ""). \
            replace("?", ""). \
            replace("\"", ""). \
            replace("<", ""). \
            replace(">", ""). \
            replace("|", "")

        # 获取paper详情页面链接，访问详情页前，要设置referer
        paper_detail_url_fake = "http://kns.cnki.net" + paper_link[0]
        print paper_detail_url_fake
        response = opener.open(paper_detail_url_fake)
        paper_detail_page_treedata = etree.HTML(response.read())
        # 下载前要设置referer为详情页
        opener.addheaders = [("Referer", response.url)]

        # 硕士论文并没有【pdf下载】的链接
        pdf_download_url = paper_detail_page_treedata.xpath('//*[@id="pdfDown"]/@href')
        if len(pdf_download_url) == 0:
            whole_book_download_url = paper_detail_page_treedata.xpath('//*[@id="DownLoadParts"]/a[1]/@href')
            download_url = whole_book_download_url[0]
            filename = localdir + paper_title + ".caj"
        else:
            download_url = pdf_download_url[0]
            filename = localdir + paper_title + ".pdf"


        try:
            response_file = opener.open(download_url)
        except urllib2.HTTPError as error:
            print error.code
            print error
            fail_log = open("C:/code/test3/pdf/log/fail.log", 'a')
            fail_log.write(paper_title + str(error) + str(error.code))
            fail_log.close()
        down_file = open(filename, 'wb')
        down_file.write(response_file.read())
        down_file.close()


