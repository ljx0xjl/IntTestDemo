import os
import hashlib
import json
import sys
import pytest
import requests
import getCase
import enprytion


# 获取测试数据
excel = getCase.getCase().get_xls()

class TestApi(object):
    # 装饰器，实现参数化
    @pytest.mark.parametrize('num, api_name, description, api_host, request_url, request_method, request_data, enprytion_method, check_point, active', excel)
    # 测试用例
    def test_api(self, num, api_name, description, api_host, request_url, request_method, request_data, enprytion_method, check_point, active):
        # 拼接出完整请求地址
        url = api_host.replace('\n', '').replace('\r', '') + request_url
        # 以防万一，如果用例未激活则跳过
        if active == "no":
            pytest.skip("active为no，跳过该测试用例")
        elif active == "yes":
            # 处理GET请求
            if  request_method == "GET":
                # 如果请求需要MD5签名
                if enprytion_method == 'MD5':
                    data = json.loads(request_data)
                    sign = enprytion.MD5_sign()
                    data.update(md5_sign=sign)
                    session = requests.Session()
                    # 禁止代理服务
                    session.trust_env = False
                    r = session.get(url, params=data)
                else:
                    session = requests.Session()
                    session.trust_env = False
                    r = session.get(url, params=request_data)
                
            # 处理POST请求
            elif request_method  == "POST":
                data = json.loads(request_data)
                session = requests.Session()
                session.trust_env = False
                # AES加密处理
                if enprytion_method == 'AES':
                    encoded = enprytion.encryptAES(json.dumps(data)).decode()
                    r = session.post(url, data={'data': encoded})
                # 未加密请求
                elif enprytion_method == 'no':
                    r = session.post(url, data=data)

            # result保存响应值
            result = r.json()
            # 检查
            assert result['status'] == int(check_point.split(':', 1)[0])
            assert result['message'] == check_point.split(':', 1)[1]

if __name__ == '__main__':
    os.system('pytest -q test_main.py --html=../Report/hehe.html --self-contained-html')
