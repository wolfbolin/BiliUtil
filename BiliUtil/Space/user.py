# coding=utf-8
from __future__ import annotations
import re
import copy
from urllib import parse
from typing import Optional, List, Union, Dict, Any
from .. import Util, Video
from .channel import Channel


class User:
    def __init__(self, uid: Optional[Union[int, str]] = None) -> None:
        self.uid: Optional[str] = str(uid) if uid is not None else None
        self.name: Optional[str] = None
        self.birthday: Optional[str] = None
        self.title: Optional[str] = None
        self.face: Optional[str] = None
        self.time: Optional[str] = None  # The datatype might need verification
        self.level: Optional[str] = None  # The datatype might need verification
        self.sex: Optional[str] = None
        self.sign: Optional[str] = None
        self.vip: Optional[bool] = None

    def set_user(self, uid: Union[int, str]) -> None:
        self.uid = str(uid)

    def set_by_url(self, url: str) -> None:
        input_url = parse.urlparse(url)
        uid = re.match('/([0-9]+)', input_url.path).group(1)
        self.uid = str(uid)

    async def sync(self) -> Dict[str, Any]:
        # 检验必要的参数
        if self.uid is None:
            raise Util.ParameterError('缺少获取用户信息的必要参数')
        # 发送网络请求
        http_request = {
            'info_obj': Util.USER,
            'params': {
                'mid': str(self.uid),
                'platform': 'web'
            },
            'cookie': Util.get_cookie()
        }
        json_data = await Util.http_get(**http_request)

        # 修改对象信息
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

    def get_channel_list(self, cookie: Optional[str] = None) -> List[Channel]:
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

    async def get_album_list(self, count: int = Util.FetchConfig.ALL) -> List[
        Video.Album]:
        # 检验必要的参数
        if self.uid is None:
            raise Util.ParameterError('缺少获取视频列表的必要参数')
        # 发送网络请求
        http_request = {
            'info_obj': Util.USER_VIDEO,
            'params': {
                'mid': str(self.uid),
                'pagesize': 30,
                'tid': 0,
                'pn': 1,
                'order': 'pubdate'
            },
            'cookie': Util.get_cookie()
        }
        album_list = []
        while True:
            json_data = await Util.http_get(**http_request)

            new_album_list = [Video.Album(av['aid']) for av in json_data['data']['list']['vlist']]
            if count != Util.FetchConfig.ALL and len(album_list) + len(new_album_list) >= count:
                album_list.extend(new_album_list[:count - len(album_list)])
                break

            # 循环获取列表
            album_list.extend([Video.Album(av['aid']) for av in json_data['data']['list']['vlist']])

            if len(album_list) < int(json_data['data']['page']['count']):
                http_request['params']['pn'] += 1
            else:
                break

        # 返回视频列表
        return album_list

    async def get_album_list_by_search(self, keyword: str = '', count: int = Util.FetchConfig.ALL) -> List[
        Video.Album]:
        # 检验必要的参数
        if self.uid is None:
            raise Util.ParameterError('缺少获取视频列表的必要参数')
        # 发送网络请求
        http_request = {
            'info_obj': Util.USER_VIDEO,
            'params': {
                'keyword': keyword,
                'mid': str(self.uid),
                'pagesize': 30,
                'tid': 0,
                'pn': 1,
                'order': 'pubdate'
            },
            'cookie': Util.get_cookie()
        }
        album_list = []
        while True:
            json_data = await Util.http_get(**http_request)

            new_album_list = [Video.Album(av['aid']) for av in json_data['data']['list']['vlist']]
            if count != Util.FetchConfig.ALL and len(album_list) + len(new_album_list) >= count:
                album_list.extend(new_album_list[:count - len(album_list)])
                break

            # 循环获取列表
            album_list.extend([Video.Album(av['aid']) for av in json_data['data']['list']['vlist']])

            if len(album_list) < int(json_data['data']['page']['count']):
                http_request['params']['pn'] += 1
            else:
                break

        # 返回视频列表
        return album_list
