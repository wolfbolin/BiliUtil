HTTP_HEADER = {
    'Host': '',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': '',
    'Referer': 'https://www.bilibili.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

ORDER_LATEST = 'pubdate'  # 按照最新发布进行排序
ORDER_CLICK = 'click'  # 按照最多点击进行排序
ORDER_STAR = 'stow'  # 按照最多收藏进行排序

URL_UP_ALL_VIDEO = 'http://space.bilibili.com/ajax/member/getSubmitVideos'
URL_UP_CHANNEL_VIDEO = 'http://api.bilibili.com/x/space/channel/video'
URL_UP_ALBUM_INFO = 'http://api.bilibili.com/x/web-interface/view'
URL_UP_VIDEO_INFO = 'http://api.bilibili.com/x/player/playurl'
URL_UP_INFO = 'GET https://api.bilibili.com/x/space/acc/info?mid=4282930&jsonp=jsonp'

file_cache_path = 'temp'
file_output_path = 'video'
