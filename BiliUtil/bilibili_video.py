# coding=utf-8
import re
import json
import copy
from urllib import parse
from BiliUtil.static_component import Util
from BiliUtil.static_component import Quality
from BiliUtil.static_component import ParameterError
from BiliUtil.static_component import RunningError


class Video:
    def __init__(self, aid, cid, name, page):
        self.aid = aid
        self.cid = cid
        self.name = name
        self.page = page
        self.quality = None
        self.length = None
        self.format = None
        self.height = None
        self.width = None
        self.level = None
        self.video = None
        self.audio = None

    def sync(self, cookie=None, quality=None):
        # 检验必要的参数
        if self.aid is None or self.cid is None:
            raise ParameterError('缺少获取视频信息的必要参数')

        if quality is None:
            quality = Quality.V1080P60

        # 发送网络请求
        http_request = {
            'info_obj': Util.VIDEO,
            'params': {
                'avid': str(self.aid),
                'cid': str(self.cid),
                'qn': quality[0],
                'otype': 'json',
                'fnver': 0,
                'fnval': 16
            },
            'cookie': cookie
        }
        json_data = Util.http_get(**http_request)

        # 自动识别不同的数据
        self.format = json_data['data']['format']
        self.length = json_data['data']['timelength']
        self.quality = Quality.INDEX[json_data['data']['quality']]
        if 'dash' in json_data['data']:
            self.level = 'new_version'
            video_obj = json_data['data']['dash']['video'][-1]
            audio_obj = json_data['data']['dash']['audio'][0]
            self.height = ['height']
            self.width = video_obj['width']
            self.video = list([video_obj['baseUrl']])
            self.audio = list([audio_obj['baseUrl']])
            if video_obj['backup_url']:
                for backup in video_obj['backup_url']:
                    self.video.append(backup)
            if audio_obj['backup_url']:
                for backup in audio_obj['backup_url']:
                    self.video.append(backup)

        elif 'durl' in json_data['data']:
            self.level = 'old_version'
            video_obj = json_data['data']['durl'][-1]
            self.video = list([video_obj['url']])
            if video_obj['backup_url']:
                for backup in video_obj['backup_url']:
                    self.video.append(backup)

        # 返回视频信息
        return copy.deepcopy(vars(self))
