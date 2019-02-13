import json
import requests
from urllib import parse
from fake_useragent import UserAgent

import BiliUtil_old.static_func as f
import BiliUtil_old.static_value as v


def get_album_info(aid):
    """
    通过av号获取该号对应的多个视频
    提取可能感兴趣的相关信息并回传
    av号在B站系统中映射为aid编号
    :return: 经过整理的视频信息列表
    """
    param = {
        'aid': str(aid)
    }
    f.print_1('正在获取视频多P列表...', end='')
    http_result = requests.get(v.URL_UP_ALBUM_INFO, params=param)
    if http_result.status_code == 200:
        f.print_g('OK {}'.format(http_result.status_code))
    else:
        f.print_r('RE {}'.format(http_result.status_code))

    # 解析反馈的json数据
    json_data = json.loads(http_result.text)

    # 试图验证json数据是否可用
    if json_data['code'] != 0:
        raise BaseException('获取数据的过程发生错误')

    # 从列表中提取有价值的信息
    album_info = dict()
    album_info['aid'] = {
        'k': '视频av号',
        'v': json_data['data']['aid']
    }
    album_info['time'] = {
        'k': '发布时间',
        'v': json_data['data']['ctime']
    }
    album_info['desc'] = {
        'k': '视频简介',
        'v': json_data['data']['desc']
    }
    album_info['title'] = {
        'k': '视频标题',
        'v': json_data['data']['title']
    }
    album_info['zone'] = {
        'k': '视频分区',
        'v': json_data['data']['tname']
    }
    album_info['num'] = {
        'k': '视频数量',
        'v': json_data['data']['videos']
    }
    album_info['pic'] = {
        'k': '视频封面',
        'v': json_data['data']['pic']
    }
    album_info['like'] = {
        'k': '点赞数',
        'v': json_data['data']['stat']['like']
    }
    album_info['coin'] = {
        'k': '投币数',
        'v': json_data['data']['stat']['coin']
    }
    album_info['favorite'] = {
        'k': '收藏数',
        'v': json_data['data']['stat']['favorite']
    }
    album_info['share'] = {
        'k': '分享数',
        'v': json_data['data']['stat']['share']
    }
    album_info['view'] = {
        'k': '播放数',
        'v': json_data['data']['stat']['coin']
    }
    album_info['danmu'] = {
        'k': '弹幕数',
        'v': json_data['data']['stat']['danmaku']
    }
    album_info['page'] = {
        'k': '分P列表',
        'v': []
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
        album_info['page']['v'].append(video_page)

    return album_info


def get_video_info(aid, cid, cookie=None):
    """
    通过视频的cid编号获得视频下载链接
    自动选取最好画质的视频进行下载
    当存在SESSDATA信息时，
    可下载该用户可观看的最高清的视频
    :return: 视频下载链接及其相关信息
    """
    # 整理用户输入的cookie信息
    if isinstance(cookie, dict):
        cookie = {
            'SESSDATA': cookie['SESSDATA']
        }
    elif isinstance(cookie, str):
        for line in cookie.split(';'):
            name, value = line.strip().split('=', 1)
            if name == 'SESSDATA':
                cookie = {
                    'SESSDATA': value
                }
                break
    else:
        cookie = dict()

    # 获取最高清的视频
    param = {
        'avid': str(aid),
        'cid': str(cid),
        'qn':116,  # 尝试1080P 60fps
        'otype': 'json',
        'fnver': 0,
        'fnval': 16
    }
    header = v.HTTP_HEADER.copy()
    header['Host'] = parse.urlparse(v.URL_UP_VIDEO_INFO).netloc
    header['User-Agent'] = UserAgent().random
    f.print_1('正在获取视频下载地址...', end='')
    http_result = requests.get(url=v.URL_UP_VIDEO_INFO,
                               params=param,
                               headers=header,
                               cookies=cookie)
    if http_result.status_code == 200:
        f.print_g('OK {}'.format(http_result.status_code))
    else:
        f.print_r('RE {}'.format(http_result.status_code))

    # 解析反馈的json数据
    json_data = json.loads(http_result.text)

    # 试图验证json数据是否可用
    if json_data['code'] != 0:
        raise BaseException('获取数据的过程发生错误')

    video_info = dict()
    'aid': {
        'k': 'av号',
        'v': aid
    }
    ,'cid': {
        'k': '视频编号',
        'v': cid
    }
    ,'quality': {
        'k': '视频画质',
        'v': json_data['data']['quality']
    }
    ,'length': {
        'k': '视频长度',
        'v': json_data['data']['timelength']
    }
    ,'video': {
        'k': '视频地址',
        'v': json_data['data']['dash']['video'][-1]['baseUrl']
    }
    ,'audio': {
        'k': '音频地址',
        'v': json_data['data']['dash']['audio'][0]['baseUrl']
    }

    return video_info
