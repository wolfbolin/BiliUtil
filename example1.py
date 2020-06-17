import BiliUtil
if __name__ == '__main__':
    # album = BiliUtil.Album("170001")
    # album = BiliUtil.Album("av170001")
    album = BiliUtil.Album("BV17x411w7KC")
    # album.set_album("456025297")
    # album.set_album("av456025297")
    # album.set_album("BV17x411w7KC")
    # album.set_by_url("https://www.bilibili.com/video/av170001")
    # album.set_by_url("https://www.bilibili.com/video/BV17x411w7KC")
    album_info = album.sync()
    print(album_info)

    video_list = album.get_video_list()
    print(video_list)
    for video in video_list:
        video.sync()
        print(video.video)
        task = BiliUtil.Task(video, 'D:/BiliUtil', album.aid)
        task.start()
