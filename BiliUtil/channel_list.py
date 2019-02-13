import json
import requests

import BiliUtil_old.static_value as v
import BiliUtil_old.static_func as f


class Channel:
    def __init__(self, uid, cid):
        print('(=・ω・=)创建频道对象(=・ω・=)')
        self.set_channel(uid, cid)

    uid = None
    cid = None
    video_list = list()
    channel_info = dict()

    def set_channel(self, uid, cid):
        self.uid = uid
        self.cid = cid
        param = {
            'mid': str(uid),
            'cid': str(cid),
            'pn': 1,  # 当前页码下标
            'ps': 30,  # 每页视频数量
            'order': 0  # 默认排序
        }
        while True:
            http_result = requests.get(v.URL_UP_CHANNEL, params=param,
                                       headers=f.new_http_header(v.URL_UP_CHANNEL))
            if http_result.status_code == 200:
                f.print_g('OK {}'.format(http_result.status_code))
            else:
                f.print_r('RE {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['code'] != 0:
                raise BaseException('获取数据的过程发生错误')

            self.channel_info = {
                'cid': {
                    'k': '用户编号',
                    'v': str(json_data['data']['list']['cid'])
                },
                'mid': {
                    'k': '频道编号',
                    'v': str(json_data['data']['list']['mid'])
                },
                'name': {
                    'k': '频道名称',
                    'v': json_data['data']['list']['name']
                },
                'cover': {
                    'k': '频道封面',
                    'v': json_data['data']['list']['cover']
                },
                'count': {
                    'k': '视频数量',
                    'v': str(json_data['data']['list']['count'])
                }
            }
            for video in json_data['data']['list']['archives']:
                self.video_list.append({
                    'title': video['title'],
                    'aid': video['aid']
                })

            # 循环翻页获取并自动退出循环
            if len(self.video_list) >= int(json_data['data']['page']['count']):
                break
            else:
                param['pn'] += 1

    def get_video_list(self):
        return self.video_list

    def get_info_key(self, key):
        return self.channel_info[key]['k']

    def get_info_val(self, key):
        return self.channel_info[key]['v']
