import os
import re
import copy
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
    quality_des = None
    length = None
    video = None
    audio = None

    def __init__(self, aid=None, cid=None, index=None, name=None):
        self.set_video(aid, cid, index, name)

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
        elif isinstance(cookie, str) and len(cookie) > 0:
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
            'qn': qn,  # 默认使用最高画质下载
            'otype': 'json',
            'fnver': 0,
            'fnval': 16
        }
        http_result = requests.get(v.URL_UP_VIDEO, params=param, cookies=self.cookie,
                                   headers=f.new_http_header(v.URL_UP_INFO))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        # 自动识别不同的数据来源
        if 'dash' in json_data['data']:
            self.quality = json_data['data']['quality']
            self.length = json_data['data']['timelength']
            self.video = json_data['data']['dash']['video'][-1]['baseUrl']
            self.audio = json_data['data']['dash']['audio'][0]['baseUrl']
        elif 'durl' in json_data['data']:
            self.quality = json_data['data']['quality']
            self.length = json_data['data']['timelength']
            self.video = json_data['data']['durl'][-1]['url']

        for index, val in enumerate(json_data['data']['accept_quality']):
            if val == self.quality:
                self.quality_des = json_data['data']['accept_description'][index]
                break

        return self

    def get_video_data(self, base_path='', name_path=False, max_length=None):
        if self.video is None and self.audio is None:
            self.get_video_info()

        if max_length is not None and max_length < self.length:
            f.print_y('视频：{}，超出限定长度取消下载')
            return

        base_path = os.path.abspath(base_path)  # 获取绝对路径地址
        if name_path:
            # 检查路径名中的特殊字符
            temp_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s'‘’]", '_', self.name)
            temp_name = re.sub(r'[‘’]', '_', temp_name)
            if len(temp_name) == 0:
                temp_name = self.cid
            cache_path = base_path + '/{}'.format(temp_name)
        else:
            cache_path = base_path + '/{}'.format(self.cid)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # 使用两个进程分别下载视频和音频
        f.print_1('正在下载视频和配套音--', end='')
        f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
        if self.audio is not None and self.video is not None:
            self.aria2c_download(cache_path, '{}_{}.aac'.format(self.cid, self.quality_des), self.audio)
            self.aria2c_download(cache_path, '{}_{}.flv'.format(self.cid, self.quality_des), self.video)
        if self.video is not None and self.audio is None:
            self.aria2c_download(cache_path, '{}_{}.mp4'.format(self.cid, self.quality_des), self.video)
        else:
            f.print_y('无需独立下载音频')
        f.print_cyan('==============================================================')

        with open(cache_path + '/info.json', 'w', encoding='utf8') as file:
            file.write(str(json.dumps(self.get_dict_info())))

    def aria2c_download(self, cache_path, file_name, download_url):
        referer = 'https://www.bilibili.com/video/av' + str(self.aid)
        shell = 'aria2c -c -s 16 -d "{}" -o "{}" --referer="{}" "{}"'
        shell = shell.format(cache_path, file_name, referer, download_url)
        process = subprocess.Popen(shell, shell=True)
        process.wait()

        file_path = '{}/{}'.format(cache_path, file_name)
        if os.path.exists(file_path):
            f.print_g('[OK]', end='')
            f.print_1('文件{}下载成功--'.format(file_name), end='')
            f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
        else:
            f.print_r('[ERR]', end='')
            f.print_1('文件{}下载失败--'.format(file_name), end='')
            f.print_b('av:{},cv:{}'.format(self.aid, self.cid))
            f.print_r(shell.format(file_path, referer, download_url))
            raise BaseException('av:{},cv:{},下载失败'.format(self.aid, self.cid))

    def get_dict_info(self):
        json_data = copy.deepcopy(vars(self))
        return json_data
