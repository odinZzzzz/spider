from bs4 import BeautifulSoup
import requests
import pymongo
import json

client = pymongo.MongoClient('localhost', 27017)
xiaoshuo = client['xiaoshuo']
xiaoshuo_biquge = xiaoshuo['biquge']


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

total_page = 11
def get_content(zz):
        web_txt = requests.get('http://www.biquge.com.tw/' + zz, headers=headers, timeout=None)
        status = web_txt.status_code
        print(status)
        txt_soup = BeautifulSoup(web_txt.content, 'lxml')
        txt_title1 = txt_soup.select('.bookname h1')
        if len(txt_title1)<=0:
            return False
        txt_title = txt_soup.select('.bookname h1')[0].text
        txt_content = txt_soup.select('#content')[0].text
        txt_count = len(txt_content)
        if txt_count > 50:
            data = {
                "title" : txt_title,
                "content" : txt_content
            }
            return data
        else:
            return False
    

def get_info(ct1,ct2):
    '''

    '''



    url = 'http://www.biquge.com.tw/%s_%s%s/'%(ct1,ct1,ct2)
    web_data = requests.get(url, headers=headers, timeout=None)
    soup = BeautifulSoup(web_data.content, 'lxml')
    nf = soup.select('#header h1')
    if len(nf)>0:
        print(url,nf[0].text)
        return False
    item = soup.select('#list a')
    info = soup.select('#info p')
    title = soup.select('#info h1')[0].text
    zz = item[0].attrs["href"]
    print(len(item))
    res_data = get_content(zz)
    if res_data ==False:
        print(title,zz,"空章呀")
    else:    
        req_data = {
            'title':title,
            'content_title':res_data['title'],
            'content':res_data['content'][0:50],
            'author':info[0].text
        }
        xiaoshuo_biquge.insert(req_data)
        print("爬取小说","《",title,"》",res_data['title'],"成功~~~")

    print('*' * 66)


if __name__ == '__main__':
    da = {
        "name":"666",
        "age":"22"
    }
    # fp=open("test.json")
    # txt_json = json.dumps(da)
    # fp.write(txt_json)
    # zz = fp.read()
    # print(zz)
    # fp.close()
    # from threading import Timer
    # def func1():
    #     print('Do something.')
    #     global timer
    # timer = Timer(3, func1)
    # timer.start()

    # print("请问你是否需要退出？")
    # global i
    # i = "N"
    # while  i!="Y" or i!='y':
    #     i=input("请输入Y/N:")
    for a in range(1,21):
            for b in range(10):
                _b="000"
                if b<10:
                    _b='00'+str(b)
                elif b<100:
                    _b='0'+str(b)
                else:
                    _b=str(b)
                print('a:%s,b:%s'%(a,_b))
                get_info(str(a),_b)

