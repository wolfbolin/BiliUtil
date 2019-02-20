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
        self.uid = uid

    def set_user(self, uid):
        self.uid = uid
        self.name = None
        self.birthday = None
        self.coin = None
        self.face = None
        self.time = None
        self.level = None
        self.sex = None
        self.sign = None

    def get_user_info(self):
        if self.uid is None:
            raise BaseException('缺少必要的参数')

        f.print_1('正在获取用户信息...', end='')
        param = {
            'mid': str(self.uid),
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

    def get_dict_info(self):
        json_data = vars(self).copy()
        return json_data
