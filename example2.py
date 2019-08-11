import BiliUtil
if __name__ == '__main__':
    cookie = ""
    cache = "D:/BiliUtil"

    user = BiliUtil.User(20165629)
    # user.set_user(user)
    # user.set_by_url("https://space.bilibili.com/20165629")
    user_info = user.sync()
    print(user_info)

    fetcher = BiliUtil.Fetcher(user)
    av_list = fetcher.fetch_all(cookie, BiliUtil.Config.SET_AS_NAME)
    print(av_list)

    positive_list, negative_list = fetcher.load_exist(cache)
    print(positive_list)
    print(negative_list)

    task_id = fetcher.load_task(cache, positive_list)
    download_list = fetcher.pull_all()
    print('完成{}个视频下载：{}'.format(len(download_list), download_list))

