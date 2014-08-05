#coding:utf-8
import re
import os
import requests  as R
from BeautifulSoup  import BeautifulSoup as BS
import multiprocessing 
import urlparse
import time
opt = "Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380"
headers = {'User-Agent':opt}
a,b = multiprocessing.Pipe() 
domain_url = "66365.m.weimob.com" 
G_queue_url = []                
G_spidered_url = []

def is_existed(file_real_path):
    i=1
    while 1: 
        if i==1:
            file_real_path_tem = file_real_path+'%s.htm'%""
        if os.path.isfile(file_real_path_tem):
            file_real_path_tem = file_real_path+'_%s.htm'%str(i) 
        else:
            return file_real_path_tem
        
        i=i+1


def get_web_page(url):
    try:
        r = R.get(url,headers=headers)
        html = r.text
    except:
        return None

    if html:
        return html
    else:
        return None

def btree(O):
    if O:
        return BS(O,fromEncoding="utf-8")
    else:
        return None

def download():
    url = "http://66365.m.weimob.com/weisite/home?pid=66365&bid=135666&wechatid=oAdrCtzBdLhgpyIOYtBNELkWXJ68&wxref=mp.weixin.qq.com"
    print 'download' 
    checked_list = []                  

    while True:
        print 'I am busy'
  

        recv_data = b.recv()
        # recv_data = [url]
        # print recv_data
        if type(recv_data)!=type([]):
            if recv_data ==0:
                break

        for url in recv_data:
            print url
            if url in checked_list:
                # checked_list.append(url)
                continue
            else:
                checked_list.append(url)

            if re.search(domain_url,url):
                url_list = urlparse.urlparse(url)
                domain_folder = url_list[1]
                file_path = url_list.path
                real_path_r = os.path.sep.join([domain_folder,file_path])
                real_path_l = re.split(r'/|\\',real_path_r)
                # print real_path_l
                if len(real_path_l)==2:
                    if not real_path_l[-1]:
                        continue
                real_path_f = os.path.sep.join(real_path_l[0:-1])
                real_path_r = is_existed(real_path_r)
                try:
                    if not os.path.exists(real_path_f) :
                        os.makedirs(real_path_f)
                        try:
                            f = open(real_path_r,'w')
                        except :
                            open(real_path_r).close()
                            f = open(real_path_r,'w')
                    else:   
                        try:
                            f = open(real_path_r,'w')
                        except :
                            open(real_path_r).close()
                            f = open(real_path_r,'w')
                    r = R.get(url)
                    content = unicode(r.text).encode(r.encoding,'ignore')
                    if not content:
                        continue
                    f.write(content)
                    f.close()
                except:
                    pass
            else:
                pass

def get_links(html):
    soup = btree(html)
    # print soup
    if not soup:
        return []
    a_links = soup.findAll('a')
    if not a_links:
        return []
    link_list = []
    for link in a_links:
        # print link
        try:
            link = link.get('href')
            if not link:
                continue
        except:
            # print link
            continue

        if not re.search(domain_url,link) and not re.search('http', link):
            link_list.append("http://"+domain_url+link)
    return link_list

def  work(url):

    global G_spidered_url
    global G_queue_url  
    # print G_spidered_url,G_queue_url
    G_spidered_url.append(url)
    html = get_web_page(url)
    all_links = get_links(html)
    send_list=[]
    if G_queue_url and all_links:
        for slink in all_links:
            if slink not in G_queue_url:
                send_list .append(slink)
                G_queue_url.append(slink)
        a.send(send_list)
    elif not G_queue_url and all_links :

        G_queue_url = all_links
        a.send(all_links)

    for url in G_queue_url:
        if url in G_spidered_url:
            continue
        else:
            G_spidered_url.append(url)
            work(url)
    a.send(0) 

def main(url):
    multiprocessing.freeze_support() 
    lock = multiprocessing.Lock()  
    w = multiprocessing.Process(target=work, args=(url, ))  
    nw = multiprocessing.Process(target=download, args=())  
    w.start()  
    nw.start()  
    w.join()  
    nw.join()  


if __name__ == '__main__':
    url= "http://66365.m.weimob.com/weisite/home?pid=66365&bid=135666&wechatid=oAdrCtzBdLhgpyIOYtBNELkWXJ68&wxref=mp.weixin.qq.com"

    import sys
    try:
        url = sys.argv[1]
    except:
        print "You have to input a complete URL"
    # main(url) 
    multiprocessing.freeze_support() 
    lock = multiprocessing.Lock()  
    w = multiprocessing.Process(target=work, args=(url, ))  
    nw = multiprocessing.Process(target=download, args=())  
    w.start()  
    nw.start()  
    w.join()  
    nw.join()  




 
