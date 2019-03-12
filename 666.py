from bs4 import BeautifulSoup
import requests
import pymongo
import json
import sys
from urllib.parse import quote


client = pymongo.MongoClient('localhost', 20018)
xiaoshuo = client['gongshang']
xiaoshuo_biquge = xiaoshuo['qiye']


# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# }
headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.creditsd.gov.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",

}

def get_content(zz):
        zz=quote(zz)
        web_txt = requests.get('http://www.creditsd.gov.cn/creditsearch.corlistace.dhtml?kw=' + zz, headers=headers, timeout=None)
        status = web_txt.status_code
        print(status)
        txt_soup = BeautifulSoup(web_txt.content, 'lxml')
        txt_title1 = txt_soup.select('.con-list li a')
        # if len(txt_title1)<=0:
        #     return False
        u = txt_title1[0].attrs["onclick"]
        z = u.split("'")[1]

        web_txt = requests.get('http://www.creditsd.gov.cn/creditsearch.cordetailace.dhtml?id=' + z, headers=headers, timeout=None)
        status = web_txt.status_code
        print(status)
        txt_soup = BeautifulSoup(web_txt.content, 'lxml')
        gongshang1 = txt_soup.select('.item-box dd')
        gongshang2 = txt_soup.select('.item-box dt')
        list={}
        inx=0
        tit_list=[""]
        for a in range(0,len(gongshang1)):
             list[gongshang2[a].text.strip()]=gongshang1[a].text.strip()
        xiaoshuo_biquge.insert_one(list)
        print("执行完毕~~~")

       
    


if __name__ == '__main__':
    if len(sys.argv)<=1:
        get_content("海尔集团公司")
    elif len(sys.argv)>=1:
        get_content(sys.argv[1])



