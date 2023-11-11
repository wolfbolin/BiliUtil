# coding=utf-8
import BiliUtil


user_list = [
    ("89916351", "半柠檬", [53712835, "26994127"]),
    # ("6799052", "泡芙酱", []),
    # ("4282930", "豆豆子", []),
    # ("8366990", "欣小萌", []),
    # ("84465926", "小金鱼", []),
    # ("4684911", "凳猫猫", []),
    # ("1600113", "萌爱", []),
    # ("389295398", "ShondaXX", []),
    # ("93411028", "北酱", [57085698]),
    # ("639647", "KAYACHANOWO", []),
    # ("632887", "伢伢", []),
    # ("941422", "优颖酱", [])
]
video_cache = r'D:\Bilibili'

# 设置代理信息
BiliUtil.Config.HTTP_PROXY = 'http://127.0.0.1:12639'
BiliUtil.Config.HTTPS_PROXY = 'http://127.0.0.1:12539'

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
    for up in user_list:
        print('正在下载用户:{} 的视频'.format(up[1]))
        user = BiliUtil.User(up[0])
        fetcher = BiliUtil.Fetcher(user)
        av_list = fetcher.fetch_av_list(BiliUtil.Config.SET_AS_NAME)
        print('视频列表:', av_list)
        positive_list, negative_list = fetcher.load_exist(video_cache)
        print('已存列表:', positive_list)
        exclude_list = positive_list + up[2]
        print('排除列表:', exclude_list)
        task_list = fetcher.load_task(video_cache, exclude_list, video_filter)
        print('任务列表:', task_list)
        download_list = fetcher.pull_all()
        print('完成{}个视频下载：{}'.format(len(download_list), download_list))
