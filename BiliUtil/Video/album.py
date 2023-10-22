# coding=utf-8
from __future__ import annotations
import re
import copy
from urllib import parse
from typing import Optional, List, Tuple, Any, Dict
import BiliUtil.Util as Util


class Album:
    def __init__(self, aid: Optional[str] = None):
        self.aid: Optional[str] = Util.to_av(aid)
        self.num: Optional[int] = None
        self.type: Optional[str] = None
        self.cover: Optional[str] = None
        self.name: Optional[str] = None
        self.time: Optional[str] = None
        self.desc: Optional[str] = None
        self.view: Optional[int] = None
        self.danmu: Optional[int] = None
        self.reply: Optional[int] = None
        self.favorite: Optional[int] = None
        self.coin: Optional[int] = None
        self.share: Optional[int] = None
        self.like: Optional[int] = None
        self.video_info: Optional[List[Tuple[int, str]]] = None
        self.is_upower_exclusive: bool = False  # 是否为充电专属

    def set_album(self, aid: str) -> None:
        self.aid = Util.to_av(aid)

    def set_by_url(self, url: str) -> None:
        input_url = parse.urlparse(url)
        bid = re.match('/video/(BV[0-9a-zA-Z]+|av[0-9]+)', input_url.path).group(1)
        self.aid = Util.to_av(bid)

    def album_name(self, name_pattern: int = Util.Config.SET_AS_CODE) -> str:
        """
        辅助生成稿件文件的名称
        :param name_pattern: 命名模式
        :return: 经过拼接的稿件文件名称
        """
        if name_pattern == Util.Config.SET_AS_CODE:
            name = self.aid
        elif name_pattern == Util.Config.SET_AS_NAME:
            name = self.name
        elif name_pattern == Util.Config.SET_AS_PAGE:
            name = self.name
        else:
            name = "unknown"

        return Util.legalize_name(name)

    def sync(self, cookie: Optional[str] = None) -> Dict[str, Any]:
        # 检验必要的参数
        if self.aid is None:
            raise Util.ParameterError('缺少获取视频信息的必要参数')

        # 发送网络请求
        http_request = {
            'info_obj': Util.ALBUM,
            'params': {
                'aid': str(self.aid)
            },
            'cookie': cookie
        }
        json_data = Util.http_get(**http_request)

        # 修改对象信息
        self.num = json_data['data']['videos']
        self.type = json_data['data']['tname']
        self.cover = json_data['data']['pic']
        self.name = json_data['data']['title']
        self.time = json_data['data']['ctime']
        self.desc = json_data['data']['desc']
        self.view = json_data['data']['stat']['view']
        self.danmu = json_data['data']['stat']['danmaku']
        self.reply = json_data['data']['stat']['reply']
        self.favorite = json_data['data']['stat']['favorite']
        self.coin = json_data['data']['stat']['coin']
        self.share = json_data['data']['stat']['share']
        self.like = json_data['data']['stat']['like']
        self.video_info = [(page['cid'], page['part']) for page in json_data['data']['pages']]
        self.is_upower_exclusive = json_data['data']['is_upower_exclusive']
        # 返回稿件信息
        return copy.deepcopy(vars(self))

    def get_video_list(self, cookie: Optional[str] = None) -> List[Video.Video]:
        # 检验必要的参数
        if self.aid is None:
            raise Util.ParameterError('缺少获取视频信息的必要参数')

        if self.video_info is None:
            self.sync(cookie)

        return [Video.Video(self, info[0], info[1], index + 1) for index, info in enumerate(self.video_info)]


import BiliUtil.Video as Video
