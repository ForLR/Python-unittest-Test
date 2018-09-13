import datetime;
import os;


def File_url(path,method):
    nowName='\\'+path+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    today=method+'\\'+datetime.datetime.now().strftime('%Y%m%d')
    report_path = os.path.join('D:\Test_log', today)
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    fileurl=''.join([nowName,".html"])
    fileurl=''.join([report_path,fileurl])
    return fileurl;
def config_url():
    url=''.join([os.path.abspath('.'),'\config'])
    if not os.path.exists(url):
        os.makedirs(url)
    url=url+'\\Setting.txt';
    return url;
def phoho_code_url():
    url=''.join([os.path.abspath('.'),'\config'])
    if not os.path.exists(url):
        os.makedirs(url)
    url=url+'\\send_phone_code.txt';
    return url;
def config(datas):
    with open(config_url(),'w') as fp:
        fp.write(datas);
def getconfig(types):#获取登录商户指定信息
    with open(config_url(),'r') as f:
       return eval(f.readline())[types]
def appendconfig(datas={}):
    with open(config_url(),'r') as f:
         seeting=eval(f.readline())
         for k,v in datas.items():
            seeting[k]=v;
         config(str(seeting))
def phone_code(types):#获取登录商户指定信息
    with open(phoho_code_url(),'r') as f:
       return eval(f.readline())[types]
