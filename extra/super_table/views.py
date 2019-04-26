import time
import json
import hashlib
import base64
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Crypto.Cipher import AES    # 用于加密解密
from super_table.models import Super_Table

# 自定义的装饰器，用于MD5解密
def md5_sign(func):
    def wrapper(request, *args, **kwargs):
        #获取客户端传来的验证信息，格式为：(客户端MD5签名)|(客户端时间戳)
        auth = request.GET.get('md5_sign', '')
        # 验证信息不能为空
        if auth == '':
            return JsonResponse({'status': 401, 'message': 'sign is empty'})
        client_md5 = auth.split('|', maxsplit=1)[0]     # 客户端传送的MD5签名
        client_time = auth.split('|', maxsplit=1)[1]        # 客户端时间戳

        now_time = time.time()      # 获取当前时间
        server_time = str(now_time).split('.')[0]  # 截取小数点前的时间，转化为字符串

        # 如果客户端请求时间与服务端手里时间超过60秒，需重新申请验证
        if int(server_time) - int(client_time) > 60:
            return JsonResponse({'status': 408, 'message': 'timeout, please try again'})
        
        # 利用客户端传送的时间戳，重新计算MD5签名,生成服务端MD5签名 
        hash = hashlib.md5()
        sign = client_time + "wahaha"       # 签名密匙为:wahaha
        sign_utf8 = sign.encode(encoding='utf-8')
        hash.update(sign_utf8)
        server_md5 = hash.hexdigest()

        # 验证客户端MD5签名与服务端MD5签名是否相符
        if server_md5 != client_md5:
            return JsonResponse({'status': 401, 'message': 'sign check fail'})
        else:
            return func(request, *args, **kwargs)

    return wrapper


# Create your views here.
def add(request):
    '''
    接收POST请求，
    添加人物信息
    '''
    key = "qwertyuiopasdfgh"  # 密匙
    iv = b"1234567890123456"    #初始化向量
    
    # 只接受POST请求
    if request.method == 'POST':
        data = request.POST.get("data", "")
    else:
        return JsonResponse({'status': 405, 'message': 'method not allowed'})

#*********************** AES解密开始 ***********************************#
    data = base64.urlsafe_b64decode(data)      # 反向客户端base64.urlsafe_b64encode()操作
    aes = AES.new(key, AES.MODE_CBC, iv)    # 初始化加密器
    data = aes.decrypt(data).decode()    # 逆向解密
    unpad = lambda s: s[0: - ord(s[-1])]      # 消除补位填充,填充模式：PKCS#5/PKCS7
    data = json.loads(unpad(data))    # 转换为字典型数据
#*********************** AES解密完成 ***********************************# 

    name = data.get('name', '')     # 人物姓名
    tel = data.get('tel', '')     # 人物联系方式
    address = data.get('address', '')     # 人物地址

    # 如果name、tel、address中某项为空，则返回“10010，参数错误”
    if name == '' or tel == '' or address == '':
        return JsonResponse({'status': 400, 'message': 'parameter error'})

    # 如果name已经存在于数据表中，返回“10020,名字已经存在”
    result = Super_Table.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 400, 'message': 'name already exists'})

    # 添加成功
    Super_Table.objects.create(name=name, tel=int(tel), address=address)
    return JsonResponse({'status': 200, 'message': 'add success'})


@md5_sign    # 自定义的装饰器，用于MD5解密
def search_by_name(request):
    '''
    接收GET请求，
    查询人物信息
    '''
    name = request.GET.get('name', '')      # 想要查询的名字

    # 查询栏不能为空
    if name == '':
        return JsonResponse({'status': 400, 'message': 'please input a name'})
    else:
        info = {}       # 查询成功时装载人物信息

        # 查询失败，姓名不存在，拋出异常
        try:
            result = Super_Table.objects.get(name=name)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 204, 'message': 'result is empty!'})
        
        # 查询成功，装载信息到info，返回
        else:
            info['name'] = result.name
            info['tel'] = result.tel
            info['address'] = result.address
            return JsonResponse({'status': 200, 'message': 'success', 'data': info})
        
