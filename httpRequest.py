import requests
from requests.cookies import RequestsCookieJar
import json;
class requestHttp:
        def returnResponse(url, param, headers={'Content-Type':'application/json'}, cookies={},method='get'):
            if method=='get':
                return requests.get(url,json.dumps(param), headers=headers, cookies=cookies).text
            else:
                return requests.post(url,json.dumps(param), headers=headers, cookies=cookies).text
        def returnCookie(url):
            res = requests.get(url)
            return res.cookies.get_dict();
class HttpHelp:   
        def __init__(self,url, param, headers="", cookies={}, json="",method='get'):
            self.cookie_jar=requests.cookies.RequestsCookieJar();
            self.r=None;
            for k,v in cookies.items():
                self.cookie_jar.set(k,v)
            if method=='get':
                self.r= requests.get(url,param, json=json, headers=headers)
            else:
                self.r= requests.post(url,param, json=json, headers=headers)
            self.r.cookies.update(self.cookie_jar)
            
        def returnResponse(self):
            return self.r
        def returnCookie(self):
            return self.r.cookies.get_dict();
