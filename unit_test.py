# coding=utf-8
import json
import BiliUtil
from BiliUtil.bilibili_video import Video

if __name__ == '__main__':
    # Video类测试
    video = Video(8147810, 13399598, '中国各省代表城市以及直辖市城市形象宣传片', 0)
    video_info = video.sync()
    print('Video info: ', json.dumps(video_info, ensure_ascii=False))

    # Album类测试
    album = BiliUtil.Album()
    album.set_by_url('https://www.bilibili.com/video/av8147810')
    album_info = album.sync()
    print('Album info: ', json.dumps(album_info, ensure_ascii=False))
    video_list = album.get_video_list()
    print('Video list: {}'.format(list(video.cid for video in video_list)))

    # Channel类测试
    ch = BiliUtil.Channel()
    ch.set_by_url('https://space.bilibili.com/20165629/channel/detail?cid=9108')
    album_list = ch.get_album_list()
    print('Album list: {}'.format(list(album.aid for album in album_list)))

    # User类测试
    user = BiliUtil.User()
    user.set_by_url('https://space.bilibili.com/20990353/video')
    user_info = user.sync()
    print('User info: ', json.dumps(user_info, ensure_ascii=False))
    album_list = user.get_album_list()
    print('Album list: {}'.format(list(album.aid for album in album_list)))
    channel_list = user.get_channel_list()
    print('Channel list: {}'.format(list(ch.uid for ch in channel_list)))



