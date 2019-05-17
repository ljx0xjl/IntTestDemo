import os

class GetPath():
    def __init__(self):
        # 获取当前文件所在目录
        self.current_dir =  os.path.split(os.path.realpath(__file__))[0]
        # 获取App文件夹路径
        self.app_dir = os.path.abspath(os.path.dirname(self.current_dir))
        # 获取项目的根目录路径
        self.project_dir = os.path.abspath(os.path.dirname(self.app_dir))

    def get_conf_path(self):
        """
        返回config.ini文件路径
        """
        path = os.path.join(self.project_dir, 'config.ini')
        return path

    def get_log_path(self):
        """
        返回logs.txt文件路径
        """
        path = os.path.join(self.project_dir, 'logs.txt')
        return path
 

    def get_case_dir(self):
        """
        返回测试用例文件存放目录
        """
        dir = os.path.join(self.project_dir, 'TestCase')
        return dir

    def get_report_dir(self):
        """
        返回测试报告存放目录
        """
        dir = os.path.join(self.project_dir, 'Report')
        return dir


if __name__ == '__main__':
    print(GetPath().get_conf_path())
    print(GetPath().get_case_dir())
    print(GetPath().get_report_dir())
    print(GetPath().get_log_path())
