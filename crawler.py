# -*- coding: utf-8 -*-
from lxml import etree
import urllib, urllib2
import time
import cookielib
import global_var



def first_request(keywords, headers):
    # 构建第一次请求时使用的URL，发送搜索关键字
    url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx?action=&NaviCode=*&'
    parameter={'ua':'1.11'}
    parameter['formDefaultResult']=''
    parameter['PageName']='ASP.brief_default_result_aspx'
    parameter['DbPrefix']='SCDB'
    parameter['DbCatalog']='中国学术文献网络出版总库'
    parameter['ConfigFile']='SCDBINDEX.xml'
    parameter['db_opt']='CJFQ'
    parameter['db_opt']='CJFQ,CJRF,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'
    parameter['txt_1_sel']='SU$%=|'
    parameter['txt_1_value1'] = keywords
    parameter['txt_1_special1']='%'
    parameter['his']='0'
    parameter['parentdb']='SCDB'
    parameter['__']='Sun Nov 05 2017 20:09:05 GMT+0800 (中国标准时间) HTTP/1.1'
    times = time.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0800 (中国标准时间)'
    parameter['__']=times

    getdata = urllib.urlencode(parameter)


    headers['Referer']='http://kns.cnki.net/kns/brief/default_result.aspx'
    req = urllib2.Request(url + getdata, headers=headers)

    cookie = cookielib.CookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), urllib2.HTTPHandler)
    html = opener.open(req).read()

    with open('C:/code/cnkiCrawl/web_log/web1.html', 'w') as web1_file:
        web1_file.write(html)
    return opener


def second_request(opener, headers):
    # 构建第二次请求时使用的URL，请求列表页第一页
    query_string = urllib.urlencode(
        {'pagename': 'ASP.brief_default_result_aspx', 'dbPrefix': 'SCDB', 'dbCatalog': '中国学术文献网络出版总库',
         'ConfigFile': 'SCDBINDEX.xml', 'research': 'off', 't': int(time.time()), 'keyValue': '爬虫', 'S': '1'})

    url2 = 'http://kns.cnki.net/kns/brief/brief.aspx'
    req2 = urllib2.Request(url2 + '?' + query_string, headers=headers)
    # 返回的是搜索结果列表页,第一页
    result2 = opener.open(req2)
    # opener.addheaders = [("Referer", req2.get_full_url())]
    print "response:", result2.url
    print "request", req2.get_full_url()
    return result2

def download_paper(treedata, opener, localdir, page_num, page_n_response_url):
    '''
    传入参数：
        treedata:当前列表页的treedata数据
        opener: referer已修改为当前页
        localdir: 保存目录
    '''
    tr_node = treedata.xpath("//tr[@bgcolor='#f6f7fb']|//tr[@bgcolor='#ffffff']")

    if tr_node:
        paper_count = 0
        # 每一次进入详情页面都应该是从列表页进入
        opener.addheaders = [("Referer", page_n_response_url)]
        for item in tr_node:
            paper_count += 1
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
            try:
                response = opener.open(paper_detail_url_fake)
            except urllib2.HTTPError as error:
                print error.code
                print error.reason
                time.sleep(180)
                continue
            except urllib2.URLError as urlerror:
                print urlerror.reason
                time.sleep(180)
                continue
            else:
                paper_detail_page_treedata = etree.HTML(response.read())
                # 下载前要设置referer为详情页
                opener.addheaders = [("Referer", response.url)]

                # 硕士论文并没有【pdf下载】的链接
                pdf_download_url = paper_detail_page_treedata.xpath('//*[@id="pdfDown"]/@href')
            if len(pdf_download_url) == 0:
                whole_book_download_url = paper_detail_page_treedata.xpath('//*[@id="DownLoadParts"]/a[1]/@href')
                download_url = whole_book_download_url[0]
                filename = localdir + str((page_num-1)*20+paper_count) + "." + paper_title + ".caj"
            else:
                download_url = pdf_download_url[0]
                filename = localdir + str((page_num-1)*20+paper_count) + "." + paper_title + ".pdf"

            try:
                response_file = opener.open(download_url)
            except urllib2.HTTPError as error:
                print error.code
                print error
                print "没有下载成功的论文：" + paper_title.decode('utf-8').encode('gbk')
                fail_log.write(paper_title)
                fail_log.close()
            except urllib2.URLError as urlerror:
                print urlerror.reason
                fail_log = open("C:/code/cnkiCrawl/log/fail.log", 'a')
                print "没有下载成功的论文：" + paper_title.decode('utf-8').encode('gbk')
                fail_log.write(paper_title)
                fail_log.close()
            else:
                down_file = open(filename, 'wb')
                down_file.write(response_file.read())
                down_file.close()
                global_var.set_value("PAGE_NUM_PROCESSING", page_num)
                print "正在下载页码：" + str(global_var.get_value("PAGE_NUM_PROCESSING"))
                # process_record = open("C:/code/cnkiCrawl/log/process_record.log", "w")
                # process_record.write(str(page_num))
                # process_record.close()
        return True
    else:
        print "获取论文列表失败"
        return False


# 从某一页开始爬取数据,头部信息中的referer已经设置为搜索结果第一页的列表页
def start_download_from_n(treedata, opener, localdir, page_start_num):
    # 获取总页数total_page_count
    current_page_node = treedata.xpath('//span[@class="countPageMark"]/text()')
    print "current_page_node:", current_page_node
    total_page_count = current_page_node[0].split('/')[1]
    print "total_page_count:", total_page_count
    for page_num in range(page_start_num, int(total_page_count)+1):
        print "休息2分钟。开始爬取第", str(page_num), "页"
        time.sleep(120)
        page_n_url = "http://kns.cnki.net/kns/brief/brief.aspx?curpage="\
                     + str(page_num)\
                     + "&RecordsPerPage=20&QueryID=0&ID=&turnpage=1" \
                       "&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode" \
                       "&PageName=ASP.brief_default_result_aspx"
        page_n_response = opener.open(page_n_url)
        page_n_html = page_n_response.read()
        page_n_treedata = etree.HTML(page_n_html)
        # 下载出来第19页后,将referer设置为第19页的列表页
        # opener.addheaders = [("Referer", page_n_response.url)]
        # localdir = "C:/code/tmp/pdf/"
        page_n_response_url = page_n_response.url
        if not download_paper(page_n_treedata, opener, localdir, page_num, page_n_response_url):
            break
        # 爬取完成一页后，将referer设置为列表页，下一个循环爬取下一页
        opener.addheaders = [("Referer", page_n_response.url)]




