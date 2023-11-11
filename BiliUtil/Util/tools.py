# coding=utf-8
import json
import os
import re
import subprocess
from urllib import parse

import aiohttp
from fake_useragent import UserAgent


# from BiliUtil import http_proxy, https_proxy
class FetchConfig:
    ALL = 0


class Config:
    SET_AS_NAME = 1
    SET_AS_CODE = 2
    SET_AS_PAGE = 3

    HTTP_PROXY = None  # http://user:pass@1.2.3.4:5678
    HTTPS_PROXY = None  # https://user:pass@1.2.3.4:5678

    class Quality:
        V360P = ('16', '流畅 360P')
        V480P = ('32', '清晰 480P')
        V720P = ('64', '高清 720P')
        V720P60 = ('74', '高清 720P60')
        V1080P = ('80', '高清 1080P')
        V1080Px = ('112', '高清 1080P+')
        V1080P60 = ('116', '高清 1080P60')
        V4K = ('120', '超清 4K')
        INDEX = {
            16: V360P,
            32: V480P,
            64: V720P,
            74: V720P60,
            80: V1080P,
            112: V1080Px,
            116: V1080P60,
            120: V4K
        }


# ##################  Private  ###################

HEADER = {
    'Host': '',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': '',
    'Origin': 'https://www.bilibili.com',
    'Referer': '',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
USER = {
    'url': 'http://api.bilibili.com/x/space/wbi/acc/info',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com'
}
USER_VIDEO = {
    'url': 'http://api.bilibili.com/x/space/wbi/arc/search',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com'
}
ALBUM = {
    'url': 'http://api.bilibili.com/x/web-interface/view',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/video'
}
VIDEO = {
    'url': 'http://api.bilibili.com/x/player/playurl',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/video'
}
CHANNEL = {
    'url': 'http://api.bilibili.com/x/space/channel/video',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com'
}
CHANNEL_LIST = {
    'url': 'http://api.bilibili.com/x/space/channel/list',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com'
}

alphabet = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"


def bv2av(bv):
    bv = str(bv)
    r = 0
    for i, v in enumerate([11, 10, 3, 8, 4, 6]):
        r += alphabet.find(bv[v]) * 58 ** i
    return str((r - 0x2_0840_07c0) ^ 0x0a93_b324)


def av2bv(av):
    av = str(av)
    if av.startswith("av"):
        av = str(av[2:])
    else:
        av = int(av)
    x = (av ^ 0x0a93_b324) + 0x2_0840_07c0
    r = list('BV1**4*1*7**')
    for v in [11, 10, 3, 8, 4, 6]:
        x, d = divmod(x, 58)
        r[v] = alphabet[d]
    return str(''.join(r))


def to_bv(vid):
    vid = str(vid)
    if vid.startswith("BV"):
        return vid
    else:
        return av2bv(vid)


def to_av(vid):
    vid = str(vid)
    if vid.startswith("BV"):
        return bv2av(vid)
    elif vid.startswith("av"):
        return str(vid[2:])
    else:
        return vid


def http_header(info_obj):
    header = HEADER.copy()
    header['Host'] = parse.urlparse(info_obj['url']).netloc
    header['User-Agent'] = UserAgent().random
    header['Origin'] = info_obj['origin']
    header['Referer'] = info_obj['referer']
    return header


async def http_get(info_obj, params, cookie=None):
    # 获取请求头信息
    new_http_header = http_header(info_obj)

    # 设定Cookies信息
    if cookie is not None:
        if isinstance(cookie, dict):
            cookie = {
                'SESSDATA': cookie['SESSDATA']
            }
        elif isinstance(cookie, str) and len(cookie) > 0:
            for line in cookie.split(';'):
                name, value = line.strip().split('=', 1)
                if name == 'SESSDATA':
                    cookie = {
                        'SESSDATA': value
                    }
                    break
        else:
            cookie = dict()
    else:
        cookie = dict()

    # 尝试进行网络连接
    async with aiohttp.ClientSession() as session:
        async with session.get(url=info_obj['url'], params=params, cookies=cookie,
                               headers=new_http_header, timeout=5) as response:
            http_result = await response.text()

    # 尝试理解并验证响应数据
    try:
        json_data = json.loads(http_result)
    except json.decoder.JSONDecodeError:
        raise RunningError('请求响应无法解析：{}'.format(http_result))

    if 'code' in json_data and json_data['code'] == 0:
        return json_data
    elif 'status' in json_data and json_data['status'] is True:
        return json_data
    elif json_data['code'] == -404 or json_data['code'] == -403:
        raise RunningError('请求对象异常或被锁定，无法获取')
    else:
        raise ConnectError('网络响应状态异常，HTTP响应码：{}'.format(response.status))


def legalize_name(name):
    legal_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s']", '_', name)
    legal_name = re.sub(r'[‘’]', '_', legal_name)
    if len(legal_name) == 0:
        return 'null'
    return legal_name


async def aria2c_pull(aid, path, name, url_list, show_process=False):
    # 设置输出信息
    out_pipe = None if show_process else subprocess.PIPE

    # 读取代理信息
    http_proxy = Config.HTTP_PROXY if Config.HTTP_PROXY is not None else ""
    https_proxy = Config.HTTPS_PROXY if Config.HTTPS_PROXY is not None else ""

    proxies = f' --http-proxy="{http_proxy}"' if http_proxy else ""
    proxies += f' --https-proxy="{https_proxy}"' if https_proxy else ""

    referer = f'https://www.bilibili.com/video/av{aid}'
    url = ' '.join(f'"{u}"' for u in url_list)
    shell = f'aria2c -c -k 1M -x {len(url_list)} -d "{path}" -o "{name}" --referer="{referer}" {proxies} {url}'

    process = subprocess.Popen(shell, stdout=out_pipe, stderr=out_pipe, shell=True)
    process.wait()


async def ffmpeg_merge(path, name, show_process=False):
    if show_process:
        out_pipe = None
    else:
        out_pipe = subprocess.PIPE
    flv_file = os.path.abspath('{}/{}.flv'.format(path, name))
    aac_file = os.path.abspath('{}/{}.aac'.format(path, name))
    mp4_file = os.path.abspath('{}/{}.mp4'.format(path, name))
    if os.path.exists(flv_file) and os.path.exists(aac_file):
        shell = 'ffmpeg -i "{}" -i "{}" -c copy -f mp4 -y "{}"'
        shell = shell.format(flv_file, aac_file, mp4_file)
        process = subprocess.Popen(shell, stdout=out_pipe, stderr=out_pipe, shell=True)
        process.wait()
        os.remove(flv_file)
        os.remove(aac_file)
    elif os.path.exists(flv_file):
        os.rename(flv_file, mp4_file)
    else:
        raise RunningError('找不到下载的音视频文件')


global_cookie: str = ""


def set_cookie(_cookie: str):
    global global_cookie
    global_cookie = _cookie


def get_cookie() -> str:
    global global_cookie
    return global_cookie


from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests

mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]


def getMixinKey(orig: str):
    """对 imgKey 和 subKey 进行字符顺序打乱编码"""
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]


def encWbi(params: dict, img_key: str, sub_key: str):
    """为请求参数进行 wbi 签名"""
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: ''.join(filter(lambda char: char not in "!'()*", str(v)))
        for k, v
        in params.items()
    }
    query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params


def getWbiKeys() -> tuple[str, str]:
    """获取最新的 img_key 和 sub_key"""
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav')
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key


def enc_params(params: dict) -> dict:
    """为请求参数进行 wbi 签名"""
    img_key, sub_key = getWbiKeys()
    return encWbi(params, img_key, sub_key)


class ParameterError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RunningError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ConnectError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
