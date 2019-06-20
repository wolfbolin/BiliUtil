# coding=utf-8
import re
import copy
from urllib import parse
from BiliUtil.bilibili_album import Album
from BiliUtil.static_component import Util
from BiliUtil.bilibili_channel import Channel
from BiliUtil.static_component import ParameterError
from BiliUtil.static_component import RunningError


class User:
    def __init__(self, uid=None):
        self.uid = uid
        self.name = None
        self.birthday = None
        self.title = None
        self.face = None
        self.time = None
        self.level = None
        self.sex = None
        self.sign = None
        self.vip = None

    def set_user(self, uid):
        self.uid = uid

    def set_by_url(self, url):
        input_url = parse.urlparse(url)
        uid = re.match('/([0-9]+)', input_url.path).group(1)
        self.uid = uid

    def sync(self, cookie=None):
        # 检验必要的参数
        if self.uid is None:
            raise ParameterError('缺少获取用户信息的必要参数')

        # 发送网络请求
        http_request = {
            'info_obj': Util.USER,
            'params': {
                'mid': str(self.uid),
                'jsonp': 'jsonp'
            },
            'cookie': cookie
        }
        json_data = Util.http_get(**http_request)

        # 修改对象信息
        self.uid = json_data['data']['mid']
        self.name = json_data['data']['name']
        self.sex = json_data['data']['sex']
        self.face = json_data['data']['face']
        self.sign = json_data['data']['sign']
        self.level = json_data['data']['level']
        self.birthday = json_data['data']['birthday']
        self.title = json_data['data']['official']['title']
        self.vip = bool(json_data['data']['vip']['status'])

        # 返回用户信息
        return copy.deepcopy(vars(self))

    def get_channel_list(self, cookie=None):
        if self.uid is None:
            raise BaseException('缺少获取频道列表的必要参数')

        # 发送网络请求
        http_request = {
            'info_obj': Util.CHANNEL_LIST,
            'params': {
                'mid': str(self.uid),
                'guest': False,
                'jsonp': 'jsonp'
            },
            'cookie': cookie
        }
        json_data = Util.http_get(**http_request)
        channel_list = list(Channel(self.uid, ch['cid']) for ch in json_data['data']['list'])

        # 返回频道列表
        return channel_list

    def get_album_list(self, cookie=None):
        # 检验必要的参数
        if self.uid is None:
            raise ParameterError('缺少获取视频列表的必要参数')

        # 发送网络请求
        http_request = {
            'info_obj': Util.USER_VIDEO,
            'params': {
                'mid': str(self.uid),
                'pagesize': 30,
                'tid': 0,
                'page': 1,
                'order': 'pubdate'
            },
            'cookie': cookie
        }
        album_list = []
        while True:
            json_data = Util.http_get(**http_request)

            # 循环获取列表
            album_list.extend([Album(av['aid']) for av in json_data['data']['vlist']])
            if len(album_list) < int(json_data['data']['count']):
                http_request['params']['page'] += 1
            else:
                break

        # 返回视频列表
        return album_list
