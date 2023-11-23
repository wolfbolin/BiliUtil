# coding=utf-8
import copy
from .. import Util


class Video:
    def __init__(self, album, cid, name, page):
        self.album = album
        self.cid = str(cid)
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

    def video_name(self, name_pattern=Util.Config.SET_AS_CODE):
        """
        辅助生成视频文件的名称
        :param name_pattern: 命名模式
        :return: 经过拼接的视频文件名称
        """
        if name_pattern == Util.Config.SET_AS_CODE:
            name = self.cid
        elif name_pattern == Util.Config.SET_AS_NAME:
            name = self.album.name
        elif name_pattern == Util.Config.SET_AS_PAGE:
            name = self.name
        else:
            name = "unknown"

        name = Util.legalize_name(name)
        return "{}_P{}_{}".format(name, self.page, self.quality[1])

    async def sync(self, quality=None):
        # 检验必要的参数
        if self.album.aid is None or self.cid is None:
            raise Util.ParameterError('缺少获取视频信息的必要参数')

        if quality is None:
            quality = Util.Config.Quality.V4K

        # 发送网络请求
        http_request = {
            'info_obj': Util.VIDEO,
            'params': {
                'avid': str(self.album.aid),
                'cid': str(self.cid),
                'qn': quality[0],
                'otype': 'json',
                'fourk': 1,
                'fnver': 0,
                'fnval': 16
            },
            'cookie': Util.get_cookie()
        }
        json_data = await Util.http_get(**http_request)

        # 自动识别不同的数据
        self.format = json_data['data']['format']
        self.length = json_data['data']['timelength']
        self.quality = Util.Config.Quality.INDEX[json_data['data']['quality']]
        if 'dash' in json_data['data']:
            self.level = 'new_version'
            video_obj = json_data['data']['dash']['video'][0]
            audio_obj = json_data['data']['dash']['audio'][0]
            self.height = video_obj['height']
            self.width = video_obj['width']
            self.video = list([video_obj['baseUrl']])
            self.audio = list([audio_obj['baseUrl']])
            if video_obj['backup_url']:
                for backup in video_obj['backup_url']:
                    self.video.append(backup)
            if audio_obj['backup_url']:
                for backup in audio_obj['backup_url']:
                    self.audio.append(backup)

        elif 'durl' in json_data['data']:
            self.level = 'old_version'
            video_obj = json_data['data']['durl'][-1]
            self.video = list([video_obj['url']])
            if video_obj['backup_url']:
                for backup in video_obj['backup_url']:
                    self.video.append(backup)

        # 返回视频信息
        return copy.deepcopy(vars(self))
