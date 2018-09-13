
import unittest;
import HTMLTestRunner;
import excelPar;
import httpRequest;
from nose_parameterized import parameterized;
import json;
import files;
import requests;

path='D:\Wallex.xlsx';
r=excelPar.excelHelp(path,excelPar.sheet_names(path)[3])
class Testone(unittest.TestCase):

    @parameterized.expand(r.listvalue)
    def test_外部账户模块(self,*lists):
        mode=dict(zip(r.p,list(lists))) #列表转字典
        url=mode['url'];
        method=mode['method'];
        response=r.responsedict(mode['response']);

        del mode['method'];
        del mode['url'];
        del mode['response'];
        mode['token']=files.getconfig('token') if mode['token']=='' else mode['token']
        if mode['annotation']=='获取外部账户流水':
            mode['page_index']=1
            mode['page_size']=5
        elif  mode['annotation']=='设置外部账户别名':
            mode['account_id']=files.getconfig('out_accounts_id') if mode['account_id']=='' else mode['account_id']
        elif mode['annotation']=='增加外部账户':
            for k,v in mode.items():
                if v!='' and type(v)==str:
                    if v[0]=='{' and v[-1]=='}':
                        #print(k,eval(v))
                        mode[k]=eval(v)
        elif mode['annotation']=='解除绑定':
            mode['account_id']=files.getconfig('out_accounts_id') if mode['account_id']=='' else mode['account_id']
        returnstr=json.loads(httpRequest.requestHttp.returnResponse(url=url,param=r.getpar(mode),method=method));

        if mode['annotation']=='获取外部账户列表' and returnstr['success']==True :
            files.appendconfig({'out_accounts_id':returnstr['out_accounts'][0]['id']})
        responsekey=list(response.keys())
        responsevalue=list(response.keys())
        strkey= returnstr.keys();
        for x in range(len(response.keys())):
           if responsekey[x] in strkey:
               if type(returnstr[responsekey[x]])==dict:
                   self.assertEqual(eval(response[responsekey[x]]),returnstr[responsekey[x]],mode['annotation']+'内容不一样.系统返回的msg为:'+str(returnstr['msg']))
               elif type(returnstr[responsekey[x]])==list:
                   for y in returnstr[responsekey[x]]:
                       for i in eval(response[responsekey[x]]):
                           #print(i in y.keys())
                           if i in y.keys():
                               if(eval(response[responsekey[x]])[i] in list(y.values())):
                                    self.assertIn(eval(response[responsekey[x]])[i], list(y.values()))
                           else:
                               self.assertIs(i,y.keys(),mode['annotation']+'键不存在.系统返回的msg为:'+str(returnstr['msg']))
                       #print(list(eval(response[responsekey[x]]).keys()) , list(y.keys()))
                   #self.assertIn(eval(response[responsekey[x]]),returnstr[responsekey[x]],'不存在返回值中.系统返回的msg为:'+str(returnstr['msg']))
               else:
                   self.assertEqual(response[responsekey[x]].upper(),str(returnstr[responsekey[x]]).upper(),mode['annotation']+'返回值不一致.系统返回的msg为:'+str(returnstr['msg']))
           else:
               self.assertIn(responsekey[x],strkey,mode['annotation']+'键不存在.系统返回的msg为:'+str(returnstr['msg']))

if __name__ == '__main__':
    try:
        unittest.main();
    except : 
        pass


