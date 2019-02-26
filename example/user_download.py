import BiliUtil

if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    ua = BiliUtil.User()
    ua.set_by_url('https://space.bilibili.com/6799052/')
    ua.set_cookie(cookie)
    ua.get_all_video_data(base_path='Download', name_path=True)
