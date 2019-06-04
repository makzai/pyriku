import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time


# 给我一个url，返回一个请求对象
def handle_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    return urllib.request.Request(url=url, headers=headers)


def get_url(url):
    request = handle_request(url)
    # 发送请求，获取响应
    content = urllib.request.urlopen(request).read().decode('utf8')
    # time.sleep(2)
    # 使用bs解析内容,生成soup对象
    soup = BeautifulSoup(content, 'lxml')
    # print(soup)

    ret = soup.find('a', class_='btn1 gaEvtTg')
    if ret != None:
        print(ret.string)
    else:
        ret = soup.find('a', class_='btn1 dgray')
        if ret != None:
            print(ret.string)
    # # 查找所有的章节链接对象
    # a_list = soup.select('.book-mulu > ul > li > a')
    # # print(ret)
    # # print(len(ret))
    # # 打开文件
    # fp = open('三国演义.txt', 'w', encoding='utf8')
    # # 遍历所有的a对象
    # for oa in a_list:
    #     # 取出这个a的内容
    #     title = oa.string
    #     # 取出a的href属性
    #     href = 'http://www.shicimingju.com' + oa['href']
    #
    #     print('正在下载%s......' % title)
    #     # 向href发送请求，直接获取到解析之后的内容
    #     neirong = get_neirong(href)
    #     print('结束下载%s' % title)
    #     time.sleep(2)
    #     string = '%s\n%s' % (title, neirong)
    #     # 将string写入到文件中
    #     fp.write(string)
    #
    # fp.close()


def get_neirong(href):
    # 向href发送请求，获取响应，解析响应，返回内容
    request = handle_request(href)
    content = urllib.request.urlopen(request).read().decode('utf8')
    # 生成soup对象，提取章节内容
    soup = BeautifulSoup(content, 'lxml')
    # 找包含章节内容的div
    odiv = soup.find('div', class_='chapter_content')
    neirong = odiv.text
    return neirong


def main():
    url = 'http://chn.lottedfs.cn/kr/product/productDetailInfoAjax?prdNo=10003094505&prdOptNo=10003094505'
    # 解析第一个页面，返回所有的章节列表
    get_url(url)


if __name__ == '__main__':
    main()