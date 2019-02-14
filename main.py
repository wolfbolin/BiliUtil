import json
import BiliUtil

if __name__ == '__main__':
    av = BiliUtil.Album(42524420)
    av.set_cookie()
    av.get_album('Download', True)
