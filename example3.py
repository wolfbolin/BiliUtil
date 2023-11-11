# coding=utf-8
import BiliUtil

user_list = [
    # Up 的 Pid， Up的名字， 排除av列表
    ("4282930", "豆豆子", []),
    ("8366990", "欣小萌", []),
]

video_cache = r'D:\Bilibili'
cookie = "SESSDATA=7f110a70%YbWeLCx2F7xXKJ8A%2C6c989ea1"  # 假的

# 设置代理信息
BiliUtil.Util.set_cookie(cookie)
BiliUtil.Config.HTTP_PROXY = 'http://127.0.0.1:8888'
BiliUtil.Config.HTTPS_PROXY = 'http://127.0.0.1:8888'

if __name__ == '__main__':
    # 初始化过滤器
    # 设置视频质量限制
    quality = [BiliUtil.Config.Quality.V1080P,
               BiliUtil.Config.Quality.V1080Px,
               BiliUtil.Config.Quality.V1080P60,
               BiliUtil.Config.Quality.V720P60,
               BiliUtil.Config.Quality.V720P]
    length = [40, 600]  # 设置视频长度
    ratio = [1, 2]  # 设置视频比例，只保留横屏
    video_filter = BiliUtil.Filter(quality=quality, length=length, ratio=ratio)

    # 扫描指定用户并下载
    # 模仿该方式，你也可以下载用户某个频道下的全部视频
    for up in user_list:
        print('正在下载用户:{} 的视频'.format(up[1]))
        user = BiliUtil.User(up[0])
        fetcher = BiliUtil.Fetcher(user)
        av_list = fetcher.fetch_av_list(BiliUtil.Config.SET_AS_NAME)
        print(av_list)
        positive_list, negative_list = fetcher.load_exist(video_cache)
        exclude_list = positive_list + up[2]
        task_list = fetcher.load_task(video_cache, exclude_list, video_filter)
        print(task_list)
        download_list = fetcher.pull_all()
        print('完成{}个视频下载：{}'.format(len(download_list), download_list))
