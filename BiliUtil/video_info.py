import json
import requests

import BiliUtil_old.static_value as v
import BiliUtil_old.static_func as f


class Video:
    def __init__(self, aid, cid, cookie):
        print('(=・ω・=)创建视频对象(=・ω・=)')
        self.set_cookie(cookie)
        self.set_cid(aid, cid)

    aid = None
    cid = None
    cookie = dict()
    video_info = dict()

    def set_cookie(self, cookie):
        if isinstance(cookie, dict):
            self.cookie = {
                'SESSDATA': cookie['SESSDATA']
            }
        elif isinstance(cookie, str):
            for line in cookie.split(';'):
                name, value = line.strip().split('=', 1)
                if name == 'SESSDATA':
                    self.cookie = {
                        'SESSDATA': value
                    }
                    break
        else:
            self.cookie = dict()

    def set_cid(self, aid, cid):
        self.cid = cid
        param = {
            'avid': str(aid),
            'cid': str(cid),
            'qn': 116,  # 尝试1080P 60fps
            'otype': 'json',
            'fnver': 0,
            'fnval': 16
        }
        http_result = requests.get(v.URL_UP_VIDEO, params=param,
                                   headers=f.new_http_header(v.URL_UP_INFO))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        self.video_info = {
            'aid': {
                'k': '视频av号',
                'v': aid
            },
            'cid': {
                'k': '视频编号',
                'v': cid
            },
            'quality': {
                'k': '视频画质',
                'v': json_data['data']['quality']
            },
            'length': {
                'k': '视频长度',
                'v': json_data['data']['timelength']
            },
            'video': {
                'k': '视频地址',
                'v': json_data['data']['dash']['video'][-1]['baseUrl']
            },
            'audio': {
                'k': '音频地址',
                'v': json_data['data']['dash']['audio'][0]['baseUrl']
            }
        }

        return True

    def get_video_info(self):
        return self.video_info

    def get_info_key(self, key):
        return self.video_info[key]['k']

    def get_info_val(self, key):
        return self.video_info[key]['v']
