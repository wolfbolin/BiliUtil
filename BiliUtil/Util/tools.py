# coding=utf-8
import os
import re
import time
import json
import requests
import subprocess
from urllib import parse
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter


# from BiliUtil import http_proxy, https_proxy


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
        INDEX = {
            16: V360P,
            32: V480P,
            64: V720P,
            74: V720P60,
            80: V1080P,
            112: V1080Px,
            116: V1080P60
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
    'url': 'http://api.bilibili.com/x/space/acc/info',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com'
}
USER_VIDEO = {
    'url': 'http://space.bilibili.com/ajax/member/getSubmitVideos',
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
    useragent_path = os.path.dirname(__file__) + '/fake_useragent.json'
    header['Host'] = parse.urlparse(info_obj['url']).netloc
    header['User-Agent'] = UserAgent(path=useragent_path).random
    header['Origin'] = info_obj['origin']
    header['Referer'] = info_obj['referer']
    return header


def http_get(info_obj, params, cookie=None):
    # 获取代理配置
    proxies = {
        'http': Config.HTTP_PROXY,
        'https': Config.HTTPS_PROXY
    }

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
    client = requests.session()
    client.mount("http://", HTTPAdapter(max_retries=5))
    client.mount("https://", HTTPAdapter(max_retries=5))

    try:
        http_result = client.get(url=info_obj['url'], params=params, cookies=cookie,
                                 headers=new_http_header, timeout=5, proxies=proxies)
    except requests.exceptions:
        raise ConnectError('多次网络请求均未能获得数据：{}'.format(info_obj['url']))

    # 尝试理解并验证响应数据
    if http_result.status_code == 200:
        try:
            json_data = json.loads(http_result.text)
        except json.decoder.JSONDecodeError:
            raise RunningError('请求响应无法解析：{}'.format(http_result.text))

        if 'code' in json_data and json_data['code'] == 0:
            return json_data
        elif 'status' in json_data and json_data['status'] is True:
            return json_data
        elif json_data['code'] == -404 or json_data['code'] == -403:
            raise RunningError('请求对象异常或被锁定，无法获取')
    else:
        raise ConnectError('网络响应状态异常，HTTP响应码：{}'.format(http_result.status_code))


def legalize_name(name):
    legal_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s']", '_', name)
    legal_name = re.sub(r'[‘’]', '_', legal_name)
    if len(legal_name) == 0:
        return 'null'
    return legal_name


def aria2c_pull(aid, path, name, url_list, show_process=False):
    # 设置输出信息
    if show_process:
        out_pipe = None
    else:
        out_pipe = subprocess.PIPE
    # 读取代理信息
    proxies = ''
    proxies += ' --http-proxy="{}"'.format(Config.HTTP_PROXY) if Config.HTTP_PROXY is not None else ""
    proxies += ' --https-proxy="{}"'.format(Config.HTTPS_PROXY) if Config.HTTPS_PROXY is not None else ""

    referer = 'https://www.bilibili.com/video/av' + str(aid)
    url = '"{}"'.format('" "'.join(url_list))
    shell = 'aria2c -c -k 1M -x {} -d "{}" -o "{}" --referer="{}" {} {}'
    shell = shell.format(len(url_list), path, name, referer, proxies, url)
    process = subprocess.Popen(shell, stdout=out_pipe, stderr=out_pipe, shell=True)
    process.wait()


def ffmpeg_merge(path, name, show_process=False):
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
