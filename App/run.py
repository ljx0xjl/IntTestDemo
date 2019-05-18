#!/usr/bin/python
import os
import datetime
import configparser
from Common.sendEmail import SendEmail
from Common.getPath import GetPath

# 当前时间
now = str(datetime.datetime.now())[0:19]
# 测试报告名
report_name = now.replace(' ', '-') + '-report.html'
# 测试报告完整路径
report_path = os.path.join(GetPath().get_report_dir(), report_name)

# config.ini文件存放路径
config_path = GetPath().get_conf_path()
# 读取配置文件config.ini
config = configparser.ConfigParser()
config.read(config_path)
# 获取[email]中指定的active值
active = config.get('email', 'active')

def run_test():
    os.system("pytest -q ./test_main.py --html=../Report/%s  --self-contained-html" %(report_name))

if __name__ == '__main__':
    run_test()
    # 如果已邮件功能激活并且测试报告成功生成
    if active == 'yes' and os.path.isfile(report_path):
        SendEmail().sendEmail(report_name)

