
import unittest;
import HTMLTestRunner;
import excelPar;
import httpRequest;
from nose_parameterized import parameterized;
import json;
import files;
path='D:\Wallex.xlsx';
r=excelPar.excelHelp(path,excelPar.sheet_names(path)[0])
class Testone(unittest.TestCase):
    @parameterized.expand(r.listvalue)
    def test_系统模块(self,*lists):
       mode=dict(zip(r.p,list(lists))) #列表转字典
       url=mode['url'];
       method=mode['method'];
       response=r.responsedict(mode['response']);
       sendcode={}
       del mode['method'];
       del mode['url'];
       del mode['response'];
       mode['phone']='+'+str(mode['phone'])
       if mode['annotation']=='注册' or mode['annotation']=='修改支付密码' or mode['annotation']=='忘记密码更改密码':
           sendcode['phone']=mode['phone']
           code__url=None;
           if mode['annotation']=='注册':
               code__url="send_register_code"
           elif mode['annotation']=='修改支付密码':
               mode['token']=files.getconfig('token') if mode['token']=='' else mode['token']
               mode['appid']='F55EF6EC-5D84-4B52-95A7-E34FA365EFED'
               sendcode['token']=mode['token']
               code__url="send_reset_paypassword_code_url";
           elif  mode['annotation']=='忘记密码更改密码':
               code__url="forget_password";
           messeage=json.loads(httpRequest.requestHttp.returnResponse(url=files.phone_code(code__url),param=sendcode,method='post'));
           code=input("请输入手机收到的"+mode['annotation']+"验证码")
           if not messeage['success']:
               self.assertTrue(messeage['success'],"发送"+mode['annotation']+"验证码，错误为"+messeage['msg'])
           mode['code']=code
       elif  mode['annotation']=='登陆':
           mode['username']='+'+str(mode['username'])
           mode['appid']='F55EF6EC-5D84-4B52-95A7-E34FA365EFED'
       elif mode['annotation']=='设置支付密码'or mode['annotation']=='验证支付密码是否正确':
           mode['token']=files.getconfig('token') if mode['token']=='' else mode['token']
        

       returnstr=json.loads(httpRequest.requestHttp.returnResponse(url=url,param=r.getpar(mode),method=method));
       if mode['annotation']=='登陆' and returnstr['success']==True:
           files.config(str(returnstr)) 
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
        print("请依次输入手机收到的注册，修改支付密码,忘记密码的验证码")
        suite = unittest.TestSuite()#创建测试套件
        #suite.addTest('test_1.py')
        all_cases = unittest.defaultTestLoader.discover('.','test_*.py')
        #找到某个目录下所有的以test开头的Python文件里面的测试用例
        for case in all_cases:
            suite.addTests(case)#把所有的测试用例添加进来
        with open(files.File_url('one',"Wallex"),'wb') as fp:#打开一个保存结果的html文件
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='all_tests',description='所有测试情况')
            runner.run(suite)
        #unittest.main();
    except : 
        pass



