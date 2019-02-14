import json
import requests

import BiliUtil.static_value as v
import BiliUtil.static_func as f


class User:
    uid = None
    name = None
    birthday = None
    coin = None
    face = None
    time = None
    level = None
    sex = None
    sign = None

    def __init__(self, uid):
        print('(=・ω・=)创建用户对象(=・ω・=)')
        self.set_user(str(uid))

    def get_mid(self):
        # 在B站的系统中存在uid与mid混用的情况
        return self.uid

    def set_user(self, uid):
        f.print_1('正在获取用户信息...', end='')
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

        # 修改对象信息
        self.uid = json_data['data']['mid']
        self.name = json_data['data']['name']
        self.birthday = json_data['data']['birthday']
        self.coin = json_data['data']['coins']
        self.face = json_data['data']['face']
        self.time = json_data['data']['time']
        self.level = json_data['data']['level']
        self.sex = json_data['data']['sex']
        self.sign = json_data['data']['sign']

        return self

    def get_user_info(self):
        user_info = {
            'uid': {
                'k': '用户ID',
                'v': self.uid
            },
            'mid': {
                'k': '用户ID',
                'v': self.uid
            },
            'name': {
                'k': '用户昵称',
                'v': self.name
            },
            'birthday': {
                'k': '生日',
                'v': self.birthday
            },
            'coin': {
                'k': '硬币',
                'v': self.coin
            },
            'face': {
                'k': '头像',
                'v': self.face
            },
            'time': {
                'k': '创号',
                'v': self.time
            },
            'level': {
                'k': '等级',
                'v': self.level
            },
            'sex': {
                'k': '性别',
                'v': self.sex
            },
            'sign': {
                'k': '签名',
                'v': self.sign
            }
        }
        return user_info
