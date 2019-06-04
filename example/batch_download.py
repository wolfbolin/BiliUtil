# -*- coding: utf-8 -*-
# Common package
import os
import BiliUtil
# Personal package

# Config setting
name_path = True
user_list = {
    '6799052': '泡芙酱',
    '4282930': '豆豆子',
    '8366990': '欣小萌'
}
channel_list = []
exclude_list = []
video_cache = r'/home/bilibili'
cookie = "SESSDATA=123123"


def open_dir(path):
    path = os.path.abspath(path)
    # 扫描当前文件夹
    BiliUtil.merge_video_file(path, True)
    # 递归搜索文件夹
    file_list = os.listdir(path)
    for file in file_list:
        file_path = path + '\\' + file
        if os.path.isdir(file_path):
            open_dir(file_path)


if __name__ == '__main__':
    # 扫描指定用户并下载
    for user in user_list.keys():
        print('正在下载用户:{} 的视频'.format(user_list[user]))
        ua = BiliUtil.User(uid=user)
        ua.set_cookie(cookie)
        exist_list = ua.get_all_video_exist_list(base_path=video_cache, name_path=name_path)
        ua.get_all_video_data(base_path=video_cache, name_path=name_path, exclude_list=exclude_list + exist_list)

    # 扫描指定频道并下载
    for channel in channel_list:
        ch = BiliUtil.Channel(uid=channel[0], cid=[1])
        ch.set_cookie(cookie)
        exist_list = ch.get_exist_list(base_path=video_cache, name_path=name_path)
        ch.get_channel_data(base_path=video_cache, name_path=name_path, exclude_list=exclude_list + exist_list)

    # 递归合并视频
    open_dir(video_cache)
