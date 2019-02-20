import BiliUtil

if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    av = BiliUtil.Album()
    av.set_by_url('https://www.bilibili.com/video/av42581472')
    av.set_cookie(cookie)
    av.get_album_data(base_path='Download', name_path=True)
