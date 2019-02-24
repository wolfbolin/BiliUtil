import BiliUtil

if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    ch = BiliUtil.Channel()
    ch.set_by_url('https://space.bilibili.com/4282930/channel/detail?cid=48758')
    ch.set_cookie(cookie)
    ch.get_channel_data(base_path='Download', name_path=True)
