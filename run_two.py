
import unittest;
import HTMLTestRunner;
from nose_parameterized import parameterized;
import files;
if __name__ == '__main__':
        suite = unittest.TestSuite()#创建测试套件
        #suite.addTest('test_1.py')
        all_cases = unittest.defaultTestLoader.discover('.','Casetest_*.py')
        #找到某个目录下所有的以test开头的Python文件里面的测试用例
        for case in all_cases:
            suite.addTests(case)#把所有的测试用例添加进来
        with open(files.File_url('two'),'wb') as fp:#打开一个保存结果的html文件
            runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='all_tests',description='所有测试情况')
            runner.run(suite)
        #unittest.main();

