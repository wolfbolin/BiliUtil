import os
import re
import json
import requests
from urllib import parse

import BiliUtil.static_value as v
import BiliUtil.static_func as f
from BiliUtil.bili_video import Video


class Album:
    cookie = None

    aid = None

    name = None
    time = None
    desc = None
    zone = None
    num = None
    cover = None
    like = None
    coin = None
    favorite = None
    share = None
    view = None
    danmu = None
    video_list = []

    def __init__(self, aid=None):
        print('(=・ω・=)创建集合对象(=・ω・=)')
        self.aid = aid

    def set_album(self, aid=None):
        self.aid = aid
        self.name = None
        self.time = None
        self.desc = None
        self.zone = None
        self.num = None
        self.cover = None
        self.like = None
        self.coin = None
        self.favorite = None
        self.share = None
        self.view = None
        self.danmu = None
        self.video_list = []

    def set_by_url(self, url):
        input_url = parse.urlparse(url)
        aid = re.match('/video/av([0-9]+)', input_url.path).group(1)
        self.set_album(aid)

    def set_cookie(self, cookie):
        self.cookie = cookie
        for video in self.video_list:
            video.set_cookie(cookie)

    def get_album_info(self):
        if self.aid is None:
            raise BaseException('缺少必要的参数')

        f.print_1('正在获取视频信息...', end='')
        param = {
            'aid': str(self.aid)
        }
        http_result = requests.get(v.URL_UP_ALBUM, params=param,
                                   headers=f.new_http_header(v.URL_UP_ALBUM))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        # 修改对象信息
        self.aid = json_data['data']['aid']
        self.time = json_data['data']['ctime']
        self.desc = json_data['data']['desc']
        self.name = json_data['data']['title']
        self.zone = json_data['data']['tname']
        self.num = json_data['data']['videos']
        self.cover = json_data['data']['pic']
        self.like = json_data['data']['stat']['like']
        self.coin = json_data['data']['stat']['coin']
        self.favorite = json_data['data']['stat']['favorite']
        self.share = json_data['data']['stat']['share']
        self.view = json_data['data']['stat']['view']
        self.danmu = json_data['data']['stat']['danmaku']
        self.video_list = list()

        for page in json_data['data']['pages']:
            cv = Video(self.aid, page['cid'], page['page'], page['part'])
            cv.set_cookie(self.cookie)
            self.video_list.append(cv)

        return self

    def get_album_data(self, base_path='', name_path=False):
        if len(self.video_list) == 0:
            self.get_album_info()

        if name_path:
            temp_name = self.name.replace('/', '-')  # 避免特殊字符
            cache_path = base_path + './{}'.format(temp_name)
        else:
            cache_path = base_path + './{}'.format(self.aid)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        f.print_1('正在获取视频封面--', end='')
        f.print_b('av:{}'.format(self.aid))
        http_result = requests.get(self.cover)
        with open(cache_path + '/cover.jpg', 'wb') as file:
            file.write(http_result.content)
        f.print_g('[OK]', end='')
        f.print_1('视频封面已保存')

        for video in self.video_list:
            video.get_video_data(cache_path, name_path)

        with open(cache_path + '/info.json', 'w', encoding='utf8') as file:
            file.write(str(json.dumps(self.get_json_info())))

    def get_json_info(self):
        json_data = vars(self).copy()
        video_list = []
        if 'video_list' in json_data:
            for video in json_data['video_list']:
                video_list.append(video.get_json_info())
            json_data['video_list'] = video_list
        return json_data
