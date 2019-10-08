import BiliUtil

album = BiliUtil.Album(7134874)
album_info = album.sync()
print(album_info)
video_list = album.get_video_list()
# print(video_list)

for video in video_list:
    #print(video)
    video.sync(cookie="SESSDATA=22c52c9...")
    video_name = ("P%03d " % video.page) + album.title_list[video.page - 1]
    task = BiliUtil.Task(video, 'D:/BiliUtil', video_name)
    task.start()
