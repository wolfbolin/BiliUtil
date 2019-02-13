import json
import requests

import BiliUtil_old.static_value as v
import BiliUtil_old.static_func as f


class User:
    def __init__(self, uid):
        print('(=・ω・=)创建用户对象(=・ω・=)')
        self.set_uid(str(uid))

    uid = None
    user_info = dict()

    def set_uid(self, uid):
        self.uid = str(uid)
        param = {
            'mid': str(uid),
            'jsonp': 'jsonp'
        }
        http_result = requests.get(url=v.URL_UP_INFO, params=param,
                                   headers=f.new_http_header(v.URL_UP_INFO))
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))
        json_data = json.loads(http_result.text)
        if json_data['code'] != 0:
            raise BaseException('获取数据的过程发生错误')

        self.user_info = {
            'uid': {
                'k': '用户ID',
                'v': json_data['data']['mid']
            },
            'mid': {
                'k': '用户ID',
                'v': json_data['data']['mid']
            },
            'name': {
                'k': '用户昵称',
                'v': json_data['data']['name']
            },
            'birthday': {
                'k': '生日',
                'v': json_data['data']['birthday']
            },
            'coin': {
                'k': '硬币',
                'v': json_data['data']['coins']
            },
            'face': {
                'k': '头像',
                'v': json_data['data']['face']
            },
            'time': {
                'k': '创号',
                'v': json_data['data']['jointime']
            },
            'level': {
                'k': '等级',
                'v': json_data['data']['level']
            },
            'sex': {
                'k': '性别',
                'v': json_data['data']['sex']
            },
            'sign': {
                'k': '签名',
                'v': json_data['data']['sign']
            }
        }

        return True

    def get_user_info(self):
        return self.user_info

    def get_info_key(self, key):
        return self.user_info[key]['k']

    def get_info_val(self, key):
        return self.user_info[key]['v']


