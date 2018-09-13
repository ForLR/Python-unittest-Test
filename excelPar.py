import xlrd;
from nose_parameterized import parameterized;
import json;
def get_xls(xls_name, sheetname):
    cls = []
    fi = xlrd.open_workbook(xls_name)
    sheet = fi.sheet_by_name(sheetname)
    return sheet; 
def param(rows,cols,sheetname):
     lists=[];
     for x in range(cols):
             lists.append(sheetname.cell_value(0,x))
     return lists;
def par(rows,cols,sheetname):
    data=[]
    for i in range(rows):
        if(i==0):continue;
        dict={}
        for y in range(cols):
            ctype = sheetname.cell(i, y).ctype  # 表格的数据类型
            cell = sheetname.cell_value(i,y)
            if ctype == 2 and cell % 1 == 0:  # 如果是整形
                cell = int(cell)
            elif ctype == 3:
                    # 转成datetime对象
                date = datetime(*xldate_as_tuple(cell, 0))
                cell = date.strftime('%Y/%d/%m %H:%M:%S')
            elif ctype == 4:
                cell = True if cell == 1 else False
            dict[sheetname.row_values(0)[y]]=cell;
        data.append(dict) 
    return data;
def sheet_names(path):
    return  xlrd.open_workbook(path).sheet_names();

class excelHelp:
    def __init__(self,path,sheet):#path 为excel路径 sheet为表名
        self.path=path
        self.xls=get_xls(path,sheet);
        self.rows=self.xls.nrows;#行
        self.cols=self.xls.ncols;#列
        self.params=par(self.rows,self.cols,self.xls);
        self.p=param(self.rows,self.cols,self.xls);#excel第一行 键 或者url ，method ，response
        self.lists=[];#键
        self.listvalue=[]#值
        for x in range(len(self.params)):
            self.lists.append(self.params[x].keys())
            self.listvalue.append(self.params[x].values())

    def responsedict(self,strs=''):#获取excel中response的字符串转为dict
        response={} 
        if len(strs)>0:
            s=strs.split('。')
            for x in range(len(s)):
                li=s[x].split('=');
                response[li[0]]=li[1];
        return response;
    def getpar(self,mode={}):#所有参数
         par={};
         for x in range(len(mode)):
             try:
                 if(type(mode[list(mode.keys())[x]])!=int):
                    if (len(mode[list(mode.keys())[x]])!=0):
                       par[list(mode.keys())[x]]=mode[list(mode.keys())[x]];
                 else:
                     par[list(mode.keys())[x]]=mode[list(mode.keys())[x]];
             except :
                pass;
         return par;
 
def get_contain_dict(src_data,dst_data):
  for k,v in src_data.items():
      if k in dst_data.keys():
         return dst_data[k]==src_data[k];
      else :
          return False;
