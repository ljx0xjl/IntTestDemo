import os
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from .getPath import GetPath


class SendEmail():
    def __init__(self):
        # config.ini文件存放路径
        config_path = GetPath().get_conf_path()
        # 读取配置文件config.ini 
        config = configparser.ConfigParser()
        config.read(config_path)
        self.receiver = config.get('email', 'receiver')    # 获取[email]中指定的收件人
        self.subject = config.get('email', 'subject')     # 获取[email]中指定的主题

        self.username = os.environ.get('username')   # 获取邮箱账户
        self.password = os.environ.get('password')   # 获取邮箱密码


    def sendEmail(self, fname):
        """
        发送邮件
        """
        # 测试报告文件完整路径
        report_path = os.path.join(GetPath().get_report_dir(), fname)

        msg = MIMEMultipart()
        msg["from"] = self.username
        msg["to"] = self.receiver 
        msg["subject"] = self.subject + ': ' + fname

        # 装载附件
        part = MIMEApplication(open(report_path, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=fname)
        msg.attach(part)

        # 发送
        s = smtplib.SMTP("smtp.sina.com", timeout=30)
        s.login(str(self.username), str(self.password))
        s.sendmail(self.username, self.receiver, msg.as_string())
        s.close
        print("测试报告%s，已发送！"%fname)

