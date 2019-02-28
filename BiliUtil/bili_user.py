import os
import re
import json
import requests
from urllib import parse

import BiliUtil.static_value as v
import BiliUtil.static_func as f
from BiliUtil.bili_album import Album
from BiliUtil.bili_channel import Channel


class User:
    cookie = None

    uid = None

    name = None
    birthday = None
    coin = None
    face = None
    time = None
    level = None
    sex = None
    sign = None

    album_list = list()
    channel_list = list()

    def __init__(self, uid=None):
        self.uid = uid

    def set_user(self, uid):
        self.uid = uid
        self.name = None
        self.birthday = None
        self.coin = None
        self.face = None
        self.time = None
        self.level = None
        self.sex = None
        self.sign = None
        self.album_list = list()
        self.channel_list = list()

    def set_by_url(self, url):
        input_url = parse.urlparse(url)
        uid = re.match('/([0-9]+)', input_url.path).group(1)
        self.set_user(uid)

    def set_cookie(self, cookie):
        self.cookie = cookie
        for channel in self.channel_list:
            channel.set_cookie(cookie)
        for video in self.album_list:
            video.set_cookie(cookie)

    def get_user_info(self):
        if self.uid is None:
            raise BaseException('缺少必要的参数')

        f.print_1('正在获取用户信息...', end='')
        param = {
            'mid': str(self.uid),
            'jsonp': 'jsonp'
        }
        http_result = requests.get(url=v.URL_UP_INFO, params=param,
                                   headers=f.new_http_header(v.URL_UP_INFO))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        # 修改对象信息
        self.uid = json_data['data']['mid']
        self.name = json_data['data']['name']
        self.birthday = json_data['data']['birthday']
        self.coin = json_data['data']['coins']
        self.face = json_data['data']['face']
        self.time = json_data['data']['jointime']
        self.level = json_data['data']['level']
        self.sex = json_data['data']['sex']
        self.sign = json_data['data']['sign']

        return self

    def get_channel_video_info(self):
        # 获取UP所有频道的所有视频
        if self.uid is None:
            raise BaseException('缺少必要的参数')

        if self.name is None:
            self.get_user_info()

        f.print_1('正在获取频道列表...', end='')
        param = {
            'mid': str(self.uid),
            'guest': False,
            'jsonp': 'jsonp'
        }
        http_result = requests.get(v.URL_UP_CHANNELS, params=param,
                                   headers=f.new_http_header(v.URL_UP_CHANNELS))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        for channel in json_data['data']['list']:
            ch = Channel(self.uid, channel['cid'])
            ch.set_cookie(self.cookie)
            self.channel_list.append(ch)

    def get_channel_video_data(self, base_path='', name_path=False, max_length=None):
        # 获取UP主的所有视频的数据
        if len(self.channel_list) == 0:
            self.get_channel_video_info()

        base_path = os.path.abspath(base_path)  # 获取绝对路径地址
        if name_path:
            # 检查路径名中的特殊字符
            temp_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s'‘’]", '_', self.name)
            if len(temp_name) == 0:
                temp_name = self.uid
            cache_path = base_path + '/{}'.format(temp_name)
        else:
            cache_path = base_path + '/{}'.format(self.uid)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        f.print_1('正在获取用户头像--', end='')
        f.print_b('user:{}'.format(self.name))
        http_result = requests.get(self.face)
        with open(cache_path + '/face.jpg', 'wb') as file:
            file.write(http_result.content)
        f.print_g('[OK]', end='')
        f.print_1('用户头像已保存')

        for channel in self.channel_list:
            channel.get_channel_data(cache_path, name_path, max_length)

        with open(cache_path + '/info.json', 'w', encoding='utf8') as file:
            file.write(str(json.dumps(self.get_dict_info())))

    def get_all_video_info(self):
        # 获取UP主的所有视频的列表信息
        if self.uid is None:
            raise BaseException('缺少必要的参数')

        if self.name is None:
            self.get_user_info()

        f.print_1('正在获取视频列表...', end='')
        param = {
            'mid': str(self.uid),
            'pagesize': 30,
            'tid': 0,
            'page': 1,
            'order': 'pubdate'
        }
        while True:
            http_result = requests.get(v.URL_UP_ALL_VIDEO, params=param,
                                       headers=f.new_http_header(v.URL_UP_ALL_VIDEO))
            if http_result.status_code == 200:
                f.print_g('OK {}'.format(http_result.status_code))
            else:
                f.print_r('RE {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['status'] is not True:
                raise BaseException('获取数据的过程发生错误')

            for video in json_data['data']['vlist']:
                av = Album(video['aid'])
                av.set_cookie(self.cookie)
                self.album_list.append(av)

            # 循环翻页获取并自动退出循环
            if len(self.album_list) >= int(json_data['data']['pages']):
                break
            else:
                param['pn'] += 1

    def get_all_video_data(self, base_path='', name_path=False, max_length=None):
        # 获取UP主的所有视频的数据
        if len(self.album_list) == 0:
            self.get_all_video_info()

        if name_path:
            # 检查路径名中的特殊字符
            temp_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s'‘’]", '_', self.name)
            if len(temp_name) == 0:
                temp_name = self.uid
            cache_path = base_path + './{}'.format(temp_name)
        else:
            cache_path = base_path + './{}'.format(self.uid)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        f.print_1('正在获取用户头像--', end='')
        f.print_b('user:{}'.format(self.name))
        http_result = requests.get(self.face)
        with open(cache_path + '/face.jpg', 'wb') as file:
            file.write(http_result.content)
        f.print_g('[OK]', end='')
        f.print_1('用户头像已保存')

        for album in self.album_list:
            album.get_album_data(cache_path, name_path, max_length)

        with open(cache_path + '/info.json', 'w', encoding='utf8') as file:
            file.write(str(json.dumps(self.get_dict_info())))

    def get_dict_info(self):
        json_data = vars(self).copy()

        album_list = []
        for album in json_data['album_list']:
            album_list.append(album.get_dict_info())
        json_data['album_list'] = album_list

        channel_list = []
        for channel in json_data['channel_list']:
            channel_list.append(channel.get_dict_info())
        json_data['channel_list'] = channel_list

        return json_data
