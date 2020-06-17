import BiliUtil
from cookie import cookie_info

if __name__ == '__main__':
    # DNA视频下载
    album = BiliUtil.Album("170001")
    # album = BiliUtil.Album("av170001")
    # album = BiliUtil.Album("BV17x411w7KC")
    # album.set_album("456025297")
    # album.set_album("av456025297")
    # album.set_album("BV17x411w7KC")
    # album.set_by_url("https://www.bilibili.com/video/av170001")
    # album.set_by_url("https://www.bilibili.com/video/BV17x411w7KC")

    # 4K视频下载测试
    # album = BiliUtil.Album("BV1QV411R7d1")

    album_info = album.sync()
    print(album_info)

    video_list = album.get_video_list()
    print(video_list)
    for video in video_list:
        video.sync(cookie=cookie_info)
        # task = BiliUtil.Task(video, 'D:/BiliUtil', album.aid)
        # task.start()
