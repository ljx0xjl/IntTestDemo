import os
import sys
import configparser
from xlrd import open_workbook
from xlrd.biffh import XLRDError 
from Common.log import Log
from Common.getPath import GetPath


class getCase():
    def get_xls(self):
        '''
        读取测试用例，
        xls_name为Excel表格名称
        sheet_name为sheet的名称
        '''
        # config.ini文件存放路径
        config_path = GetPath().get_conf_path()
        # 读取配置文件config.ini 
        config = configparser.ConfigParser()
        config.read(config_path)
        # 获取[excel]中指定的file_name
        file_name = config.get('excel', 'file_name')
        # 获取[excel]中指定的sheet_name
        sheet_name = config.get('excel', 'sheet_name')

        # 测试用例文件路径:../TestCase
        case_path = os.path.join(GetPath().get_case_dir(), file_name)
        log = Log(__name__).getlog()
        # 判断用例文件是否存在
        if not os.path.isfile(case_path):
            # 记录到日志并退出python程序
            log.error("测试用例文件不存在！")
            os._exit(1)     

        file = open_workbook(case_path)     # 打开EXCEL
        sheets = sheet_name.split('|')
        cls = []    # 用于存储用例
        for s in sheets:
            try:
                sheet = file.sheet_by_name(s)   # 打开指定sheet
            except XLRDError as e:
                log.error("config.ini文件中sheet_name编辑错误")
                raise
            nrows = sheet.nrows    # sheet的行数
            for i in range(nrows):
                if sheet.row_values(i)[0] != 'Num':     # 过滤顶栏目录
                    if sheet.row_values(i)[9] != 'no':  # 过滤未激活的用例
                        cls.append(sheet.row_values(i))
        return cls


if __name__ == '__main__':
    # 打印 Num 一栏
    print(getCase().get_xls()[0][0])
    # 打印 Api name 一栏
    print(getCase().get_xls()[0][1])
    # 打印 Active 一栏
    print(getCase().get_xls()[0][9])
    # 打印全部
    print(getCase().get_xls())
