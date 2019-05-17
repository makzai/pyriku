import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


def main():
    p = input('prdOptNo: ')
    prdNo = '10003094505'
    # prdOptNo = '10003094505'
    prdOptNo = p
    if scan(prdNo, prdOptNo):
        print('有料')
    else:
        print('冇料')


def scan(prdNo, prdOptNo):
    url = 'http://chn.lottedfs.cn/kr/product/productDetailInfoAjax?prdNo='+prdNo+'&prdOptNo='+prdOptNo
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    request = urllib.request.Request(url=url, headers=headers)
    content = urllib.request.urlopen(request).read().decode('utf8')
    soup = BeautifulSoup(content, 'lxml')
    ret = soup.find('a', class_='btn1 gaEvtTg')
    if ret is not None:
        if ret.string == '立即购买':
            return True
    return False


if __name__ == '__main__':
    main()
