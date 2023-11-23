# coding=utf-8
from __future__ import annotations
import re
from urllib import parse

from .. import Util, Video


class Channel:
    def __init__(self, uid=None, cid=None):
        self.uid = str(uid)
        self.cid = str(cid)
        self.name = None
        self.cover = None
        self.count = None

    def set_channel(self, uid, cid):
        self.uid = str(uid)
        self.cid = str(cid)

    def set_by_url(self, url):
        input_url = parse.urlparse(url)
        uid = re.match('/([0-9]+)/channel/detail', input_url.path).group(1)
        cid = parse.parse_qs(input_url.query)['cid'][0]
        self.uid = str(uid)
        self.cid = str(cid)

    async def get_album_list(self, cookie=None):
        # 检验必要的参数
        if self.uid is None or self.cid is None:
            raise Util.ParameterError('缺少获取频道列表的必要参数')
        # 发送网络请求
        http_request = {
            'info_obj': Util.CHANNEL,
            'params': {
                'mid': str(self.uid),
                'cid': str(self.cid),
                'pn': 1,  # 当前页码下标
                'ps': 30,  # 每页视频数量
                'order': 0  # 默认排序
            },
            'cookie': cookie
        }
        album_list = []
        while True:
            json_data = await Util.http_get(**http_request)

            # 修改对象信息
            self.name = json_data['data']['list']['name']
            self.cover = json_data['data']['list']['cover']
            self.count = str(json_data['data']['list']['count'])

            # 循环获取列表
            album_list.extend([Video.Album(av['aid']) for av in json_data['data']['list']['archives']])
            if len(album_list) < int(json_data['data']['page']['count']):
                http_request['params']['pn'] += 1
            else:
                break

        return album_list
