import unittest;
import HTMLTestRunner;
import excelPar;
import httpRequest;
from nose_parameterized import parameterized;
import json;
import files;
import requests;

path='D:\Wallex.xlsx';
r=excelPar.excelHelp(path,excelPar.sheet_names(path)[4])
class Testone(unittest.TestCase):

    @parameterized.expand(r.listvalue)
    def test_转账模块(self,*lists):
        mode=dict(zip(r.p,list(lists))) #列表转字典
        url=mode['url'];
        method=mode['method'];
        response=r.responsedict(mode['response']);

        del mode['method'];
        del mode['url'];
        del mode['response'];
        mode['token']=files.getconfig('token') if mode['token']=='' else mode['token']
        if mode['annotation']=='获取转账的费用费率等信息（锁汇）' or mode['annotation']=='转账':
            for k,v in mode.items():
                if v!='' and type(v)==str:
                    if v[0]=='{' and v[-1]=='}':
                        #print(k,eval(v))
                        mode[k]=eval(v)
        if mode['annotation']=='汇率是否超时' or mode['annotation']=='转账':
            mode['action_id']=files.getconfig('action_id') if mode['action_id']=='' else mode['action_id']
        if mode['annotation']=='获取转账详情':
            mode['transfer_id']=files.getconfig('transfer_id') if mode['transfer_id']=='' else mode['transfer_id']
        returnstr=json.loads(httpRequest.requestHttp.returnResponse(url=url,param=r.getpar(mode),method=method));
        if mode['annotation']=='获取转账的费用费率等信息（锁汇）'and returnstr['success']==True:
            files.appendconfig({'action_id':returnstr['action_id']})
        if mode['annotation']=='转账'and returnstr['success']==True:
            files.appendconfig({'transfer_id':returnstr['transfer']['id']})
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
        suite = unittest.TestSuite()#创建测试套件
        #suite.addTest('test_1.py')
        all_cases = unittest.defaultTestLoader.discover('.','Casetest_*.py')
        #找到某个目录下所有的以test开头的Python文件里面的测试用例
        for case in all_cases:
            suite.addTests(case)#把所有的测试用例添加进来
        with open(files.File_url('two',"Wallex"),'wb') as fp:#打开一个保存结果的html文件
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='all_tests',description='所有测试情况')
            runner.run(suite)
    except : 
        pass


