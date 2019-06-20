# coding=utf-8
import os
import re
import copy
import time
import json
import requests
import subprocess
from fake_useragent import UserAgent


class Quality:
    V360P = ('16', '流畅 360P')
    V480P = ('32', '清晰 480P')
    V720P = ('64', '高清 720P')
    V7200P60 = ('74', '高清 720P60')
    V1080P = ('80', '高清 1080P')
    V1080Px = ('112', '高清 1080P+')
    V1080P60 = ('116', '高清 1080P60')
    INDEX = {
        16: V360P,
        32: V480P,
        64: V720P,
        74: V7200P60,
        80: V1080P,
        112: V1080Px,
        116: V1080P60
    }


class Downloader:
    SET_AS_NAME = 1
    SET_AS_CODE = 2

    class Filter:
        def __init__(self, quality=None, length=None, height=None, width=None, page=None):
            self.quality = quality
            self.length = length
            self.height = height
            self.width = width
            self.page = page

        def set_quality(self, quality):
            if ~isinstance(quality, list):
                raise ParameterError('参数类型异常')
            self.quality = quality

        def set_length(self, length):
            if ~isinstance(length, tuple):
                raise ParameterError('参数类型异常')
            self.length = length

        def set_height(self, height):
            if ~isinstance(height, tuple):
                raise ParameterError('参数类型异常')
            self.height = height

        def set_width(self, width):
            if ~isinstance(width, tuple):
                raise ParameterError('参数类型异常')
            self.width = width

        def set_page(self, page):
            if ~isinstance(page, list):
                raise ParameterError('参数类型异常')
            self.page = page

        def check_video(self, video):
            if self.quality and video.quality in self.quality:
                print(video.quality)
                return False
            if self.length and self.length[0] <= video.length <= self.length[1]:
                return False
            if video.level == 'new_version':
                if self.height and self.height[0] <= video.height <= self.height[1]:
                    return False
                if self.width and self.width[0] <= video.width <= self.width[1]:
                    return False
            if self.page and video.page in self.page:
                return False
            return True  # 有问题

    class Task:
        def __init__(self, video, output, name_pattern):
            self.video_info = copy.deepcopy(vars(video))
            del self.video_info['video']
            del self.video_info['audio']
            self.aid = video.aid
            self.level = video.level
            self.video = video.video
            self.audio = video.audio
            self.path = os.path.abspath(output)
            if name_pattern == Downloader.SET_AS_NAME:
                self.name = '{}_P{}_{}'.format(Util.legalize_name(video.name), video.page, video.quality[1])
            elif name_pattern == Downloader.SET_AS_CODE:
                self.name = '{}_P{}_{}'.format(video.cid, video.page, video.quality[1])
            else:
                raise ParameterError('参数类型异常')

        def start(self):
            if self.level == 'old_version':
                Util.aria2c(self.aid, self.path, self.name + '.mp4', self.video)
            elif self.level == 'new_version':
                Util.aria2c(self.aid, self.path, self.name + '.acc', self.audio)
                Util.aria2c(self.aid, self.path, self.name + '.flv', self.video)


class AutoLoad:
    @staticmethod
    def user_all_video(user, output, name_pattern, v_filter=None, cookie=None):
        absolute_path = os.path.abspath(output)
        user_structure = {
            'type': 'user',
            'path': absolute_path,
            'name': user.uid,
            'sublayer': []
        }
        if name_pattern == Downloader.SET_AS_NAME:
            user.sync()
            user_structure['name'] = Util.legalize_name(user.name)

        album_list = user.get_album_list()
        album_path = '{}/{}'.format(user_structure['path'], user_structure['name'])
        album_path = os.path.abspath(album_path)
        for album in album_list:
            album_structure = {
                'type': 'album',
                'path': album_path,
                'name': album.aid,
                'sublayer': []
            }
            if name_pattern == Downloader.SET_AS_NAME:
                album.sync()
                album_structure['name'] = Util.legalize_name(album.name)

            video_list = album.get_video_list()
            video_path = '{}/{}'.format(album_structure['path'], album_structure['name'])
            video_path = os.path.abspath(video_path)
            for video in video_list:
                video.sync(cookie)
                if v_filter and v_filter.check_video(video):
                    continue
                task = Downloader.Task(video, video_path, name_pattern)
                album_structure['task_list'].append(task)

            if len(album_structure['task_list']) > 0:
                user_structure['sublayer'].append(album_structure)

        return user_structure

    @staticmethod
    def channel_all_video(channel, v_filter, cookie, output, name_pattern):
        absolute_path = os.path.abspath(output)
        channel_structure = {
            'type': 'channel',
            'path': absolute_path,
            'name': channel.cid,
            'sublayer': []
        }
        if name_pattern == Downloader.SET_AS_NAME:
            channel.sync()
            channel_structure['name'] = Util.legalize_name(channel.name)

        album_list = channel.get_album_list()
        album_path = '{}/{}'.format(channel_structure['path'], channel_structure['name'])
        album_path = os.path.abspath(album_path)
        for album in album_list:
            album_structure = {
                'type': 'album',
                'path': album_path,
                'name': album.aid,
                'task_list': []
            }
            if name_pattern == Downloader.SET_AS_NAME:
                album.sync()
                album_structure['name'] = Util.legalize_name(album.name)

            video_list = album.get_video_list()
            video_path = '{}/{}'.format(album_structure['path'], album_structure['name'])
            video_path = os.path.abspath(video_path)
            for video in video_list:
                video.sync(cookie)
                if v_filter and v_filter.check_video(video):
                    continue
                task = Downloader.Task(video, video_path, name_pattern)
                # album_structure['task_list'].append(task)
                album_structure['task_list'].append(copy.deepcopy(vars(task)))

            if len(album_structure['task_list']) > 0:
                channel_structure['sublayer'].append(album_structure)

        return channel_structure


class Util:
    HEADER = {
        'Host': 'api.bilibili.com',
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

    @staticmethod
    def new_http_header(info_obj):
        header = Util.HEADER.copy()
        useragent_path = os.path.dirname(__file__) + '/fake_useragent.json'
        header['User-Agent'] = UserAgent(path=useragent_path).random
        header['Origin'] = info_obj['origin']
        header['Referer'] = info_obj['referer']
        return header

    @staticmethod
    def http_get(info_obj, params, cookie=None):
        http_header = Util.new_http_header(info_obj)
        if cookie is not None:
            http_header['Cookie'] = cookie

        for times in range(5):
            try:
                http_result = requests.get(url=info_obj['url'], params=params, headers=http_header, timeout=5)
            except requests.exceptions:
                time.sleep(3)
                continue
            if http_result.status_code == 200:
                try:
                    json_data = json.loads(http_result.text)
                except json.decoder.JSONDecodeError:
                    time.sleep(1)
                    continue
                if 'code' in json_data and json_data['code'] == 0:
                    return json_data
                elif 'status' in json_data and json_data['status'] is True:
                    return json_data
                elif json_data['code'] == -404 or json_data['code'] == -403:
                    raise RunningError('请求对象异常或被锁定，无法获取')

        raise RunningError('多次网络请求均未能获得数据：{}'.format(info_obj['url']))

    @staticmethod
    def legalize_name(name):
        legal_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s']", '_', name)
        legal_name = re.sub(r'[‘’]', '_', legal_name)
        if len(legal_name) == 0:
            return 'null'
        return legal_name

    @staticmethod
    def aria2c(aid, path, name, url_list):
        referer = 'https://www.bilibili.com/video/av' + str(aid)
        url = '"{}"'.format('" "'.join(url_list))
        shell = 'aria2c -c -k 1M -x {} -d "{}" -o "{}" --referer="{}" {}'
        shell = shell.format(len(url_list), path, name, referer, url)
        print(shell)
        process = subprocess.Popen(shell, shell=True)
        process.wait()


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
