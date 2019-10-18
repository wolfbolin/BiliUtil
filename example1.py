import BiliUtil
if __name__ == '__main__':
    # album = BiliUtil.Album(7134874)  # 旧版视频集合
    # album = BiliUtil.Album(66768830)  # 新版视频集合
    # album = BiliUtil.Album(3947271)  # 旧版单个视频
    album = BiliUtil.Album(71420798)  # 新版单个视频
    # 使用时无需分类，以上仅为说明各种情况均通过测试

    # album.set_album(3947271)
    # album.set_by_url("https://www.bilibili.com/video/av3947271")
    album_info = album.sync()
    print(album_info)

    video_list = album.get_video_list()
    for video in video_list:
        # SESSDATA字段获取：在登录状态下切换到B站标签页，浏览器地址栏左侧小锁->Cookie->bilibili.com->Cookie->SESSDATA
        video.sync(cookie="SESSDATA=abcd68fd...")
        # 分别处理单个视频和视频集合的文件命名
        if len(video_list) > 1:
            video_name = ("P%02d " % video.page) + album.title_list[video.page - 1]
        else:
            video_name = album_info['name']
        task = BiliUtil.Task(video, 'D:/BiliUtil', video_name)
        task.start()
