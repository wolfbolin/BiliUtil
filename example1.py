import BiliUtil
import asyncio


async def main():
    # DNA视频下载
    # album = BiliUtil.Album("170001")
    # album = BiliUtil.Album("av170001")
    # album = BiliUtil.Album("BV17x411w7KC")
    # album.set_album("456025297")
    # album.set_album("av456025297")
    # album.set_album("BV17x411w7KC")
    # album.set_by_url("https://www.bilibili.com/video/av170001")
    # album.set_by_url("https://www.bilibili.com/video/BV17x411w7KC")
    BiliUtil.Util.set_cookie('')
    album = BiliUtil.Album("BV1fK4y1t7hj")

    album_info = await album.sync()
    print(album_info)

    video_list = await album.get_video_list()
    print(video_list)
    for video in video_list:
        await video.sync()
        task = BiliUtil.Task(video, 'D:/BiliUtil', album.aid)
        await task.start()


if __name__ == '__main__':
    asyncio.run(main())
