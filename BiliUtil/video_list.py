import json
import requests
import fake_useragent

import BiliUtil_old.static_func as f
import BiliUtil_old.static_value as v


def get_up_all_video_list(uid, order):
    """
    通过UP主的uid获取该UP主发布的所有视频列表
    但是uid在B站的URL中使用mid表示，不是uid
    order可使用该类中所描述的三种排序方式
    :return: 经过整理的视频信息列表
    """
    param = {
        'mid': str(uid),  # 用户uid
        'pagesize': 30,  # 每页视频数量
        'tid': 0,  # 未知的参数
        'page': 1,  # 当前页码下标
        'keyword': '',  # 可能是分区
        'order': order  # 排序方式
    }
    video_list = []
    while True:
        f.print_1('正在获取第{}页视频列表...'.format(param['page']), end='')
        http_result = requests.get(v.URL_UP_ALL_VIDEO, params=param)
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))

        # 解析反馈的json数据
        json_data = json.loads(http_result.text)

        # 试图验证json数据是否可用
        if json_data['status'] is not True:
            raise BaseException('获取数据的过程发生错误')

        # 从列表中提取有价值的信息
        for video in json_data['data']['vlist']:
            video_list.append({
                'title': video['title'],
                'aid': video['aid']
            })

        # 循环翻页获取并自动退出循环
        if str(json_data['data']['pages']) == str(param['page']):
            break
        else:
            param['page'] += 1

    return video_list


def get_up_channel_video_list(uid, cid):
    """
    获取指定UP名下，某一频道的所有视频列表
    uid与cid必须是配套的，否则无法读取
    :return: 经过整理的视频信息列表
    """
    param = {
        'mid': str(uid),
        'cid': str(cid),
        'pn': 1,  # 当前页码下标
        'ps': 30,  # 每页视频数量
        'order': 0  # 默认排序
    }
    video_list = []
    channel_info = dict()
    while True:
        http_result = requests.get(v.URL_UP_CHANNEL_VIDEO, params=param)
        if http_result.status_code == 200:
            f.print_g('OK {}'.format(http_result.status_code))
        else:
            f.print_r('RE {}'.format(http_result.status_code))

        # 解析反馈的json数据
        json_data = json.loads(http_result.text)

        # 从列表中提取有价值的信息
        ,'cid': {
            'k': '用户编号',
            'v': str(json_data['data']['list']['cid'])
        }
        ,'mid': {
            'k': '频道编号',
            'v': str(json_data['data']['list']['mid'])
        }
        ,'name': {
            'k': '频道名称',
            'v': json_data['data']['list']['name']
        }
        ,'cover': {
            'k': '频道封面',
            'v': json_data['data']['list']['cover']
        }
        ,'count': {
            'k': '视频数量',
            'v': str(json_data['data']['list']['count'])
        }
        for video in json_data['data']['list']['archives']:
            video_list.append({
                'title': video['title'],
                'aid': video['aid']
            })

        # 循环翻页获取并自动退出循环
        if len(video_list) >= int(json_data['data']['page']['count']):
            break
        else:
            param['pn'] += 1

    return video_list, channel_info
