import json
import BiliUtil

if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    av = BiliUtil.Album(42524420)
    av.set_cookie(cookie)
    av.get_album('Download', True)
