import json
import requests

import BiliUtil_old.static_value as v
import BiliUtil_old.static_func as f


class Album:
    def __init__(self, aid):
        print('(=・ω・=)创建集合对象(=・ω・=)')
        self.set_aid(aid)

    aid = None
    album_info = dict()

    def set_aid(self, aid):
        self.aid = aid
        param = {
            'aid': str(aid)
        }
        http_result = requests.get(v.URL_UP_ALBUM, params=param,
                                   headers=f.new_http_header(v.URL_UP_INFO))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        self.album_info = {
            'mid': {
                'k': '用户ID',
                'v': json_data['data']['owner']['mid']
            },
            'name': {
                'k': '用户昵称',
                'v': json_data['data']['owner']['name']
            },
            'aid': {
                'k': '视频av号',
                'v': json_data['data']['aid']
            },
            'time': {
                'k': '发布时间',
                'v': json_data['data']['ctime']
            },
            'desc': {
                'k': '视频简介',
                'v': json_data['data']['desc']
            },
            'title': {
                'k': '视频标题',
                'v': json_data['data']['title']
            },
            'zone': {
                'k': '视频分区',
                'v': json_data['data']['tname']
            },
            'num': {
                'k': '视频数量',
                'v': json_data['data']['videos']
            },
            'pic': {
                'k': '视频封面',
                'v': json_data['data']['pic']
            },
            'like': {
                'k': '点赞数',
                'v': json_data['data']['stat']['like']
            },
            'coin': {
                'k': '投币数',
                'v': json_data['data']['stat']['coin']
            },
            'favorite': {
                'k': '收藏数',
                'v': json_data['data']['stat']['favorite']
            },
            'share': {
                'k': '分享数',
                'v': json_data['data']['stat']['share']
            },
            'view': {
                'k': '播放数',
                'v': json_data['data']['stat']['coin']
            },
            'danmu': {
                'k': '弹幕数',
                'v': json_data['data']['stat']['danmaku']
            },
            'page': {
                'k': '分P列表',
                'v': []
            }
        }

        for page in json_data['data']['pages']:
            video_page = dict()
            video_page['cid'] = {
                'k': '视频编号',
                'v': page['cid']
            }
            video_page['index'] = {
                'k': '分P下标',
                'v': page['page']
            }
            video_page['name'] = {
                'k': '分P名称',
                'v': page['part']
            }
            self.album_info['page']['v'].append(video_page)

        return True

    def get_album_info(self):
        return self.album_info

    def get_info_key(self, key):
        return self.album_info[key]['k']

    def get_info_val(self, key):
        return self.album_info[key]['v']
