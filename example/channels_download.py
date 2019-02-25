import BiliUtil

if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    ua = BiliUtil.User()
    ua.set_by_url('https://space.bilibili.com/4093899/channel/index')
    ua.set_cookie(cookie)
    ua.get_channel_video_data(base_path='Download', name_path=True)
