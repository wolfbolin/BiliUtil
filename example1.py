import BiliUtil
if __name__ == '__main__':
    album = BiliUtil.Album(3947271)
    # album.set_album(3947271)
    # album.set_by_url("https://www.bilibili.com/video/av3947271")
    album_info = album.sync()
    print(album_info)

    video_list = album.get_video_list()
    for video in video_list:
        video.sync(cookie="SESSDATA=abcd68fd...")
        if len(video_list) > 1:
            video_name = ("P%02d " % video.page) + album.title_list[video.page - 1]
        else:
            video_name = album_info['name']
        task = BiliUtil.Task(video, 'D:/BiliUtil', video_name)
        task.start()
