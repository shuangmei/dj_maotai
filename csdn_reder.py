import requests,re,timefrom concurrent.futures import ProcessPoolExecutorfrom threading import Thread, Lockheaders = {    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",    "Accept": "text/html,application/xhtml+xml,application/xml;"              "q=0.9,image/webp,image/apng,*/*;"              "q=0.8,application/signed-exchange;"              "v=b3",    "Connection": "keep-alive"}url_list = ["https://blog.csdn.net/weixin_42849517"]class CSDN_reader(object):    def __init__(self):        self.url_list = ["https://blog.csdn.net/weixin_42849517"]        self.headers = {            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",            "Accept": "text/html,application/xhtml+xml,application/xml;"                      "q=0.9,image/webp,image/apng,*/*;"                      "q=0.8,application/signed-exchange;"                      "v=b3",            "Connection": "keep-alive"}        self.get_real_article_list = []    def get_headers(self):        import random        user_agent_list = [            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36"            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0"            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36"            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36"            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"            "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"            "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0"            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"            "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01"            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0"            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36"            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36"            "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F"            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"        ]        headers = {            "Accept": "text/html,application/xhtml+xml,application/xml;"                      "q=0.9,image/webp,image/apng,*/*;"                      "q=0.8,application/signed-exchange;"                      "v=b3",            "Connection": "keep-alive",            'Accept-Language': 'en',            'User-Agent': random.choice(user_agent_list)        }        return headers    def get_proxy(self):        return requests.get("http://127.0.0.1:5010/get/").json()    def delete_proxy(self,proxy):        return requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))    def get_real_article_list(self):        for one_url in self.url_list:            resp = requests.get(one_url, headers=self.headers)            content = resp.text            pattern = re.findall(r'https://blog.csdn.net/weixin_42849517/article/details/+.\d{7,15}', content)            str = u''            article_list = set(pattern)            real_article_list = []            for one in article_list:                a = requests.get(one, headers=self.headers)                if a.status_code == 200:                    real_article_list.append(one)            return real_article_list    def run(self):        print("--------------start---------------")        for one_url in self.get_real_article_list:            proxy = self.get_proxy().get("proxy")            try:                headers = self.get_headers()                html = requests.get(one_url, headers=headers, proxies={"http": "http://{}".format(proxy)},                                    timeout=10)                # 使用代理访问                time.sleep(1)            except BaseException as  e:                # 删除代理池中代理                print(e)                self.delete_proxy(proxy)                continue                pass        print("--------------end-------------")        return self.run()def get_real_article_list(url_list,headers):    for one_url in url_list:        resp = requests.get(one_url, headers=headers)        content = resp.text        pattern = re.findall(r'https://blog.csdn.net/weixin_42849517/article/details/+.\d{7,15}', content)        article_list = set(pattern)        real_article_list = []        for one in article_list:            a = requests.get(one, headers=headers)            if a.status_code == 200:                real_article_list.append(one)        return real_article_listif __name__ == '__main__':    headers = {        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",        "Accept": "text/html,application/xhtml+xml,application/xml;"                  "q=0.9,image/webp,image/apng,*/*;"                  "q=0.8,application/signed-exchange;"                  "v=b3",        "Connection": "keep-alive"}    url_list = ["https://blog.csdn.net/weixin_42849517"]    real_article_list = get_real_article_list(url_list,headers)    work_count = 10    threads = []    for _ in range(work_count):        new = CSDN_reader()        new.get_real_article_list = real_article_list        new.headers = headers        thread1 = Thread(target=new.run, args=())        threads.append(thread1)        thread1.start()    for t in threads:        t.join()    # for _ in range(5):    #     new = CSDN_reader()    #     new.get_real_article_list = real_article_list    #     new.run()    # with ProcessPoolExecutor(work_count) as pool:    #     for i in range(work_count):    #         pool.submit(getHtml())