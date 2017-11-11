# -*- coding: utf-8 -*-
import time
import urllib
import urllib2
import cookielib
from lxml import etree
import random
import crawler
import sys
import global_var

# 完成记录下载失败页码，自动更换User-Agent,重新下载

def start_crawl():
    while True:
        try:
            uapools = [
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
                "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
                "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
            ]
            headers = {'Connection': 'Keep-Alive',
                       'Accept': 'text/html,*/*',
                       'User-Agent': random.choice(uapools)}

            # 发送第一次请求，发送搜索关键字
            opener = crawler.first_request("爬虫", headers)

            # 发送第二次请求，返回第一页搜索结果列表页
            first_page_response = crawler.second_request(opener, headers)

            # 如果有上次运行的记录process_record.log，从记录页码19开始运行
            print "上次在第", global_var.get_value("PAGE_NUM_PROCESSING"), "页失败"
            opener.addheaders = [("Referer", first_page_response.url)]
            page_n_response = opener.open("http://kns.cnki.net/kns/brief/brief.aspx?curpage=" + str(global_var.get_value("PAGE_NUM_PROCESSING")) + "&RecordsPerPage=20&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx")
            page_n_html = page_n_response.read()
            page_n_treedata = etree.HTML(page_n_html)
            opener.addheaders = [("Referer", page_n_response.url)]
            localdir = "C:/code/tmp/pdf/"
            crawler.start_download_from_n(page_n_treedata, opener, localdir, global_var.get_value("PAGE_NUM_PROCESSING"))
        except Exception as error:
            print error
            print "爬取到第", str(global_var.get_value("PAGE_NUM_PROCESSING")), "失败，重新等待5分钟后，重新从第",\
                str(global_var.get_value("PAGE_NUM_PROCESSING")), "页开始爬取数据"
            time.sleep(300)


global_var._init()
global_var.set_value("PAGE_NUM_PROCESSING", 1)
start_crawl()


'''

# 保存第一页的列表页并且下载该页的论文
html2 = first_page_response.read()
with open('C:/code/test3/web2.html', 'w') as e:
    e.write(html2)
treedata = etree.HTML(html2)
# 请求详情页之前把引用地址改成列表页
opener.addheaders = [("Referer", first_page_response.url)]
localdir = "C:/code/tmp/pdf/"
crawler.download_paper(treedata, opener, localdir, 1)

#获取总页数total_page_count
current_page_node = treedata.xpath('//span[@class="countPageMark"]/text()')
print "current_page_node:", current_page_node
total_page_count = current_page_node[0].split('/')[1]
print "total_page_count:", total_page_count

current_url = first_page_response.url
for page_num in range(2, int(total_page_count)+1):
    #获取下一页的链接
    print "休息2分钟。开始爬取第", str(page_num), "页"

    next_page_node = treedata.xpath('//div[@class="TitleLeftCell"]/a[last()]/@href')
    next_page_url = next_page_node[0]
    next_page_url_full = "http://kns.cnki.net/kns/brief/brief.aspx" + next_page_url
    print "第", str(page_num), "页" ,"列表页的链接：", next_page_url_full
    opener.addheaders = [("Referer", current_url)]
    try:
        # 返回的是搜索结果下一页的列表页
        next_page_response = opener.open(next_page_url_full)
    except urllib2.URLError as error:
        print error.reason
        print error
    opener.addheaders = [("Referer", next_page_response.url)]
    html = next_page_response.read()

    # 保存列表页，用于跟踪错误，命名为页码加html
    web_file = open("C:/code/cnkiCrawl/web_log/" + str(page_num) + ".html", 'w')
    web_file.write(html)
    web_file.close()

    # 修改上一页，以供请求下页时引用
    treedata = etree.HTML(html)
    current_url = next_page_response.url

    localdir = "C:/code/tmp/pdf/"
    crawler.download_paper(treedata, opener, localdir, page_num)
    
'''




