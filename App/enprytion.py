import time
import hashlib
from Crypto.Cipher import AES
import base64


def MD5_sign():
    """
    生成MD5数字签名并返回
    """
    key = "wahaha"
    now_time = time.time()      # 获取当前时间
    client_time = str(now_time).split('.')[0]  # 转换为字符串，截取小数点前

    # 生成MD5签名
    hash = hashlib.md5()
    sign = client_time + key
    sign_utf8 = sign.encode(encoding='utf-8')
    hash.update(sign_utf8)
    sign_md5 = hash.hexdigest()
    md5_sign = "%s|%s" %(sign_md5, client_time)

    return md5_sign


def encryptAES(src):
    """
    AES加密函数
    """
    key = "qwertyuiopasdfgh"
    iv = b"1234567890123456"    # 初始化向量
    block = 16  # 密码块要求16位,该数据用于计算填充补位
    aes = AES.new(key, AES.MODE_CBC, iv)   # 初始化加密器
    # 如果s不足16位，进行填充。填充模式：PKCS#5/PKCS7
    pad = lambda s: s + (block-len(s)%block) * chr(block-len(s)%block)
    src = aes.encrypt(pad(src))    # 进行AES加密
    return base64.urlsafe_b64encode(src)    # 二次转换，便于传输

