import sys,time
import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    "Host":"q.10jqka.com.cn",
    "Accept-Encoding":"gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def __get_page_num(first_url):
    ctx = requests.get(first_url, headers=header)
    soup = BeautifulSoup(ctx.text, 'lxml')
    temp = soup.select_one("span.page_info").text
    return int(temp.split("/")[1])


def __format_code(code):
    if code.startswith('6'):
        return f"SHSE.{code}"
    else:
        return f"SZSE.{code}"


def __parse(url):
    """

    @param url:
    @return:
    """
    result = []
    ctx = requests.get(url, headers=header)
    retry_cnt = 0
    while ctx.status_code!=200 and retry_cnt<=3:
        time.sleep(5)
        ctx = requests.get(url, headers=header)
        retry_cnt += 1

    soup = BeautifulSoup(ctx.text, 'lxml')
    trs = soup.find_all("tr")
    trs = trs[1:]
    for tr in trs:
        tds = tr.find_all("td")
        code = tds[1].text
        code = __format_code(code)
        name = tds[2].text
        result.append((code, name))
    return result

if __name__=="__main__":
    gnurl = "http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code/{}"
    hyurl = "http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}"

    urls = {
        "gn": gnurl,
        "hy":hyurl,
    }

    cls = sys.argv[1]  # 大分类
    code = sys.argv[2] # 概念，行业代码
    base_url = urls[cls]
    url = base_url.format(1,code)
    page_num = __get_page_num(url)
    #print(page_num)
    code_name_result = []
    for i in range(1, page_num+1):
        #print(i)
        url_i = base_url.format(i, code)
        code_name_result.extend((__parse(url_i)))
        time.sleep(3)

    for code, name in code_name_result:
        print(f"{code},{name}")
