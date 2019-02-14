import os
import json
import requests
import subprocess

import BiliUtil.static_value as v
import BiliUtil.static_func as f


class Video:
    cookie = None

    aid = None
    cid = None
    index = None  # Page index 分P下标
    name = None  # Page name 分P名称

    quality = None
    length = None
    video = None
    audio = None

    def __init__(self, aid=None, cid=None, index=None, name=None):
        print('(=・ω・=)创建视频对象(=・ω・=)')
        self.aid = aid
        self.cid = cid
        self.index = index
        self.name = name

    def set_video(self, aid=None, cid=None, index=None, name=None):
        self.aid = aid
        self.cid = cid
        self.index = index
        self.name = name
        self.quality = None
        self.length = None
        self.video = None
        self.audio = None

    def set_cookie(self, cookie):
        if isinstance(cookie, dict):
            self.cookie = {
                'SESSDATA': cookie['SESSDATA']
            }
        elif isinstance(cookie, str):
            for line in cookie.split(';'):
                name, value = line.strip().split('=', 1)
                if name == 'SESSDATA':
                    self.cookie = {
                        'SESSDATA': value
                    }
                    break
        else:
            self.cookie = dict()

    def get_video_info(self, qn=116):
        if self.aid is None or self.cid is None:
            raise BaseException('缺少必要的参数')

        f.print_1('正在获取分P信息...', end='')
        param = {
            'avid': str(self.aid),
            'cid': str(self.cid),
            'qn': qn,  # 默认尝试1080P 60fps
            'otype': 'json',
            'fnver': 0,
            'fnval': 16
        }
        http_result = requests.get(v.URL_UP_VIDEO, params=param,
                                   headers=f.new_http_header(v.URL_UP_INFO))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        self.quality = json_data['data']['quality']
        self.length = json_data['data']['timelength']
        self.video = json_data['data']['dash']['video'][-1]['baseUrl']
        self.audio = json_data['data']['dash']['audio'][0]['baseUrl']

        return self

    def get_video(self, base_path='', name_path=False):
        if self.video is None and self.audio is None:
            self.get_video_info()

        if name_path:
            cache_path = base_path + './{}'.format(self.name)
        else:
            cache_path = base_path + './{}'.format(self.cid)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # 使用两个进程分别下载视频和音频
        f.print_1('正在下载视频和配套音--', end='')
        f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
        f.print_cyan('==============================================================')
        referer = 'https://www.bilibili.com/video/av' + str(self.aid)
        audio_shell = "powershell aria2c -c -s 2 -o'{}/{}.aac' --referer={} '{}'"
        audio_process = subprocess.Popen(
            audio_shell.format(cache_path, self.cid, referer, self.audio))

        video_shell = "powershell aria2c -c -s 2 -o'{}/{}.flv' --referer={} '{}'"
        video_process = subprocess.Popen(
            video_shell.format(cache_path, self.cid, referer, self.video))

        audio_process.wait()
        video_process.wait()

        f.print_cyan('==============================================================')

        audio_cache_path = '{}/{}.aac'.format(cache_path, self.cid)
        video_cache_path = '{}/{}.flv'.format(cache_path, self.cid)
        if os.path.exists(audio_cache_path) and os.path.exists(video_cache_path):
            f.print_g('[OK]', end='')
            f.print_1('视频与配套音频下载成功--', end='')
            f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
        else:
            f.print_r('[ERR]', end='')
            f.print_1('视频或配套音频下载失败--', end='')
            f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
            raise BaseException('av:{},cv:{},下载失败'.format(self.aid, self.cid))

        with open(cache_path + '/info.json', 'w', encoding='utf8') as file:
            file.write(str(json.dumps(self.get_json_info())))

    def get_json_info(self):
        json_data = vars(self).copy()
        return json_data
